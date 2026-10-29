`sfdisk` 是你所熟知的 `fdisk` 的可脚本化版本：它通过标准输入以文本形式读取整个分区表并一次性写入，因此磁盘布局就变成了一个你可以审查、应用并保留的文件。
在这里，它将临时磁盘 `/dev/sda`（64 MiB，一个 63 MiB 的分区）上旧的 dos 分区表替换为 GPT。

### GPT 条目

GPT 是取代 MBR 的分区表格式，`sfdisk` 将 MBR 称为 `dos`。

它在磁盘末尾保留了一个备份头部。
默认情况下，其分区条目数组有 128 个槽位；该大小在创建分区表时设定，而在 sfdisk 脚本头部添加 `table-length: 256` 行则会为新表分配 256 个槽位。
除了起始位置和大小之外，每个条目还包含：

- 一个说明分区用途的类型 GUID：`0FC63DAF-8483-4772-8E79-3D69D8477DE4` 表示 Linux filesystem，`0657FD6D-A4AB-43C4-84E5-0933C84B4F4F` 表示 Linux swap。
  你在分区时对其进行选择；之后使用 `mkfs.ext4` 或其他工具格式化分区绝不会改变它。
- 一个为此条目生成的 PARTUUID。
  它存在于分区表中，因此重新格式化分区仍会保留它，并且 fstab 行可以通过 `PARTUUID=` 来指定分区。
- 一个可选的分区名称，例如 `data`。

udev 会将这些信息复制到其设备数据库中，这也是 `lsblk` 读取其 `PARTTYPENAME` 和 `PARTLABEL` 列的地方。

### 脚本与转储

一个 sfdisk 脚本由头部行以及按顺序每行一个分区组成：

```text
label: gpt
size=24MiB, type=L, name=data
```

`label: gpt` 将新分区表设为 GPT。
`size=` 接受类似 `MiB` 的单位；纯数字则表示 512 字节的扇区数。
`type=` 接受别名 `L`（Linux filesystem）、`S`（Linux swap）或完整的类型 GUID。
没有 `size=` 的行将占用磁盘的剩余空间。

sfdisk 位于 `/usr/sbin` 中，本章后续用于对磁盘进行格式化、调整、检查和设置 swap 的工具也是如此。
该目录不在你的 `PATH` 中，因此直接运行 `sfdisk` 会输出 `command not found`；请使用 `sudo` 运行其中的每一个工具，`sudo` 会在 `/usr/sbin` 中进行搜索。
此处的 `/sbin` 是指向 `/usr/sbin` 的链接，因此 `/sbin/sfdisk` 是同一个文件。
`lsblk` 位于 `/usr/bin` 中，可以以你当前的身份运行。

sfdisk 会在不进行询问的情况下覆盖现有分区表，然后通知内核重新读取它：

```bash
sudo sfdisk /dev/sda < /home/learner/ops/sda.layout
```

`sudo sfdisk --dump /dev/sda` 以完全相同的格式输出当前的分区表，并列出每一个具体值：

```text
label: gpt
label-id: 379CF8C8-1756-7949-AE3B-8248C6237D7E
...
/dev/sda1 : start=        2048, size=       49152, type=0FC63DAF-8483-4772-8E79-3D69D8477DE4, uuid=4ABF0C99-4D89-B445-AF2B-6AFA94BDFA07, name="data"
```

因为它是一个脚本，所以将保存的 dump 重新输入给 `sfdisk` 可以完全重建该分区表，包括 PARTUUID。
若要就地修改某个条目，`--part-type` 和 `--part-label` 接受磁盘、分区号以及新值：`sudo sfdisk --part-label /dev/sda 3 logs`。


### 要求

- `/dev/sda` 拥有一个 GPT 分区表，按顺序依次为：24 MiB（49152 个扇区）的 Linux filesystem，命名为 `data`；16 MiB（32768 个扇区）的 Linux swap，命名为 `swap`；磁盘的剩余空间（sfdisk 对齐其末尾后为 45056 个扇区），Linux filesystem，命名为 `logs`。
- `/home/learner/ops/sda.sfdisk` 保存该新分区表的 `sfdisk --dump` 输出。

`lsblk -o NAME,SIZE,PARTTYPENAME,PARTLABEL /dev/sda` 可用于查看结果。

### 解答

```bash
# 编写 GPT 布局脚本：data 24MiB，swap 16MiB，logs 占用剩余空间
mkdir -p /home/learner/ops
cat > /home/learner/ops/sda.layout <<'EOF'
label: gpt
size=24MiB, type=L, name=data
size=16MiB, type=S, name=swap
type=L, name=logs
EOF

# 一次性写入新的分区表
sudo sfdisk /dev/sda < /home/learner/ops/sda.layout

# 保存新分区表的 dump
sudo sfdisk --dump /dev/sda > /home/learner/ops/sda.sfdisk

# 查看结果
lsblk -o NAME,SIZE,PARTTYPENAME,PARTLABEL /dev/sda
cat /home/learner/ops/sda.sfdisk
```
