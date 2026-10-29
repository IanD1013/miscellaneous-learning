`ops-quarantine.service` 将一个 token 写入了 `/tmp/handoff.token`，并向 `lo` 添加了第二个地址，但在宿主机上执行 `cat /tmp/handoff.token` 却提示 `No such file or directory`，并且 `ip -o -4 addr show dev lo` 只列出了 `127.0.0.1/8`。

每个命令查看的都是当前 shell 所在的命名空间（namespace）。
`PrivateTmp=yes` 和 `PrivateNetwork=yes` 为该 unit 分配了独立的 mount namespace（存放其专属的 `/tmp`）以及独立的 network namespace（存放其专属的 `lo`），而你的 shell 及其启动的所有进程仍留在宿主机的命名空间中。

`nsenter` 可以在另一个进程的命名空间内运行命令。
传入 `-t` 和 PID 后，它会根据你指定的类型打开该进程的 `/proc/PID/ns/` 条目，对每个条目调用 `setns` 将自身切换进去，然后执行你的命令，因此该命令能够看到目标进程所看到的内容。
这些标志包括：`-m` 代表 mount namespace，`-n` 代表 network，`-u` 代表 UTS（主机名），`-p` 代表 PID。
进入另一个进程的命名空间需要 root 权限，因此需要使用 `sudo` 运行。

要找到目标，`systemctl show -p MainPID --value ops-quarantine.service` 可以输出 systemd 为该 unit 跟踪的主 PID，而 `sudo lsns -p PID` 可以列出该进程所属的命名空间以及每个命名空间中的最小 PID；其中显示该服务自身的 PID 而非 PID 1 的行，就是它未与 init 共享的命名空间。
获取 PID 后，命名空间标志放在 `--` 之前，要运行的命令放在其后：

```bash
sudo nsenter -t PID -m -- ls -l /tmp
sudo nsenter -t PID -n -- ip -br link
```

第一个命令列出该进程看到的 `/tmp`，第二个命令列出其 network namespace 中的网络设备。
`--` 表示 nsenter 选项的结束，因此其后的所有内容（包括标志）都属于目标命令。
PID 可以直接填写数字，也可以写作 `$(systemctl show -p MainPID --value ops-quarantine.service)`。

单次调用也可以同时进入多个命名空间，例如 `sudo nsenter -t PID --mount --net -- sh -c '...'`。


重启会为服务分配全新且空白的命名空间，并且该 unit 是从一个已被删除的一次性 handoff 文件中读取这两个值的，因此一旦重启，unit 将失败且无法留下任何可供检查的内容。
从宿主机端读取 token 也是可行的：
`PrivateTmp=` 会将服务的 `/tmp` 保留在 `/tmp/systemd-private-*-ops-quarantine.service-*/tmp/` 下，位于只有 root 才能打开的目录中，因此通配符 `*` 必须在通过 `sudo sh -c '...'` 启动的 root shell 中展开，而不是在你的普通 shell 中。
但地址的情况有所不同：
由于 handoff 文件已不复存在，它仅作为活动状态保留在服务的 network namespace 中，因此你必须从该命名空间内部进行读取。

### 需求

- `/home/learner/ops/quarantine-token` 仅包含来自服务 `/tmp/handoff.token` 的 token。
- `/home/learner/ops/quarantine-addrs` 包含服务 network namespace 内 `lo` 上的 IPv4 地址及其 `/prefix`，格式为 `ip addr show` 输出的任意形式。
- `ops-quarantine.service` 仍在运行你开始时所运行的同一进程。


### 解答

```bash
# 找到服务的主 PID 并查看它的命名空间
PID=$(systemctl show -p MainPID --value ops-quarantine.service)
sudo lsns -p $PID
# 进入服务的 mount namespace 读取其专属 /tmp 中的 token
sudo nsenter -t $PID -m -- cat /tmp/handoff.token > /home/learner/ops/quarantine-token
# 进入服务的 network namespace 读取 lo 上的 IPv4 地址
sudo nsenter -t $PID -n -- ip -o -4 addr show dev lo > /home/learner/ops/quarantine-addrs
# 确认结果，且服务 PID 未变
cat /home/learner/ops/quarantine-token /home/learner/ops/quarantine-addrs
systemctl show -p MainPID --value ops-quarantine.service
```
