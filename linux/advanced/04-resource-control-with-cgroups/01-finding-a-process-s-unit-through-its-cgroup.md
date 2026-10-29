`ledger-compact` 是一个繁忙的进程，你被要求将其终止，但直接杀死它并不能彻底解决问题。
它以 `root` 身份运行，因此终止操作需要 `sudo`，而且几秒钟后它就会以新的 PID 重新生成副本：

```shell
$ old=$(pgrep ledger-compact); sudo kill $old; sleep 6; echo "old=$old new=$(pgrep ledger-compact)"
old=161 new=187
```

是一个 systemd 服务启动了该替代进程。
其 `Restart=always` 策略会在进程以任何方式退出后重新启动它，即使是普通的 `kill`（SIGTERM）所引发的正常退出也是如此；而如果是 `Restart=on-failure`，此时则会保持停止状态。
要彻底停止该工作，你需要停止对应的 unit，而该 unit 的名称记录在进程的 cgroup 中，而不是进程名中。

### 每个进程对应一个 cgroup

在 **cgroup v2** 下，内核维护着一棵单独的控制组（control groups）树，挂载在 `/sys/fs/cgroup`，并且每个进程恰好位于其中一个控制组中。
systemd 负责构建这棵树：
每个 slice（一组 unit，例如用于服务的 `system.slice`）都是一个目录，而每个服务在其 slice 下都有自己的叶子目录。
fork 出的子进程会在其父进程的 cgroup 中启动，因此服务运行的所有内容都会归入该服务的叶子目录中。

`/proc/<pid>/cgroup` 显示了一个进程所在的位置：

```bash
cat /proc/PID/cgroup
```

在 cgroup v2 上，它会打印一行内容，即 `0::` 加上 `/sys/fs/cgroup` 下的路径。
cgroup v1 会为每个控制器层级打印一行，这也是进程可能同时存在于多个组中的概念来源。
对于服务而言，该路径的最后一部分就是该 unit 的完整名称。

另外两种视图也能得到相同的答案。
`systemd-cgls --no-pager` 可以绘制出带有每个叶子目录内 PID 的树；添加类似 `/system.slice` 的路径可以只绘制特定的分支。
`systemctl status PID` 接受 PID 代替 unit 名称，并报告拥有该进程的 unit。
这三种方法都不需要 `sudo`，即使对于以 `root` 运行的进程也是如此，因为每个用户都可以读取 `/proc/<pid>/cgroup`。


内核根据其可执行文件为进程命名，而 unit 则是根据其 unit 文件命名的，因此这两个名称是各自独立选择的。
请务必从 cgroup 路径中获取 unit 名称，切勿直接取自进程名。

### 任务

- 将包含 `ledger-compact` 所在 cgroup 的 unit 完整名称（包含 `.service` 后缀）写入 `/home/learner/ops/owner-unit`，文件中不要包含任何其他内容。
- 使用 `sudo systemctl stop` 停止该 unit，以确保没有遗留任何正在运行的 `ledger-compact` 进程。
  使用 `sudo systemctl disable --now` 同样可以停止它，并且还能防止它在开机时启动。
- 保持所有其他服务的初始状态，维持运行并保持启用（enabled）。

### 解答

```bash
# 查看 ledger-compact 所在的 cgroup，路径最后一部分就是 unit 名称
pid=$(pgrep -o ledger-compact)
cat /proc/$pid/cgroup
systemctl status $pid --no-pager

# 取 cgroup 路径的最后一部分写入文件
basename "$(cut -d: -f3 /proc/$pid/cgroup)" > /home/learner/ops/owner-unit
cat /home/learner/ops/owner-unit

# 停止该 unit（只动这一个 unit）
sudo systemctl stop "$(cat /home/learner/ops/owner-unit)"

# 确认已没有 ledger-compact 进程
sleep 6
pgrep ledger-compact || echo "no ledger-compact running"
```
