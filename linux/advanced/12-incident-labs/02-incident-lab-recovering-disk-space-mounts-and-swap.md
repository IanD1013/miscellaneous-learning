下一批处理任务需要在 `/srv/ops/spool` 上获得 8 MiB 的空间，但 `df` 显示那里的可用空间远低于该值。
`/srv/ops/archive` 尚未挂载，并且 `sudo mount /srv/ops/archive` 报错拒绝。
虽然 `/etc/fstab` 中包含一条 swap 条目，但 `/proc/swaps` 中没有任何记录。
每个问题都对应 `/dev/sda` 上各自的分区，因此请逐个排查解决。
分区表本身已经是正确的；请勿修改分区布局。

重启系统并不是事故排查手段：
它只能通过终止 spooler 来释放 spool 空间，且无助于解决另外两个问题。
archive 挂载行缺少 `nofail`，因此 systemd 会将该挂载视为本地文件系统的必需项，启动时的挂载失败会导致系统进入 emergency mode；而 swap 条目依然会像现在这样报错失败。
无法挂载的文件系统并不一定损坏。
在着手使用修复工具之前，请将 fstab 行所请求的内容与分区上的实际内容进行对比，因为 `/srv/ops/archive/manifest.txt` 中存有必须保留的数据。

### 限制条件

`/srv/ops/spool` 是 `/dev/sda1` 上的 ext4 文件系统。
`ops-spooler.service` 运行 `/usr/local/sbin/ops-spooler`，它会将其启动次数写入 `/run/ops/spooler.starts`。

该文件当前内容为 `1`，在你完成时必须仍为 `1`，且保持相同的 spooler 进程持续运行：
禁止重启，禁止终止（kill）。
空间必须在 `/dev/sda1` 本身释放，因此在整个过程中 `/srv/ops/spool` 必须始终保持从该分区挂载。
在 `/srv/ops/spool` 之上覆盖挂载其他文件系统所获得的可用空间，或者在卸载 spool 的情况下获得的可用空间，均不计入。

`findmnt --verify` 会根据当前存在的设备检查每一行 fstab 配置。
请使用 `sudo` 运行它，因为以 `learner` 用户运行时无法打开块设备，并会在报告中夹杂 `Permission denied` 警告。
`blkid`、`mkswap` 和 `swapon` 位于 `/sbin` 中，不在你的 `PATH` 内，因此调用它们时请使用 `sudo`，如同你对 `/etc/fstab` 的每次修改一样。

### 要求达到的最终状态

- 挂载在 `/srv/ops/spool` 的文件系统为 `/dev/sda1`，且以 root 视角的可用空间至少为 8 MiB。
- `/run/ops/spooler.starts` 仍然为 `1`，且 `ops-spooler.service` 仍处于 active 状态，运行着与初始时相同的 `/usr/local/sbin/ops-spooler` 进程。
  手动启动该脚本的副本属于不同的进程，不计入在内。
- `/srv/ops/archive` 以 `ext4` 类型挂载，且 `/srv/ops/archive/manifest.txt` 未被更改。
- `/etc/fstab` 以类型 `ext4` 挂载 `/srv/ops/archive`，挂载方式可以使用 `LABEL=ops-archive`、文件系统已有的 UUID（修改该行配置，而非修改文件系统）或 `PARTLABEL=archive`，其选项中包含 `nofail` 且没有 `noauto`，以便开机时也能挂载，并且不存在指定了磁盘未拥有的 UUID 的活动行。
- `/proc/swaps` 列出 `/dev/sda3` 且类型为 `partition`，同时你的 fstab swap 行使用的标识方式与当前 `sudo blkid /dev/sda3` 报告的内容一致。
  再次运行 `mkswap` 会写入新的 UUID，因此请在其执行后再修改 fstab 行。
- `/etc/fstab` 中包含一条针对 `/dev/sda3` 的 swap 行，挂载点为 `none`，类型为 `swap`，带有 `nofail` 且没有 `noauto`，以便开机时也能启用它；该行可以使用指向该分区的设备路径（`/dev/sda3` 本身或其在 `/dev/disk/by-*` 下的链接之一）或 `sudo blkid /dev/sda3` 实际报告的 `UUID=`、`LABEL=`、`PARTUUID=` 或 `PARTLABEL=` 值来指定该分区。
  所有其他活动的 swap 行均已移除，包括针对 `/home/learner/ops/swapfile` 的那一行；被注释掉的行视为已移除。
- 根目录行 `host9p / 9p trans=virtio,version=9p2000.L,rw 0 0` 保持完全不变。

### 解答

```bash
# 排查：对比 fstab 请求的内容与分区上的实际内容
cat /etc/fstab
sudo findmnt --verify
sudo blkid /dev/sda1 /dev/sda2 /dev/sda3
cat /proc/swaps
df -h /srv/ops/spool
stat -f /srv/ops/spool

# 1. spool 空间：找出仍被进程打开、但已删除的 spool 文件
sudo find /proc/[0-9]*/fd -lname '/srv/ops/spool/* (deleted)' -printf '%p -> %l\n' 2>/dev/null

# 通过 /proc/<pid>/fd 截断这些文件以释放空间，不重启也不终止 spooler
for fd in $(sudo find /proc/[0-9]*/fd -lname '/srv/ops/spool/* (deleted)' 2>/dev/null); do
    sudo truncate -s 0 "$fd"
done

# stat -f 中 Free 为 root 视角的可用块数，确认至少 8 MiB
df -h /srv/ops/spool
stat -f /srv/ops/spool
findmnt /srv/ops/spool
cat /run/ops/spooler.starts

# 2. 注释掉现有的 archive 行和所有 swap 行（根目录行不受影响）
sudo sed -i -E 's@^([^#[:space:]]+[[:space:]]+/srv/ops/archive[[:space:]])@#\1@' /etc/fstab
sudo sed -i -E 's@^([^#[:space:]]+[[:space:]]+[^[:space:]]+[[:space:]]+swap[[:space:]])@#\1@' /etc/fstab

# 按文件系统标签以 ext4 挂载 archive，带 nofail
echo 'LABEL=ops-archive /srv/ops/archive ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount /srv/ops/archive
findmnt /srv/ops/archive
cat /srv/ops/archive/manifest.txt

# 3. swap：分区上没有可用的 swap 签名时才运行 mkswap，再启用
sudo swapon /dev/sda3 || { sudo mkswap /dev/sda3 && sudo swapon /dev/sda3; }

# mkswap 之后再写 fstab 行；使用设备路径，与 blkid 报告的分区一致
echo '/dev/sda3 none swap sw,nofail 0 0' | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload

# 验证
cat /proc/swaps
sudo blkid /dev/sda3
cat /etc/fstab
sudo findmnt --verify
systemctl is-active ops-spooler.service
cat /run/ops/spooler.starts
```
