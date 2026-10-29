`.mount` unit 以类似 fstab 行的方式描述一个挂载，每个字段都在 `[Mount]` 小节中进行命名。
以下是这台机器 fstab 中已有的归档条目 `LABEL=ops-archive /srv/ops/archive ext4 defaults,nofail 0 2`，重写为符合本任务要求的 unit 形式：使用 `nodev,noatime` 替换 `defaults,nofail`。

最后两个字段（dump 标志和 fsck pass 序号）在 `[Mount]` 中没有对应的项。
基于 pass `2`，fstab 生成器会使挂载首先依赖对设备的 `systemd-fsck@` 检查，因此与它替换的行不同，该 unit 在开机引导时不会执行文件系统检查。
该检查是此 unit 放弃的唯一依赖：由于示例下方说明的原因，它仍然会等待对应的磁盘。

```ini
[Unit]
Description=Ops archive filesystem

[Mount]
What=/dev/disk/by-label/ops-archive
Where=/srv/ops/archive
Type=ext4
Options=nodev,noatime

[Install]
WantedBy=multi-user.target
```

`What=` 是设备。
在 unit 文件中，请将其指定为 `/dev` 下的路径，例如 `/dev/disk/by-label/ops-archive`（指向标签为 `ops-archive` 的分区的链接）：在此 systemd 版本（252，Debian 12 附带的版本）上，仅当 `What=` 为设备路径时，挂载才会在开机引导时等待其设备，并且只有 fstab 生成器才会将 `LABEL=` 或 `UUID=` 转换为设备路径。
因此，带有 `What=LABEL=ops-archive` 的 unit 在你手动启动时可以挂载，但开机时不会等待磁盘就绪。
较新的 systemd 版本也会在 unit 文件中转换这些形式；而设备路径在所有版本中均可使用。
`Where=` 是挂载点，`Type=` 和 `Options=` 承载 fstab 的第三和第四个字段。
`noatime` 可阻止读取操作将访问时间写回磁盘。

### 文件名来源于 Where=

systemd 仅在 mount unit 的名称与其 `Where=` 路径经过 unit 名称转义后的结果一致时才接受它：开头的 `/` 被移除，其他斜杠变为短横线，其他任何特殊字符均被转义。
这与 `systemd-escape` 应用于实例名称的规则相同，因此可以让它来完成这项工作：

```text
$ systemd-escape -p --suffix=mount /srv/ops/archive
srv-ops-archive.mount
```

如果将相同的内容保存为 `archive.mount`，运行 `sudo systemctl start archive.mount` 会失败并报错 `Unit archive.mount has a bad unit file setting.`，同时 journal 会记录 `Where= setting doesn't match unit name. Refusing.`。


你的 fstab 行其实已经是这种类型的 unit。
在开机引导以及每次执行 `daemon-reload` 时，fstab 生成器（`systemd-fstab-generator`）都会为每行向 `/run/systemd/generator/` 中写入一个 unit，这也是为什么现在运行 `systemctl status srv-ops-archive.mount` 有效并显示 `Loaded: loaded (/etc/fstab; generated)` 的原因。

删除该行并重载不会卸载任何内容。
文件系统仍保持其原有的 `rw,relatime` 挂载状态，并且启动一个路径已处于挂载状态的 mount unit 也不会改变任何东西，因此单独执行 `enable --now` 仍会保留旧的选项。
在启动该 unit 之前运行 `sudo umount /srv/ops/archive`，或者在启动后运行 `sudo systemctl restart srv-ops-archive.mount`。

启动仅在本次开机运行期间挂载它；启用（enable）则会添加 `multi-user.target.wants` 链接，以便在下次开机时自动挂载。

### 设置大小上限的 tmpfs

`tmpfs` 是一种内存支持的文件系统：其文件驻留在 RAM 中，并在卸载时消失。
如果没有 `size=` 选项，它可能会增长到内核报告内存的一半，而此虚拟机上未设置大小的 tmpfs 在 `df -h` 中会显示 `115M`，足以让一个失控的写入进程挤压所有其他进程。
`size=16M` 设置了上限，超出此上限的写入操作将失败并提示 `No space left on device`。

tmpfs 背后没有对应的物理设备，因此 `What=tmpfs` 仅是一个标签，`Type=tmpfs` 用于选择该文件系统。
`Options=size=16M,mode=1777` 还会赋予挂载根目录类似于 `/tmp` 的全局可写及 sticky 权限。

### 要求

此处的所有更改都需要 `sudo`。

使用 `sudo tee` 写入 unit 文件，并在写入或修改后运行 `sudo systemctl daemon-reload`。


- `/etc/fstab` 移除 `LABEL=ops-archive` 行，仅保留原有的 `host9p` 根条目，保持不变。
- `/etc/systemd/system/srv-ops-archive.mount` 将 `ops-archive` 文件系统以 ext4 挂载至 `/srv/ops/archive`，配置必须完全为 `Options=nodev,noatime`，其 `What=` 为设备路径（如 `/dev/disk/by-label/ops-archive`）而非 `LABEL=`。
- `/etc/systemd/system/srv-ops-scratch.mount` 将 tmpfs 挂载至 `/srv/ops/scratch`，并带有 `Options=size=16M,mode=1777`。
- 两个 unit 都在这台机器开机启动时能够到达的 target 下启用（enabled），以便在下次开机时再次挂载，并且现在已使用新选项完成挂载。`findmnt` 可显示该结果，并且在归档重新挂载后 `/srv/ops/archive/index.txt` 会再次恢复可见。

### 解答

```bash
# 从 fstab 删除归档行，只保留 host9p 根条目
sudo sed -i '/^LABEL=ops-archive[[:space:]]/d' /etc/fstab
cat /etc/fstab

# 归档的 mount unit（文件名必须与 Where= 转义结果一致）
sudo tee /etc/systemd/system/srv-ops-archive.mount <<'EOF'
[Unit]
Description=Ops archive filesystem

[Mount]
What=/dev/disk/by-label/ops-archive
Where=/srv/ops/archive
Type=ext4
Options=nodev,noatime

[Install]
WantedBy=multi-user.target
EOF

# 限制大小为 16M 的 tmpfs mount unit
sudo tee /etc/systemd/system/srv-ops-scratch.mount <<'EOF'
[Unit]
Description=Ops scratch tmpfs

[Mount]
What=tmpfs
Where=/srv/ops/scratch
Type=tmpfs
Options=size=16M,mode=1777

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

# 确认开机默认 target 会拉起 multi-user.target
systemctl get-default

# 先卸载旧的 rw,relatime 挂载，再启用并立即以新选项挂载
sudo umount /srv/ops/archive
sudo systemctl enable --now srv-ops-archive.mount srv-ops-scratch.mount

# 检查结果
findmnt /srv/ops/archive
findmnt /srv/ops/scratch
ls /srv/ops/archive/index.txt
```
