`[Service]` 中的 `Restart=` 决定了哪些退出情况会促使 systemd 重新启动程序。
`Restart=on-failure` 会在非零退出码、超时或因异常信号（如 `SIGKILL` 或 `SIGSEGV`）终止后重启程序。
它不会对正常退出执行重启：即退出状态为 0，或者 `SIGTERM`、`SIGINT`、`SIGHUP`、`SIGPIPE`，systemd 将这些视为刻意停止。
`Restart=always` 会在每次退出后都进行重启（包括正常退出），因此即便程序主动选择退出且返回值为 0，也会被立即重新启动。
这两种策略都不会重启你通过 `systemctl stop` 停止的 unit。
`RestartSec=` 是每次重启前的暂停时间，如果不设置，默认是 100ms。
systemd 会在 unit 的 `NRestarts` 属性中记录当前运行周期的自动重启次数（`systemctl show -p NRestarts ops-ingest.service`）；你手动输入的 `systemctl start` 会从 0 开始一个新的运行周期。

每次启动都会计入该 unit 的启动限制，自动重启同样算作启动：
在 `StartLimitIntervalSec=` 时间内最多允许 `StartLimitBurst=` 次启动，默认是 10 秒内 5 次。
随后的启动请求将被拒绝。
systemd 会记录日志 `Start request repeated too quickly.`，停止重启并将 unit 保持在 failed 状态。
当被拒绝的启动是一次自动重启时（如同此循环中的情况），systemd 252 会将 unit 的结果保留为上一次崩溃时的 `exit-code`，因此在这里该 journal 日志行是限制被触发的唯一迹象。
在计数器重置之前，手动执行 `systemctl start` 也不会运行任何东西。
当时间窗口过去、执行 `sudo systemctl reset-failed ops-ingest.service` 或执行 `systemctl daemon-reload`（同样会重置该计数器）时，计数器会被清除。

要度过崩溃循环，你可以拉大尝试间隔、允许更多启动次数，或者两者兼顾。
限制指令配置在 `[Unit]` 中：

```ini
[Unit]
StartLimitIntervalSec=60
StartLimitBurst=10

[Service]
Restart=on-failure
RestartSec=3
```

两次尝试之间间隔 3 秒，10 秒的时间窗口内最多只能容纳 4 次启动。
`[Unit]` 中的这对配置将限制放宽到了每分钟 10 次启动。

### 让 ops-ingest.service 完成预热

`/usr/local/sbin/ops-ingest` 每次启动时都会将 `/var/lib/ops-ingest/attempts` 中的数值加 1。
它的 feed 只有在单个运行周期内经历 6 次自动重启后才会响应，因此重复手动启动永远无法达到该状态。
6 次自动重启需要经历 7 次启动，所以前 6 次启动它会记录 `feed not ready (start N)` 并立即以状态码 1 退出。
从第 7 次启动开始，它会读取 unit 的 `NRestarts`：
若低于 6，它会记录 `feed not ready (start N, restart R)` 并以 1 退出；若达到 6，则会记录 `feed ready after 6 restarts`，将计数值写入 `/var/lib/ops-ingest/ready` 并保持运行。
当它以状态码 0 退出时，代表它是有意停止，并且必须保持停止状态。

仅编辑文件本身是不够的；systemd 还必须加载修改后的内容。
`systemctl show -p Restart,RestartUSec,StartLimitBurst,StartLimitIntervalUSec,NeedDaemonReload ops-ingest.service` 会输出这些值（`NeedDaemonReload=yes` 表示 unit 文件包含 systemd 尚未重新加载的修改），并且这些配置必须允许单个运行周期内容纳 7 次启动。

当 burst 为 7 或更多，或者仅重启间隔就能覆盖整个时间窗口（即 `StartLimitBurst=` 乘以 `RestartSec=` 至少达到 `StartLimitIntervalSec=`）时，单个运行周期内就可以容纳 7 次启动。
按照默认的 10 秒 5 次计算，这意味着 `RestartSec=2` 或更大。
时间窗口从第一次启动开始计算，而在超过 `StartLimitIntervalSec=` 之后发生的启动会开启一个新的窗口，因此每次尝试在 `RestartSec=` 之外所花费的时间就是你的富余量。
计算时不要将它算入总和，因为它会随程序运行和机器繁忙程度而变化。
如果设置 `RestartSec=1`，该 worker 早期的启动会立即失败，因此 5 次间隔加起来只有大约 6 秒，第 6 次启动就会被拒绝。
关闭限制（`StartLimitIntervalSec=0` 或 `StartLimitBurst=0`）也可以让 7 次启动通过。
代价是 systemd 永远不会停止尝试：
如果程序彻底持续失败，只要机器还在运行，它就会在每次崩溃后不断重启，并且 journal 中永远不会记录拒绝信息。
将 burst 设置为适合预热的大小（例如 1 分钟内 10 次启动）也能启动此 worker，并且它仍然会在程序持续失败时放弃重启。

`/etc/systemd/system/ops-ingest.service` 使用 `Restart=always` 和 `RestartSec=0` 运行该 worker，此前已经触发了限制并处于 failed 状态，随后 attempts 文件被重置为 0。
使用 `sudo` 执行以下操作：

- 查找 `ops-ingest.service` 的 journal 日志行，确认 systemd 放弃重启的记录。
- 使用 `tee` 或任意编辑器重写该 unit 文件，将其改为 `Restart=on-failure` 而不是 `Restart=always`，并修改 `RestartSec=`、启动限制或同时修改两者，以便在单个运行周期内容纳 7 次启动。
- 重新加载 systemd 并启动该服务。
  最终状态必须为 active，worker 正在运行，attempts 文件中的数值达到 7 或更多，`/var/lib/ops-ingest/ready` 已被写入，且 systemd 加载的配置值显示 `Restart=on-failure`、`NeedDaemonReload=no`，以及允许容纳 7 次启动的间隔和限制。
  如果间隔设置为 3 秒，大约需要 25 秒，当 ready 文件生成后检查将自动通过。

### 解答

```bash
# 确认 systemd 放弃重启的 journal 记录
sudo journalctl --no-pager -u ops-ingest.service | grep 'Start request repeated too quickly'

# 改为 Restart=on-failure，并把间隔设为 3 秒（5 次 x 3 秒 >= 10 秒窗口，可容纳 7 次启动）
sudo sed -i -e 's/^Restart=.*/Restart=on-failure/' -e 's/^RestartSec=.*/RestartSec=3/' /etc/systemd/system/ops-ingest.service
sudo systemctl daemon-reload
sudo systemctl start ops-ingest.service

# 大约 25 秒后检查
systemctl is-active ops-ingest.service
cat /var/lib/ops-ingest/attempts /var/lib/ops-ingest/ready
systemctl show -p Restart,RestartUSec,StartLimitBurst,StartLimitIntervalUSec,NeedDaemonReload ops-ingest.service
```
