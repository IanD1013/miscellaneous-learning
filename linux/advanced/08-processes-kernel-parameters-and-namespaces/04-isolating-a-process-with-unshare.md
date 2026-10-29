进程看到的主机名、它看到的 PID 编号以及它的挂载表都各自来自一个命名空间（namespace），而在同类型的不同命名空间中的进程看到的则是自己独立的一套内容。
本课将使用这三种类型：`uts`（主机名）、`pid` 和 `mnt`。

第四种类型 `net` 包含网络接口和端口，它就是 `PrivateNetwork=` 让 systemd 为服务创建的内容。
每个进程在每种类型中都恰好处于一个命名空间中，子进程会在其父进程的命名空间中启动，`/proc/<pid>/ns/` 中的链接命名了它们：

```text
$ readlink /proc/self/ns/uts /proc/self/ns/pid
uts:[4026531838]
pid:[4026531836]
```

括号中的数字标识了命名空间，打印相同数字的进程共享该命名空间。
`lsns` 列出命名空间及其进程计数和最低 PID，而 `lsns -p PID` 则显示单个进程所在的命名空间。
对于另一个账户（包括 root）拥有的进程，`readlink` 和 `lsns -p` 都需要 `sudo`；没有它，它们什么也不会输出。

### 在新的命名空间中运行程序

`unshare` 在新的命名空间中启动程序，并且在该系统上只有 root 可以创建它们。
对于 UTS 或挂载命名空间，`unshare` 会在启动程序之前将自身移入其中，因此在新的 UTS 命名空间中设置的主机名会保留在该命名空间内：

```text
$ sudo unshare --uts sh -c 'hostname scratch; hostname'; hostname
scratch
dometrain-linux
```

PID 命名空间从不吸纳创建它的进程。
它的子进程会在内部创建，并且第一个子进程会成为 PID 1。
`--fork` 让 `unshare` 将你的程序作为第一个子进程启动。
如果没有它，程序会留在外部，它的第一个子进程会成为 PID 1，并且一旦该子进程退出，后续的每次 fork 都会失败。

`ps` 读取 `/proc`，在有程序挂载新的 `/proc` 之前，它会一直描述宿主机。
`--mount-proc` 会在一个新的挂载命名空间内执行该操作，该挂载命名空间由它为你创建：

```text
$ sudo unshare --pid --fork ps -o pid,comm | head -3
  PID COMMAND
    1 systemd
    2 kthreadd
$ sudo unshare --uts --pid --fork --mount-proc ps -o pid,comm
  PID COMMAND
    1 ps
```

### 任务

提供的 `/usr/local/sbin/opsbox-report` 会记录它看到的主机名、其自身的 PID 以及 PID 1 的名称，然后作为 `opsbox-hold` 继续运行，以使命名空间保持活动状态。
花括号内的第一行将主机名保存到 `/run/ops` 下的一个单独文件中以供本练习使用，并不参与本任务：

```bash
#!/bin/bash
{
  hostname > "/run/ops/opsbox-hostname/$(cut -d' ' -f22 /proc/$$/stat)" 2>/dev/null
  echo "hostname=$(hostname)"
  echo "pid=$$"
  echo "init=$(cat /proc/1/comm)"
} > /home/learner/ops/sandbox.txt
exec -a opsbox-hold sleep 100000
```

使用 `sudo unshare` 在新的 UTS、PID 和挂载命名空间中启动它，并带有全新的 `/proc`，在它运行之前在内部将主机名设置为 `opsbox`。

`unshare` 只运行一个程序，因此请为其提供 `sh -c`，包含 `hostname opsbox` 以及紧随其后的 `exec /usr/local/sbin/opsbox-report`。

`exec` 会用该脚本替换 shell，而不是将其作为子进程启动，因此该脚本本身在读取 `/proc/1/comm` 时就是 PID 1。
该脚本永不退出，因此请在行尾添加 `&` 使其在后台保持运行。

- `/home/learner/ops/sandbox.txt` 的内容完全为：

```text
hostname=opsbox
pid=1
init=opsbox-report
```

- 机器自身的主机名保持为 `dometrain-linux`。
- 名为 `opsbox-hold` 的进程仍在运行，处于其自有的 UTS、PID 和挂载命名空间中。

然后运行 `sudo lsns -p $(pgrep -f '^opsbox-hold ')`。

新的 `mnt` 和 `uts` 行计数为两个进程：`unshare` 和 `opsbox-hold`，因为 `unshare` 移入了这些命名空间。
新的 `pid` 行计数为一个进程。


### 解答

```bash
# 在新的 UTS、PID、挂载命名空间中运行，挂载全新的 /proc，先设置主机名再 exec 脚本，放到后台
sudo unshare --uts --pid --fork --mount-proc sh -c 'hostname opsbox; exec /usr/local/sbin/opsbox-report' &
# 确认结果
cat /home/learner/ops/sandbox.txt
hostname
sudo lsns -p $(pgrep -f '^opsbox-hold ')
```
