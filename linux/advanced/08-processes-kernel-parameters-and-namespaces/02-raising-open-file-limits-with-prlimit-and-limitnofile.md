`/etc/security/limits.d/ops.conf` 为 `gateway` 账户分配了 8192 个打开文件数，然而以 `User=gateway` 运行的 `ops-gateway.service` 却只有 64 个。
该文件由 `pam_limits` 读取，这是一个在打开 PAM 会话（例如控制台登录、`su`、`sudo`、SSH 登录）时应用 `limits.conf` 和 `limits.d` 的 PAM 模块。
systemd 启动服务时不会创建 PAM 会话，因此这些文件中的任何配置都不会传递给它。
服务从其自身的 unit 文件中获取限制。

每个进程针对每种资源都有两项限制。
软限制（soft limit）由内核强制执行：
一旦进程持有的文件描述符数量达到其软限制 `RLIMIT_NOFILE`，其接下来打开文件的操作就会失败并报错 EMFILE（"Too many open files"）。
硬限制（hard limit）则是上限天花板。
进程可以将自身的软限制最高提升至硬限制，而只有 root 用户可以提高硬限制。
通过 fork 创建的子进程会继承父进程限制的副本。
任何用户都可以读取这些限制：

```bash
cat /proc/PID/limits
```

在 `/proc/<pid>/limits` 中，`Max open files` 这一行依次显示软限制值和硬限制值。
`systemctl show -p MainPID --value ops-gateway` 可以输出 gateway 的 PID。

`prlimit` 可以修改已经在运行的进程的限制：

```bash
sudo prlimit --pid PID --nofile=1024:2048
```

该参数的值为 soft:hard 格式，因此这会将该进程的软限制设为 1024，硬限制设为 2048。
传入单个数字会同时设置两者：
`--nofile=1024` 会使硬限制也变成 1024。
只有该进程及其在此之后 fork 出的子进程能感知到此更改。
gateway 属于另一个用户，因此不加 `sudo` 执行 `prlimit` 即使仅进行读取也会被拒绝；但 `/proc` 则没有这个限制。

systemd 在启动服务时会根据 `LimitNOFILE=` 设置服务的限制。
该值采用相同的 soft:hard 格式，因此在 `[Service]` 下配置 `LimitNOFILE=1024:2048` 会在启动时将其软限制设为 1024、硬限制设为 2048。
在执行 `sudo systemctl daemon-reload` 之前，新增的 drop-in 配置对 systemd 是不可见的；即使重载之后，正在运行的进程仍然保持其现有的限制，新配置将等待下一次启动生效。
systemd 也会从 `/run/systemd/system/` 加载 drop-in，但 `/run` 在每次开机时都会被清空，因此放在那里的限制无法在下次重启后继续保留。
`systemctl show -p LimitNOFILE -p LimitNOFILESoft ops-gateway.service` 会输出 systemd 届时将应用的值，其中 `LimitNOFILE` 保存的是硬限制值。

### 将 ops-gateway.service 提升至 4096:8192

gateway 需要软限制为 4096、硬限制为 8192，该限制需要立即对当前运行生效并在之后的每次启动时保持，且**不能重启该服务**：

- 使用 `prlimit` 提升正在运行的 gateway 的限制。
- 使用 `sudo` 在 `/etc/systemd/system/ops-gateway.service.d/` 下添加一个 drop-in 配置，在其 `[Service]` 部分将 `LimitNOFILE=` 设置为相同的数值对，然后重载 systemd。
  不要重启该服务。

`systemctl show -p DropInPaths -p NeedDaemonReload ops-gateway.service` 会输出 systemd 在上次重载时为该 unit 加载的 drop-in 文件列表，以及自那时起磁盘上的 unit 文件是否发生过变动。
当已加载的 unit 文件或 drop-in 被编辑或删除，或者已读取的 drop-in 目录中出现了新文件时，`NeedDaemonReload` 会变为 `yes`。

你即将创建的 drop-in 位于一个尚不存在的目录中，因此在重载之前，它只会表现为 `DropInPaths` 中缺失的条目，且 `NeedDaemonReload` 保持为 `no`。

`/run/ops/gateway.starts` 记录了 gateway 的启动次数（当前为 `1`）。
完成所有操作后，gateway 在 `/proc` 中的 `Max open files` 行应显示 `4096` 和 `8192`，systemd 报告 `LimitNOFILE=8192` 以及 `LimitNOFILESoft=4096`，`DropInPaths` 仅列出 `/etc/systemd/system/ops-gateway.service.d/` 中的文件，`NeedDaemonReload` 为 `no`，且启动计数仍为 `1`。



### 解答

```bash
# 找到 gateway 的 PID
PID=$(systemctl show -p MainPID --value ops-gateway)
# 立即提升正在运行进程的限制（软 4096，硬 8192）
sudo prlimit --pid $PID --nofile=4096:8192
grep 'Max open files' /proc/$PID/limits
# 添加持久的 drop-in 配置
sudo mkdir -p /etc/systemd/system/ops-gateway.service.d
printf '[Service]\nLimitNOFILE=4096:8192\n' | sudo tee /etc/systemd/system/ops-gateway.service.d/limits.conf
# 重载 systemd，不重启服务
sudo systemctl daemon-reload
# 确认 systemd 将应用的值、drop-in 路径和重载状态
systemctl show -p LimitNOFILE -p LimitNOFILESoft -p DropInPaths -p NeedDaemonReload ops-gateway.service
cat /run/ops/gateway.starts
```
