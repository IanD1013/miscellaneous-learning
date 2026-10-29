`/srv/ops/archive` 的 fstab 行通过 UUID 指定其文件系统，而该 UUID 存储在 ext4 超级块（superblock）中，即 `dumpe2fs -h` 所打印的头部信息。
在 `/dev/sda1` 上，超级块已被清零，因此系统上不再有任何设备带有该 UUID。
`sudo mount /srv/ops/archive` 和 `sudo mount -a` 都不会输出任何内容并以 0 退出，因为 `nofail` 会将缺失的设备转为静默跳过，且 `findmnt /srv/ops/archive` 显示没有任何挂载。
指定设备名称后，真正的错误就会出现，退出状态码为 32：

```console
$ sudo mount /dev/sda1 /srv/ops/archive
mount: /srv/ops/archive: wrong fs type, bad option, bad superblock on /dev/sda1, missing codepage or helper program, or other error.
```

文件仍保存在磁盘上，超级块的备用副本也是如此。
ext4 将文件系统划分为块组（block group），并在组 1 以及组号为 3、5 或 7 的幂的每个组的开头写入一个备份超级块。
每个组从哪里开始取决于块大小。
若使用 4 KiB 块，一个组长度为 32768 个块，组 0 从块 0 开始，因此组 1 从块 32768 开始，组 3 从块 98304 开始。
若使用 1 KiB 块，一个组长度为 8192 个块，组 0 从块 1 开始，因为主超级块位于设备内 1024 字节处，因此每个组的起始位置都会向上移动一个块。
文件系统的大小决定了它拥有多少个组，从而决定了它实际使用其中的哪些位置。

常规的 e2fsck 仅使用其中的一部分：

```console
$ sudo e2fsck -f -y /dev/sda1
e2fsck 1.47.0 (5-Feb-2023)
ext2fs_open2: Bad magic number in super-block
e2fsck: Superblock invalid, trying backup blocks...
e2fsck: Bad magic number in super-block while trying to open /dev/sda1
...
    e2fsck -b 8193 <device>
 or
    e2fsck -b 32768 <device>
```

当主超级块不可读时，e2fsck 仅回退到每种块大小的第一个备份位置：1 KiB 为 8193，2 KiB 为 16384，4 KiB 为 32768。
在这里该回退也失败了，因此 e2fsck 以退出状态码 8 放弃且未写入任何内容。
末尾的两条建议是通用的首个备份位置，对每个磁盘打印的内容都相同；它们并不是该文件系统副本的列表。

通过试运行（dry run）获取磁盘本身的列表。
`mke2fs -n` 会计算出格式化该设备所创建的布局并将其打印出来，而不会写入任何字节；若去掉 `-n`，相同的命令将格式化设备，从而摧毁你要挽救的数据。
`-b` 指定块大小。
若不带该参数，mke2fs 会根据设备大小从 `/etc/mke2fs.conf` 中选取大小：通常为 4096，对于小于 512 MiB 时使用的 `small` 类型则为 1024，这也是未指定 `-b` 格式化的文件系统获取其块大小的方式。
对于使用 4 KiB 块的 1 GiB 镜像文件：

```console
$ sudo mke2fs -n -b 4096 /tmp/demo.img
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 262144 4k blocks and 65536 inodes
Filesystem UUID: b5e166ee-18d1-451e-a592-217513d2d791
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376
```

262144 个块构成了 8 个大小为 32768 的组，副本位于组 1、3、5 和 7 的开头。
这里的 UUID 是 mke2fs 原本会使用的随机 UUID，而不是从设备中读取的。
错误的块大小会移动每个位置，因此该列表仅对文件系统实际具有的块大小有效。

`e2fsck -b` 指定从中开始恢复的副本。
`sudo e2fsck -f -y -b BLOCK -B SIZE DEVICE` 会读取存储在块 BLOCK 处的超级块，其中 `-B` 指定块大小，以使块编号指向磁盘上的正确位置。
随后它会检查整个文件系统（`-f` 强制执行完整检查，`-y` 对所有修复回答 yes）并写入修复后的主超级块。
如果不带 `-B`，e2fsck 会自行尝试各种块大小；错误的 `-B` 会失败。
仅在未挂载的文件系统上运行它。
退出状态码会报告结果：0 表示干净，1 表示错误已更正，4 表示仍有错误未更正，8 表示无法打开文件系统且未写入任何内容。
只有主超级块会被重写；已损坏的备份副本仍会保持损坏。

### 修复归档

找出此分区上幸存的副本，并从中恢复文件系统，切勿格式化。
该归档是用 mke2fs 为其分区默认选取的块大小进行格式化的，`lsblk /dev/sda1` 显示了该分区的大小。
mke2fs、e2fsck 和 blkid 都是位于 `/usr/sbin` 中需要使用 `sudo` 运行的磁盘工具，mount 同样需要 root 权限。
修复完成后，systemd 不会自动启动由 fstab 生成的 `srv-ops-archive.mount`；请通过现有的 fstab 行使用 `sudo mount /srv/ops/archive` 或 `sudo mount -a` 进行挂载。
完成意味着修复已写入磁盘，因此 `sudo blkid /dev/sda1` 再次报告 `TYPE="ext4"` 和该归档的 UUID；`/srv/ops/archive` 已作为 ext4 挂载；且 `/srv/ops/archive/manifest.txt` 仍保留其原本的 5 行内容，开头为 `archive-set: 2026-q3-closing`。

重新格式化同样可以挂载，但不会有该文件。

### 解答

```bash
# 查看分区大小（小于 512 MiB 时 mke2fs 默认使用 1 KiB 块）
lsblk /dev/sda1

# 试运行（-n 绝不写入），按默认块大小列出该分区的备份超级块位置
sudo mke2fs -n -t ext4 /dev/sda1

# 从试运行输出中提取块大小（字节）和备份超级块列表
bs=$(( $(sudo mke2fs -n -t ext4 /dev/sda1 | sed -n 's/^Creating filesystem with [0-9]* \([0-9]*\)k blocks.*/\1/p') * 1024 ))
backups=$(sudo mke2fs -n -t ext4 /dev/sda1 | sed -n '/^Superblock backups/,/^$/{/^\t/p}' | tr ',' ' ')
echo "block size: $bs, backups: $backups"

# 依次尝试每个备份副本，直到 e2fsck 以 0（干净）或 1（已更正）退出
for b in $backups; do
  sudo e2fsck -f -y -b "$b" -B "$bs" /dev/sda1
  rc=$?
  echo "backup $b -> exit $rc"
  [ "$rc" -le 1 ] && break
done

# 确认主超级块已恢复：TYPE="ext4" 和原来的 UUID
sudo blkid /dev/sda1

# 通过现有 fstab 行挂载并检查文件
sudo mount /srv/ops/archive
findmnt /srv/ops/archive
cat /srv/ops/archive/manifest.txt
```
