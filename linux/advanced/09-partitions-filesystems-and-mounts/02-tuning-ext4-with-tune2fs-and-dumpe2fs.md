ext4 文件系统将其设置保存在超级块（superblock）中，这是位于设备起始位置附近的一条小型记录，内核在每次挂载时都会读取它：UUID、标签（label）、块数量与大小、保留块、挂载次数、检查间隔以及特性标志（feature flags）。
`dumpe2fs -h` 会打印该记录，并跳过构成其其余输出的按块组（per-group）列表。
与 `tune2fs` 一样，它是需要使用 `sudo` 运行的 `/usr/sbin` 磁盘工具之一：

```text
$ sudo dumpe2fs -h /dev/sda1
dumpe2fs 1.47.0 (5-Feb-2023)
Filesystem volume name:   old-data
...
Mount count:              1
Maximum mount count:      -1
...
Check interval:           0 (<none>)
```

保留块（位于挂载计数稍上方的 `Reserved block count` 行）是为 root 保留的，除非在 `mkfs.ext4` 时另有指定，否则默认为 5%，这样当用户占满磁盘时，root 所属的服务仍能写入，并且你仍有空间进行清理。
小型数据卷很少需要 5%。
挂载次数在每次挂载时递增；一旦达到最大挂载次数，或者自上次检查起已超过检查间隔，启动时的 fsck 就会检查该文件系统，即使它被标记为 clean。
`-1` 和 `0` 会分别关闭这两项检查。

`tune2fs` 可以直接就地修改这些字段，因此文件系统上的任何文件都不会受到影响，也不会重新格式化任何内容。
`tune2fs -L ops-data /dev/sda1` 用于设置标签。
`tune2fs -m 1` 保留 1% 的块；`-r` 接受绝对块数，因此 `-r 1` 仅保留恰好一个块。
`tune2fs -c 20` 设置最大挂载次数，而 `-i 1m` 或 `-i 30d` 设置一个月的检查间隔。
多个选项可以合并在一条命令中执行。

所有这些操作都可以在文件系统处于挂载状态时执行，但存在一个注意事项：在已挂载的设备上，当 `-L` 与 `-m`、`-c` 或 `-i` 放在同一条命令中时，tune2fs 1.47.0 仅会应用标签修改，并且仍会以 0 退出，而不会指出跳过了哪些选项。
请将标签修改与其他字段修改分开在不同命令中执行，并在完成后使用 `dumpe2fs -h` 回读每个字段进行确认。

`/dev/disk/by-label` 是由 udev 构建的，而 udev 仅在发生 change 事件时才会重新读取设备的标签。
在未挂载状态下，`/dev/sda1` 会在 tune2fs 完成时接收到该事件。
但在已挂载状态下则不会，因此需要手动发送一个事件并等待 udev 处理完毕：

```bash
sudo udevadm trigger --action=change /dev/sda1 && sudo udevadm settle
```

### 需求

`/dev/sda1` 是一个 ext4 文件系统，标签为 `old-data`，挂载在 `/srv/ops/data`，且在 `/etc/fstab` 中没有对应条目。
其中包含 `inventory.csv` 和 `receipts/`。


- 标签为 `ops-data`，且 `ls /dev/disk/by-label` 能够列出它。
- 保留 1% 的块，最大挂载次数为 20，检查间隔为一个月。
- `/home/learner/ops/superblock.txt` 包含修改后 `dumpe2fs -h` 的 `Reserved block count`、`Maximum mount count` 和 `Check interval` 行。
  保存整个头部信息也可以。
- 最终，同一个文件系统在保持 `inventory.csv` 未被修改的情况下，仍挂载在 `/srv/ops/data`。
  如果调整参数时需要卸载，请确保随后重新挂载。

### 解答

```bash
# 标签单独修改（已挂载时不能与 -m/-c/-i 放在同一条命令里）
sudo tune2fs -L ops-data /dev/sda1

# 保留 1% 的块，最大挂载次数 20，检查间隔一个月
sudo tune2fs -m 1 -c 20 -i 1m /dev/sda1

# 已挂载的设备不会自动产生 change 事件，手动通知 udev 刷新 by-label
sudo udevadm trigger --action=change /dev/sda1 && sudo udevadm settle
ls /dev/disk/by-label

# 保存修改后的超级块头部信息
sudo dumpe2fs -h /dev/sda1 > /home/learner/ops/superblock.txt
grep -E '^(Filesystem volume name|Reserved block count|Maximum mount count|Check interval):' /home/learner/ops/superblock.txt

# 确认仍挂载在原处
findmnt /srv/ops/data
```
