内核在允许进程绑定低于 1024 的 TCP 端口之前，从不检查它是否为 root。
它检查的是 **capability**：root 的权力被划分为 41 个具名权限，掩码中的每一位代表一项权限，而用于低位端口的位是 `CAP_NET_BIND_SERVICE`（第 10 位，掩码 `0x400`）。
运行在 81 端口的服务只需要该位，而不需要其余的 40 个权限，其中包括 `CAP_SYS_ADMIN`（挂载及更多操作）和 `CAP_DAC_OVERRIDE`（忽略文件权限）。

进程在若干个集合中持有其 capability，`grep Cap /proc/PID/status` 会以十六进制掩码的形式打印它们。
当前虚拟机上已安装的 `ops-hello.service` 以 root 身份运行，其对应内容如下：

```text
CapInh:	0000000000000000
CapPrm:	000001ffffffffff
CapEff:	000001ffffffffff
CapBnd:	000001ffffffffff
CapAmb:	0000000000000000
```

`capsh --decode` 可以将掩码解析为名称。
它位于 `/usr/sbin` 中，该路径不在你的 `PATH` 中，因此需要通过完整路径调用：`/usr/sbin/capsh --decode=0000000000000400` 会输出 `0x0000000000000400=cap_net_bind_service`，而 `000001ffffffffff` 则解码为全部 41 个权限。

- `CapEff` 是 effective 集合，即内核在进程执行操作时检查的位。
  `CapPrm` 是 permitted 集合，代表进程可以启用的权限。
- `CapBnd` 是 bounding 集合，即权限上限：一旦某个 capability 从中被移除，该进程或其启动的任何进程都永远无法再次获取它。
  仅在上限内保留某项 capability 本身并不会赋予任何权限。
- `CapAmb` 是 ambient 集合。
  当非 root 进程运行普通程序时，内核会清空其 permitted 和 effective 集合，唯独保留 ambient 集合传递过来的权限。
  `CapInh` 是 inheritable 集合，必须持有相同的位，systemd 会自动填入这些位。

这最后一条规则解释了为什么仅配置 `User=` 会导致低端口服务失败：
systemd 切换到该账户并运行程序，而程序启动时没有任何 capability。
三条指令可以解决此问题：

```ini
[Service]
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
```

`AmbientCapabilities=` 将列出的 capability 置入服务的 ambient 集合中，进而进入其 permitted 和 effective 集合，使其在切换到 `User=` 后依然生效。
`CapabilityBoundingSet=` 将上限裁剪为该列表。
`NoNewPrivileges=yes` 会设置内核的 `no_new_privs` 标志，子进程会继承该标志且任何操作都无法清除它：
像 `sudo` 这样的 setuid 程序将不再能够提升特权，因此 sudo 会拒绝运行。
即使在只有一个位的上限下，该标志依然至关重要，因为 setuid-root 程序以 uid 0 运行，而 uid 0 可以通过普通所有者权限写入 `/etc` 的大部分内容。
`/proc/PID/status` 将其报告为 `NoNewPrivs: 1`；而在你的 shell 中显示为 `0`。


### 以 opsweb 身份运行 ops-hello

当 `ops-hello.service` 启动时，其脚本 `/usr/local/lib/ops/ops-hello.sh` 会将 `id -un` 以及自身的 capability 和 `NoNewPrivs` 行写入 `/run/ops-hello/status`，然后替换自身为一个监听在 `127.0.0.1:81` 上的监听器，向每个连接应答其运行所使用的账户。
系统账户 `opsweb` 已经存在。

使用 `sudo` 在 `/etc/systemd/system/ops-hello.service.d/` 下添加一个 drop-in 配置，设置 `User=opsweb` 以及上述三条指令，重载 systemd 并重启该服务使其处于 active 状态。
drop-in 应该放在 `/etc` 下，以便系统重启后服务仍保持该配置。
此时 `/run/ops-hello/status` 的内容必须为：

```text
opsweb
CapInh:	0000000000000400
CapPrm:	0000000000000400
CapEff:	0000000000000400
CapBnd:	0000000000000400
CapAmb:	0000000000000400
NoNewPrivs:	1
```

随后运行 `bash -c 'exec 3<>/dev/tcp/127.0.0.1/81; cat <&3'` 将打印 `hello from ops-hello as opsweb`。

在重启后立即发起的连接可能会在监听器启动完成前被拒绝；重新运行一次即可。

### 解答

```bash
# 在 /etc 下写入 drop-in：以 opsweb 运行，只保留绑定低位端口的 capability，并禁止提升特权
sudo mkdir -p /etc/systemd/system/ops-hello.service.d
sudo tee /etc/systemd/system/ops-hello.service.d/opsweb.conf > /dev/null <<'EOF'
[Service]
User=opsweb
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
EOF

# 重载 systemd 并重启服务
sudo systemctl daemon-reload
sudo systemctl restart ops-hello.service
systemctl is-active ops-hello.service

# 验证状态文件和监听器（连接被拒绝时再运行一次）
cat /run/ops-hello/status
/usr/sbin/capsh --decode=0000000000000400
bash -c 'exec 3<>/dev/tcp/127.0.0.1/81; cat <&3'
```
