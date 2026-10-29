`mkswap` 通过在块设备的开头写入 swap 签名（一个包含全新随机 UUID 的单页头部）来将其转换为 swap。
分区表无法替你完成这一步。
这里的 `/dev/sda2` 已经具有 GPT 类型 Linux swap 以及分区名 `swap`，但在运行 `mkswap` 之前，`lsblk -o NAME,PARTLABEL,FSTYPE /dev/sda` 不会为其显示任何 `FSTYPE`。

随后，`swapon` 可以立即将该区域移交给内核，无需重启系统，而 `swapoff` 则会将其收回：

```bash
sudo mkswap /dev/sda2
sudo swapon -p 10 /dev/sda2
cat /proc/swaps
```

`/proc/swaps` 列出了每个活动区域及其类型、大小、以 KiB 为单位的使用量以及优先级。
内核会将页面放入有剩余空间且优先级最高的区域中，并在具有相同优先级的区域之间分散分配。
`-p` 用于在启用时设置该优先级数值。
若省略该参数，内核会自行对区域编号，按照这些区域启用的顺序从 -2 开始递减（先是 -2，然后是 -3），而无论其他区域具有何种优先级。
这容易让人误以为启用顺序才是规则，但实际上起决定作用的是优先级。

### Swap 文件

内核会将 swap 页面直接写入 swap 文件底层的磁盘块，从而绕过文件系统，因此该文件必须位于能够报告这些块的文件系统上，并且在启用之前每个块都必须存在。
挂载在 `/srv/ops/data` 上的 `/dev/sda1` 处的 ext4 文件系统符合要求。
这台虚拟机的根文件系统（包含 `/home`）没有可报告的块，因此 `swapon` 会拒绝那里的文件并提示 `swapon failed: Invalid argument`。

使用从 `/dev/zero` 读取的 `dd` 命令可以写入每一个块（在当前 ext4 上 `fallocate -l 16M` 同样有效）：

```bash
sudo dd if=/dev/zero of=/srv/ops/data/swapfile bs=1M count=16
sudo chmod 600 /srv/ops/data/swapfile
sudo mkswap /srv/ops/data/swapfile
```

使用 `sudo` 创建的文件属于 root。
由于它将保存系统中每个进程的内存页面，因此请赋予其 0600 权限模式；若为 0644，`mkswap` 和 `swapon` 都会打印不安全权限警告，但仍会继续执行。

为了在开机时挂载，每个区域都需要在 `/etc/fstab` 中添加一行，挂载点为 `none`，类型为 `swap`，选项为 `sw,pri=` 加数字，并像所有临时磁盘条目一样加上 `nofail`：

```text
UUID=... none swap sw,pri=10,nofail 0 0
```

可以通过 `UUID=`（使用 `sudo blkid /dev/sda2` 读取）、`PARTUUID=`、`PARTLABEL=swap` 或 `/dev/sda2` 指定分区，通过完整路径指定文件。
`sudo swapon -a` 会以各自的 `pri=` 激活 `/etc/fstab` 中尚未激活的每个 swap 条目，这也使其成为检验你所编写条目是否正确的方法。

### 要求

- `/dev/sda2` 包含 swap 签名，并且是优先级为 10 的活动 swap。
- `/srv/ops/data/swapfile` 是一个属主为 root、权限模式为 0600 的 16 MiB 文件，且作为优先级为 5 的 swap 处于活动状态。
- `/etc/fstab` 保留现有行（根文件系统和 `LABEL=ops-data` 条目），并为每个区域新增一行 swap 条目：分区使用 `pri=10`，通过其设备路径或当前 `sudo blkid /dev/sda2` 所报告的值进行指定；文件使用 `pri=5`，两者均包含 `nofail`。

### 解答

```bash
# 在分区上写入 swap 签名并以优先级 10 启用
sudo mkswap /dev/sda2
sudo swapon -p 10 /dev/sda2

# 在 /dev/sda1 的 ext4 上创建 16 MiB、root 所有、0600 的 swap 文件并以优先级 5 启用
sudo dd if=/dev/zero of=/srv/ops/data/swapfile bs=1M count=16
sudo chmod 600 /srv/ops/data/swapfile
sudo mkswap /srv/ops/data/swapfile
sudo swapon -p 5 /srv/ops/data/swapfile

# 在 fstab 末尾追加两条 swap 条目（保留现有行）
echo '/dev/sda2 none swap sw,pri=10,nofail 0 0' | sudo tee -a /etc/fstab
echo '/srv/ops/data/swapfile none swap sw,pri=5,nofail 0 0' | sudo tee -a /etc/fstab

# 检验条目：已激活的区域会被跳过，不应报错
sudo swapon -a
cat /proc/swaps
ls -l /srv/ops/data/swapfile
```
