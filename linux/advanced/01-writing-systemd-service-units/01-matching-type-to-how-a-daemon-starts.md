`ops-relay.service` 曾启动过一次，目前处于 `inactive (dead)` 状态，没有遗留任何 relay 进程。
它的 unit 文件中没有 `Type=` 配置行，因此 systemd 应用了默认的 `Type=simple`。

这是它运行的程序 `/usr/local/sbin/ops-relay`：

```bash
#!/bin/bash
case "${1:-}" in
  --loop)
    # 告诉启动器 relay 已在提供服务，然后空闲等待，直到 systemd 停止它。
    echo serving > /run/ops-relay.ready
    sleep infinity ;;
  --warmup)
    # 加载路由三秒，然后变为 relay 循环（相同的 PID）。
    sleep 3
    exec /usr/local/sbin/ops-relay --loop ;;
esac
rm -f /run/ops-relay.ready
mkfifo -m 0600 /run/ops-relay.ready
setsid /usr/local/sbin/ops-relay --warmup </dev/null >/dev/null 2>&1 &
echo "$!" > /run/ops-relay.pid
read -r _ < /run/ops-relay.ready
rm -f /run/ops-relay.ready
exit 0
```

在不带参数运行时，它会使用 `setsid` 启动自身的第二个副本，将该副本的 PID 写入 `/run/ops-relay.pid`，并阻塞等待读取命名管道 `/run/ops-relay.ready`。

该副本以 `ops-relay --warmup` 形式运行 3 秒，然后通过 `exec` 替换为 `ops-relay --loop`（保持相同的 PID），并向管道写入 `serving`。

只有在此之后，启动脚本才会以 0 退出，因此在它返回时，relay 已经在提供服务了。

### Type= 对 systemd 的意义

在 `Type=simple` 下，systemd 将它为 `ExecStart=` 启动的脚本视作 unit 的**主进程**（main process，即其退出意味着服务终止的进程），并在 fork 该脚本的瞬间就认定启动完成。
3 秒后，一旦副本报告它已开始提供服务，该脚本便以 0 退出；对 systemd 而言，这就意味着服务已结束：
它记录了 `Deactivated successfully` 并停止了该 unit 的 cgroup 中的所有进程。
虽然 `setsid` 为副本分配了新的 session，但该副本仍然位于该 cgroup 中，因此 relay 也随之终止。
`Type=exec` 的表现也是一样的。
它与 `Type=simple` 的唯一区别在于 `systemctl start` 还会等待程序被执行，因此如果二进制文件缺失，启动操作本身就会失败。

`Type=forking` 适用于会将自身放入后台运行的程序。
当 `ExecStart=` 进程退出时，启动才算完成，而它留下的运行中的子进程将成为主进程。
systemd 不会按名称选取该子进程。
在父进程退出后，它会读取 `PIDFile=` 中的绝对路径，因此 daemon 必须在退出前写入该文件，且该文件通常应位于 `/run` 目录下。
这两个键都应放在 `[Service]` 小节中，因为若放在 `[Unit]` 下，systemd 会记录 `Unknown key` 并忽略它们：

```ini
[Service]
Type=forking
PIDFile=/run/ops-relay.pid
ExecStart=/usr/local/sbin/ops-relay
```

已加载的 unit 会保留 systemd 先前解析的定义。
当前 unit 会一直保持加载状态，因为另一个处于 active 状态的 unit `ops.target` 引用了它，所以在修改文件后，必须在启动前执行 `sudo systemctl daemon-reload`，否则启动仍会使用 `Type=simple`。

之后，`systemctl show -p MainPID ops-relay.service` 会输出 systemd 接管的 PID，该值应等于 `/run/ops-relay.pid` 中的数字；`systemctl show -p Type -p PIDFile ops-relay.service` 则会显示 systemd 实际使用的类型和 PID 文件。

### 任务

- 使用 `sudo` 重写 `/etc/systemd/system/ops-relay.service` 的 `[Service]` 小节，声明 `Type=forking` 和 `PIDFile=/run/ops-relay.pid`，并保留 `ExecStart=/usr/local/sbin/ops-relay` 以及 `[Unit]` 和 `[Install]` 小节。
- 重新加载 systemd 并启动 `ops-relay.service`。
  它必须保持 active 状态，`ops-relay --loop` 进程必须正在运行，`systemctl show -p Type -p PIDFile ops-relay.service` 必须输出 `Type=forking` 和 `PIDFile=/run/ops-relay.pid`，并且 `systemctl show -p MainPID ops-relay.service` 必须输出 `/run/ops-relay.pid` 中的 PID。
  在 `Type=forking` 下，由于 systemd 需要等待启动脚本退出，`systemctl start` 大约需要 3 秒才会返回。

### 解答

```bash
# 在 [Service] 小节标头之后插入 Type= 和 PIDFile=，其余行（含 ExecStart=、[Unit]、[Install]）保持不变
sudo sed -i '/^\[Service\]/a Type=forking\nPIDFile=/run/ops-relay.pid' /etc/systemd/system/ops-relay.service
sudo systemctl daemon-reload
# 约 3 秒后返回
sudo systemctl start ops-relay.service

# 检查
systemctl is-active ops-relay.service
pgrep -af 'ops-relay --loop'
systemctl show -p Type -p PIDFile ops-relay.service
systemctl show -p MainPID ops-relay.service
cat /run/ops-relay.pid
```
