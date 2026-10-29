还有两个指令可以将服务与整台机器通常共享的资源隔离开来：`/tmp` 中的临时暂存空间以及网络。

```ini
[Service]
PrivateTmp=yes
PrivateNetwork=yes
```

- `PrivateTmp=yes` 为服务提供其专属的空 `/tmp` 和 `/var/tmp`。
  在宿主机上，该服务的 `/tmp` 是 systemd 在启动时创建的一个目录 `/tmp/systemd-private-<boot ID>-<unit>-<random>/tmp`，它被挂载到服务 mount namespace 中的 `/tmp` 之上。
  服务写入的文件会保存在这里，其他进程无法在各自的 `/tmp` 中看到它们；宿主机 `/tmp` 中已有的文件对该服务不可见，但对其他进程保持不变。
  当服务停止时，systemd 会删除其私有目录。
  每个 unit 都会获得自己独立的目录，因此通过 `/tmp` 交换文件的两个服务将无法再看到彼此的文件（`JoinsNamespaceOf=` 可以将它们放回同一个命名空间；本任务不需要此配置）。
- `PrivateNetwork=yes` 在一个新的 network namespace 中启动服务，该命名空间是一个独立的网络栈副本，具有自己的接口、地址和端口，仅包含具有 127.0.0.1 的环回接口 `lo`。
  该 127.0.0.1 属于该命名空间，因此监听在宿主机环回接口上的宿主机守护进程将无法被访问。
  绑定到路径的 Unix socket 仍可正常工作：它们是文件系统中的文件，而 network namespace 并不覆盖文件系统。
  由 `ss -x` 列出且带有前导 `@` 的抽象 Unix socket 没有对应的文件，属于 network namespace，因此服务也无法访问宿主机守护进程的抽象 socket。

### 隔离 ops-convert.service

`ops-convert.service` 当前在未沙箱化的状态下运行。
每次启动时，其脚本都会用三行内容重写 `/srv/ops/convert/probe.txt`：`tmp` 说明其是否能看到 `/tmp/ops-host-marker`（位于宿主机 `/tmp` 中的文件）；`net` 说明与 127.0.0.1:7171 的 TCP 连接是否成功（socket unit `ops-canary.socket` 监听于此并回复 `canary`）；`links` 列出来自 `ip -o link` 的接口名称。
目前内容为 `tmp=shared`、`net=reachable`、`links=lo,enp0s5`。


使用 `sudo`，在 `/etc/systemd/system/ops-convert.service.d/` 下添加一个 drop-in，设置 `PrivateTmp=yes` 和 `PrivateNetwork=yes`，重新加载 systemd 并重启该服务使其处于 active 状态。
该文件随后必须准确显示为：

```text
tmp=private
net=isolated
links=lo
```

这些行必须来自 `ops-convert.service` 自身（在 systemd 加载你的 drop-in 之后启动）：`systemctl show -p PrivateTmp -p PrivateNetwork ops-convert.service` 对两者都必须输出 `yes`。


你自己的视角保持不变。
`ls /tmp` 仍会列出 `ops-host-marker`，以及一个新的 `systemd-private-...-ops-convert.service-...` 目录；`sudo find /tmp -name ops-convert.scratch` 会找到两份副本：未沙箱化运行时留在宿主机 `/tmp` 中的副本，以及私有目录内的活跃副本。
`bash -c 'exec 3<>/dev/tcp/127.0.0.1/7171; cat <&3'` 对你而言仍会输出 `canary`。


### 解答

```bash
# 在 /etc 下写入 drop-in，为服务提供私有 /tmp 和独立的网络命名空间
sudo mkdir -p /etc/systemd/system/ops-convert.service.d
sudo tee /etc/systemd/system/ops-convert.service.d/isolate.conf > /dev/null <<'EOF'
[Service]
PrivateTmp=yes
PrivateNetwork=yes
EOF

# 重新加载 systemd 并重启服务
sudo systemctl daemon-reload
sudo systemctl restart ops-convert.service
systemctl is-active ops-convert.service
systemctl show -p PrivateTmp -p PrivateNetwork ops-convert.service

# 验证服务写出的结果
cat /srv/ops/convert/probe.txt

# 验证自己的视角未受影响
ls /tmp
sudo find /tmp -name ops-convert.scratch
bash -c 'exec 3<>/dev/tcp/127.0.0.1/7171; cat <&3'
```
