nginx 已安装在此处，且站点配置在 `127.0.0.1:8080`，但它无法启动。
`systemctl status nginx` 下的日志行指明了原因：`bind() to 127.0.0.1:8080 failed (98: Address already in use)`。

某个其他进程已经占用了该地址和端口上的监听套接字，而默认情况下内核只允许一个进程占用。
`ss` 可以从内核读取套接字表并找出该所有者：

```text
$ sudo ss -tlnp 'sport = :8080'
State    Recv-Q   Send-Q     Local Address:Port     Peer Address:Port  Process
LISTEN   0        4096           127.0.0.1:8080          0.0.0.0:*      users:(("legacy-relay",pid=324,fd=3))
```

`-t` 将列表限制为 TCP（`-u` 为 UDP），`-l` 限制为处于监听状态的套接字，`-n` 将端口显示为数字而不是服务名称，`-p` 则添加 `users:` 字段：进程名、PID 以及持有该套接字的文件描述符。
直接运行 `ss -tlnp` 会列出所有 TCP 监听者；带引号的过滤条件则仅保留源端口（本地端）为 8080 的行。
若不带 `sudo` 运行，Process 列将保持为空，因为 `ss` 无法读取属于其他用户（包括 root）的进程。

本地地址决定了谁可以连接。
`127.0.0.1` 仅接受来自本机的连接，`0.0.0.0` 接受来自任意 IPv4 地址的连接，`[::]` 接受来自任意 IPv6 地址的连接，而 `*` 接受来自任何地址的连接。

`legacy-relay` 是可执行文件的文件名，并没有 unit 使用该名称。
可以将 PID 提供给 systemd：`systemctl --no-pager status 324`（请使用你自己的 PID）会输出拥有该进程的 unit，而 `cat /proc/324/cgroup` 则以 cgroup 路径的形式显示相同的答案：`0::/system.slice/ops-legacy-proxy.service`。


该 unit 配置了 `Restart=always` 并且已启用（enabled）。
杀掉该 relay 进程后，systemd 会立刻重新启动一个新的；停止它后，在下次开机时它仍然会恢复运行。
`systemctl disable --now` 是 `enable --now` 的相反操作，可以通过一条命令停止它并移除开机启动链接。

### 要求

- `ops-legacy-proxy.service` 已被停止并禁用（disabled）：`/usr/local/lib/ops/legacy-relay` 不再运行，且 `/etc/systemd/system/multi-user.target.wants/ops-legacy-proxy.service` 已被移除。
- `nginx.service` 处于 active 状态，且仍在 `127.0.0.1:8080` 上监听。
  请保持 `/etc/nginx/conf.d/ops.conf` 原样不变；将 nginx 迁移到其他端口不计入完成。
- 在执行 `ss -p` 以及每一次 `systemctl` 更改时均使用 `sudo`。

### 解答

```bash
# 找出占用 8080 端口的进程
sudo ss -tlnp 'sport = :8080'

# 取出该进程的 PID，并查出它所属的 unit
pid=$(sudo ss -tlnp 'sport = :8080' | sed -n 's/.*pid=\([0-9]*\).*/\1/p')
systemctl --no-pager status "$pid"
cat /proc/"$pid"/cgroup

# 停止并禁用该 unit（一条命令完成 stop + 移除开机链接）
sudo systemctl disable --now ops-legacy-proxy.service

# 端口释放后启动 nginx
sudo systemctl start nginx

# 确认结果
systemctl is-active nginx
sudo ss -tlnp 'sport = :8080'
systemctl is-enabled ops-legacy-proxy.service
```
