`ops-report.service` 当前正在以 `REPORT_MODE=draft` 运行，因为其 unit 文件通过内联方式设置了 `Environment=REPORT_MODE=draft`。

该主机应使用的值已保存在 `/etc/ops/report.env` 中，且 unit 可以通过 `EnvironmentFile=` 加载它们：

```ini
[Service]
Environment=REPORT_MODE=draft
EnvironmentFile=/etc/ops/report.env
EnvironmentFile=-/etc/ops/report.local.env
```

每次 unit 启动时，systemd 自身都会以 root 身份读取列出的每个文件。
文件的行格式为 `KEY=VALUE`，以 `#` 开头的行为注释。
但行中后部的 `#` 则不是注释：
`REPORT_MODE=final # host default` 会将值 `final # host default` 传给程序，因此请将注释单独写在独立的行中。
值周围的双引号会被移除，但不会进行 shell 展开：
`$HOME` 或 `$(date)` 会作为字面文本传递给程序。
因为读取操作发生在启动阶段，修改环境变量文件后只需执行 restart 即可。
`daemon-reload` 仅用于修改了 unit 文件的情况。

无论两行在 unit 中位于何处，来自 `EnvironmentFile=` 文件的变量都会覆盖通过 `Environment=` 设置的同名变量；当有两个文件设置了同一变量时，后列出的文件生效。
因此，上述程序将从 `report.env` 获取模式。
第二个路径前的 `-` 使其成为可选文件：
如果它不存在，systemd 会跳过它。
若没有 `-`，文件缺失会导致启动失败。

`systemctl show -p Environment` 无法确定最终生效的值，因为它只打印 `Environment=` 行。
进程实际收到的变量位于 `/proc/<pid>/environ` 中，以 NUL 分隔的条目形式存在，使用 `tr '\0' '\n' < /proc/PID/environ` 可以每行打印一个。
该服务以 root 身份运行，而 `sudo` 无法作用于你当前 shell 打开的 `<` 重定向，因此请通过 `sudo cat` 管道输出该文件：

```bash
sudo cat /proc/$(systemctl show -p MainPID --value ops-report.service)/environ | tr '\0' '\n' | grep '^REPORT_'
```

### 加载报告设置

使用 `sudo` 编辑 `/etc/systemd/system/ops-report.service`，在其 `[Service]` 部分添加 `EnvironmentFile=` 行以加载 `/etc/ops` 中已存在的两个文件，使运行的服务接收到：

- 来自 `/etc/ops/report.env` 的 `REPORT_MODE=final` 和 `REPORT_DIR=/srv/ops/reports`；
- 位于 `/etc/ops/report.secret.env` 中的上传凭据 `REPORT_TOKEN`，该文件只有 root 可以读取。
  切勿将 token 本身放入任何 `Environment=` 行中：
  该 unit 文件的权限模式为 644，且 `systemctl show -p Environment` 会向任何用户打印内联的值。

在列出这两个文件时不要加 `-`：
每台主机都包含它们，因此若启动时无法读取其中之一，应该报错失败，而不是在缺少配置或 token 的情况下运行。
此外，将 `/etc/ops/report.local.env` 列为可选文件。
该文件在此主机上不存在，但其他主机上会有。
原有的两个内联 `Environment=` 行保留或删除均可。
然后运行 `sudo systemctl daemon-reload`，重启该服务并检查其处于 active 状态。
在每次启动时，它都会将接收到的已排序 `REPORT_*` 变量写入 `/run/ops/report.env-seen`，并将 `systemctl show -p EnvironmentFiles -p Environment` 针对其报告的内容写入 `/run/ops/report.unit-seen`。


### 解答

```bash
# 在 [Service] 标头之后添加三行 EnvironmentFile=，可选文件前加 -
sudo sed -i '/^\[Service\]/a EnvironmentFile=/etc/ops/report.env\nEnvironmentFile=/etc/ops/report.secret.env\nEnvironmentFile=-/etc/ops/report.local.env' /etc/systemd/system/ops-report.service
sudo systemctl daemon-reload
sudo systemctl restart ops-report.service

# 检查
systemctl is-active ops-report.service
sudo cat /proc/$(systemctl show -p MainPID --value ops-report.service)/environ | tr '\0' '\n' | grep '^REPORT_'
cat /run/ops/report.env-seen /run/ops/report.unit-seen
```
