`/srv/ops/bin/portbind` 设置了 setuid root，以便以无特权账户 `opsportal`（uid 2200）运行的 `ops-portal.service` 能够绑定低于 1024 的端口 `127.0.0.1:82`。

这一代价体现在 `/run/ops-portal/status` 中，该 unit 在启动后立即在此记录了其主进程信息：

```text
Uid:	2200	0	0	0
CapEff:	000001ffffffffff
```

实际 UID 仍然是 2200，但有效（effective）、已保存（saved）和文件系统（filesystem）UID 均为 0，且每个 capability 位都被置位。
一个只需要单项特权的辅助程序因此可以读写系统上的所有文件。

文件 capability（file capability）仅授予二进制文件所需的特权。
它存储在文件的 `security.capability` 扩展属性中，无论谁运行该文件，内核在 exec 时都会将列出的 capability 添加到新进程中。
每个 capability 都带有标志（flags）：
`p` 将其放入允许集合（permitted set），即进程可能使用的集合；`e` 则放入有效集合（effective set），即内核实际检查的集合。
自行管理 capabilities 的程序可以将 permitted 集合中的 capability 提升到 effective 集合中；`portbind` 是 `systemd-socket-activate` 的副本，它从不执行此操作，因此需要同时设置这两者。
绑定低于 1024 的端口需要 `cap_net_bind_service`，即 `CapEff` 的第 10 位。
清除 setuid 位（`chmod u-s FILE`）而未添加该 capability 会导致绑定失败并报错 `Permission denied`。


`setcap NAME=FLAGS FILE` 用于写入属性，`getcap FILE` 用于打印属性，而 `setcap -r FILE` 用于删除属性。
以下示例在具有 `cap_net_raw`（原始套接字 capability）的 `true` 临时副本上执行这些命令：

```console
$ sudo cp /bin/true /srv/ops/bin/demo
$ sudo setcap cap_net_raw=ep /srv/ops/bin/demo
$ sudo getcap /srv/ops/bin/demo
/srv/ops/bin/demo cap_net_raw=ep
$ sudo setcap -r /srv/ops/bin/demo
```

在执行 `setcap -r` 之后，`getcap` 不会针对该文件打印任何内容。
`getcap -r DIR` 会遍历整个目录树，并仅打印带有 capability 的文件。
这两个工具都位于 `/usr/sbin`，不在你的 `PATH` 中，因此需要通过 `sudo` 运行。
`ls -l` 从不显示 capabilities，这也是为什么跳过权限检查的二进制文件可以在普通目录列表中不被察觉的原因，而在 `/srv/ops/bin` 中除了 `portbind` 之外还有一个这样的文件。

`AmbientCapabilities=` 将 capability 授予单个 unit 的进程；而文件 capability 则会赋予每个被允许执行该文件的账户。
将 `net.ipv4.ip_unprivileged_port_start` 降低到 1024 以下并不是替代方案：
这样一来，每个账户都可以绑定从新数值往上的任何端口，而不仅仅是这个辅助程序。

该属性很容易丢失。
普通的 `cp` 创建的新文件不包含该属性，并且写入文件会将其清除，因此被替换的二进制文件需要重新执行 `setcap`。

内核还会忽略带有 `nosuid` 标志的挂载点上以及具有 no\_new\_privs 的进程中的文件 capabilities，因此若在 `ops-portal.service` 中添加 `NoNewPrivileges=yes` 将会导致绑定失败。
`/srv/ops/bin` 是为本课程挂载的一个小型 tmpfs，未设置 `nosuid`，因为此虚拟机的根文件系统无法存储 `security.capability`。


### 要求

- `/srv/ops/bin/portbind` 仍由 root 所有，权限模式为 0755，且仅在 permitted 和 effective 集合中带有 `cap_net_bind_service`，不包含其他 capability。
  除了服务的主进程外，每次启动 `ops-portal.service` 还会以 `nobody` 身份在 `127.0.0.1:83` 上运行一次 `portbind`，并将 `bound` 或 `denied` 写入 `/run/ops-portal/nobody-bind`。
  该文件内容必须为 `bound`（只有存储在文件上的 capability 才能赋予此权限），且 `net.ipv4.ip_unprivileged_port_start` 保持为 1024。
- `ops-portal.service` 处于运行状态，且 `/run/ops-portal/status` 显示 `Uid:` 后跟 4 次 2200 以及 `CapEff: 0000000000000400`。
  该文件仅在服务启动时写入，因此在更改二进制文件后请运行 `sudo systemctl restart ops-portal.service`。
- `/srv/ops/bin/logscan`（`cat` 的副本）保留在原位，所有者为 root 且权限模式为 0755，并移除其 capability，使 `nobody` 不再能通过它读取 `/etc/shadow`。
  除带有 `cap_net_bind_service` 的 `portbind` 外，系统上的任何其他文件也不得携带 capability。
  在你运行每条命令后，以 root 运行的检查会将以下内容写入 `/run/dometrain-state/logscan-check`：`nobody` 从 `logscan` 获取的结果以及该文件的权限模式和所有者 uid、随后是 `getcap` 为 `portbind` 打印的内容、最后是带有 capability 的任何其他文件。
  其内容必须为以下三行：`denied 755 0`、`portbind: cap_net_bind_service=ep` 以及 `others: none`（使用 `sudo cat` 可查看最新内容）。


### 解答

```bash
# 清除 setuid 位，权限模式恢复为 0755
sudo chmod 0755 /srv/ops/bin/portbind
# 只授予绑定低端口所需的 capability（permitted + effective）
sudo setcap cap_net_bind_service=ep /srv/ops/bin/portbind
# 移除 logscan 上的 capability，文件本身保留原位
sudo setcap -r /srv/ops/bin/logscan
# 确认整个系统只剩 portbind 带有 capability
sudo getcap -r / 2>/dev/null
# 确认 portbind 和 logscan 的所有者与权限模式
ls -l /srv/ops/bin/portbind /srv/ops/bin/logscan
# 重启服务，让 status 文件按新二进制重新写入
sudo systemctl restart ops-portal.service
systemctl is-active ops-portal.service
sudo cat /run/ops-portal/status
sudo cat /run/ops-portal/nobody-bind
sudo sysctl net.ipv4.ip_unprivileged_port_start
sudo cat /run/dometrain-state/logscan-check
```
