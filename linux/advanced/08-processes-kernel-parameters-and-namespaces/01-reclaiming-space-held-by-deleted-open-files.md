在 `/srv/ops/spool` 上，`df` 和 `du` 的统计结果相差约 48 MiB：

```text
$ df -h /srv/ops/spool; sudo du -sh /srv/ops/spool
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda         55M   49M  1.5M  98% /srv/ops/spool
782K	/srv/ops/spool
```

这个差距是由一个失去了文件名但仍处于打开状态的文件导致的。
`rm` 会移除文件名，从而减少文件的链接数（link count），内核仅在链接数为零且没有进程通过打开的文件描述符（file descriptor）持有该文件时，才会释放该 inode 及其数据块。
`du` 是通过文件名遍历来累加文件大小，因此被删除的文件会立即从其统计总和中移除；而 `df` 报告的是文件系统已分配的数据块，只要描述符仍处于打开状态，这些数据块就会一直保持已分配。

在此处，`ops-spooler.service` 在文件描述符 3 上以追加模式打开了 `/srv/ops/spool/spool.log`，而这个 48 MiB 的日志文件在该 spooler 仍保持打开时被删除了。
下一个批次需要在这个文件系统上腾出 8 MiB 的空间，而 `df` 显示的 1.5M 可用空间远远不够。
`/srv/ops/spool/archive` 中的三个文件总共只有 768 KiB，因此删除它们也无法腾出足够的空间。

### 查找持有该文件的进程

进程打开的每个描述符都会以其编号命名显示在 `/proc/PID/fd` 下的符号链接中，当其背后的文件失去了文件名时，链接目标会显示为 `path (deleted)`。

`systemctl show -p MainPID --value ops-spooler` 会输出该 spooler 的 PID，使用该 PID 运行 `sudo ls -l /proc/PID/fd` 会显示：

```text
l-wx------ 1 root root 64 Oct  7 03:11 3 -> '/srv/ops/spool/spool.log (deleted)'
```

要一次性搜索所有进程，可以使用 `sudo lsof +L1` 列出链接数小于 1 的每个打开文件，并显示命令名称、PID、描述符（`3w` 表示以写入模式打开的文件描述符 3）以及 `NLINK` 0。
这两个命令都需要 `sudo`，因为 spooler 以 root 身份运行，而 `learner` 无法检查其他账户的描述符。

### 释放数据块

重启 spooler 会关闭该描述符并释放空间，但这会中断服务，而终止（kill）它则会导致服务直接中断。
直接操作描述符链接即可：
`/proc/PID/fd/3` 指向 spooler 持有的同一个已删除 inode，因此 `sudo truncate -s 0 /proc/PID/fd/3` 会将该文件截断为零字节并立即释放其数据块，同时 spooler 依然保持着描述符 3。
Spooler 以 `O_APPEND`（即 `>>` 重定向）打开了该文件，因此它的下一次写入会落在文件的新末尾。
如果某个程序在打开文件时未使用 `O_APPEND`，它将继续在旧的偏移量处写入，从而在新的数据前留下稀疏空洞（sparse hole）。
任何以 root 身份打开该链接并执行截断的操作都能达到同样的效果，例如 `sudo sh -c ': > /proc/PID/fd/3'`。


### 要求

- `/srv/ops/spool` 所在的文件系统本身是 `/dev/sda`，且至少有 8 MiB 可用空间。
  检查在每个命令执行后以 root 身份运行，因此在释放数据块的命令执行完毕后即视为通过。
  挂载在 `/srv/ops/spool` 之上的其他文件系统的可用空间，或者卸载 spool 磁盘后的可用空间，均不计入。
- `ops-spooler.service` 必须保持运行，切勿重启或 kill 它。
  它将其启动次数记录在 `/run/ops/spooler.starts` 中，该文件内容必须仍为 `1`。


### 解答

```bash
# 找到 spooler 的 PID
PID=$(systemctl show -p MainPID --value ops-spooler)
# 确认描述符 3 指向已删除的 spool.log
sudo ls -l /proc/$PID/fd
sudo lsof +L1
# 通过描述符链接把已删除文件截断为零字节，立即释放数据块
sudo truncate -s 0 /proc/$PID/fd/3
# 确认可用空间至少 8 MiB，且服务未被重启
df -h /srv/ops/spool
systemctl is-active ops-spooler
cat /run/ops/spooler.starts
```
