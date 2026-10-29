端口可以在背后没有运行任何程序的情况下接受连接。
这正是 socket unit 的作用：
systemd 绑定并持有该地址，只有当客户端连接时处理进程才会存在，并通过 systemd 继承的文件描述符获取其 socket，而不是自己去绑定端口。
借助下面介绍的 `Accept=yes`，该处理程序甚至可以完全省略网络代码。
监听端是一个 `.socket` 文件：

```ini
[Socket]
ListenStream=127.0.0.1:7070
Accept=yes
```

`ListenStream=` 指定了 TCP 地址和端口。
请务必同时提供两者：
仅写 `ListenStream=7070` 会在所有接口上监听。
该端口在 socket unit 启动时打开，因此关键步骤是 `sudo systemctl start ops-echo.socket`，随后 `systemctl status ops-echo.socket` 会报告 `Active: active (listening)` 和 `Listen: 127.0.0.1:7070 (Stream)`，而此时处理进程并不存在。
启动或启用（enable）service 绝不会打开此端口。
你应该启动的是 socket unit，如果要在开机时启用它，需配置包含 `WantedBy=sockets.target` 的 `[Install]` 部分（在此虚拟机上对 socket 执行 `enable --now` 大约需要 10 秒）。

`Accept=` 决定了 service 会接收到什么。
在默认值 `Accept=no` 下，一个以 socket 命名的单个 service（`ops-echo.service`）会接收监听 socket，并且必须在其上调用 accept，而 shell 脚本无法做到这一点。
使用 `Accept=yes` 时，systemd 会接受每个连接，并为每个连接启动以该 socket 命名的模板实例 `ops-echo@.service`；该实例在其进程退出时停止。
普通的 `ops-echo.service` 无法接受实例名称，因此在 `Accept=yes` 下，首个客户端会被断开连接且 socket 会失败。

在模板中，`StandardInput=socket` 将已接受的连接附加到处理程序的 stdin。
除非专门设置，否则 stdout 会跟随 stdin，因此程序打印的内容会直接返回给客户端：

```ini
[Service]
ExecStart=/usr/local/sbin/ops-echo
StandardInput=socket
```

`/usr/local/sbin/ops-echo` 已经安装好：
它读取一行并回复 `ok` 以及该行内容。
它还会将该行追加到 `/run/ops/echo.log` 中，并加上其运行所在的 unit 以及其 stdin 为前缀，因此日志会显示是否是由 socket 激活的实例为其提供了服务。

### 需求

- 创建 `/etc/systemd/system/ops-echo.socket`（仅监听 `127.0.0.1:7070` 并设置 `Accept=yes`），以及运行处理程序的模板 `/etc/systemd/system/ops-echo@.service`。
  写入这两个文件都需要 `sudo`；之后请运行 `sudo systemctl daemon-reload`。
- `ops-echo.socket` 处于 active 状态。
- 通过 bash 的 `/dev/tcp` 重定向发送 `check-in` 这行内容（这会在文件描述符 3 上打开一个 TCP 连接）。
  它会打印 `ok check-in`，然后 `/run/ops/echo.log` 中会包含类似 `ops-echo@0-127.0.0.1:7070-127.0.0.1:43344.service stdin=socket check-in` 的行，由提供该连接服务的实例写入（手动运行处理程序会记录不同的 unit，这不算数）：

```bash
exec 3<>/dev/tcp/127.0.0.1/7070; printf 'check-in\n' >&3; cat <&3; exec 3<&-
```

### 解答

```bash
# 创建 socket unit：仅监听 127.0.0.1:7070，每个连接启动一个模板实例
sudo tee /etc/systemd/system/ops-echo.socket <<'EOF'
[Socket]
ListenStream=127.0.0.1:7070
Accept=yes
EOF

# 创建模板 service：已接受的连接作为处理程序的 stdin（stdout 跟随 stdin）
sudo tee /etc/systemd/system/ops-echo@.service <<'EOF'
[Service]
ExecStart=/usr/local/sbin/ops-echo
StandardInput=socket
EOF

# 重新加载并启动 socket unit（不是 service）
sudo systemctl daemon-reload
sudo systemctl start ops-echo.socket
systemctl status ops-echo.socket --no-pager

# 通过 /dev/tcp 发送 check-in，应打印 ok check-in
exec 3<>/dev/tcp/127.0.0.1/7070; printf 'check-in\n' >&3; cat <&3; exec 3<&-

# 确认日志由 ops-echo@...service 实例写入且 stdin=socket
cat /run/ops/echo.log
```
