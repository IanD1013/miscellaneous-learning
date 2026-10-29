`noexec`、`nosuid` 和 `nodev` 是按挂载点生效的选项（per-mount options）：它们属于文件系统的单次挂载，而不是属于其上的文件，并且内核会将它们应用于通过该挂载点进行的每一次访问。

- `noexec` 会使内核拒绝执行该挂载点上的任何文件，无论其权限位（mode bits）如何设置。
  这是一种防止运行存放在那里的恶意/未知文件的防护措施，而非万无一失的壁垒：`sh file` 仍能运行脚本，因为被执行的程序是来自根文件系统的 `sh`，而脚本只是其输入。
- `nosuid` 会忽略 setuid 和 setgid 位以及文件 capabilities，因此复制到那里的二进制文件无法以其所有者的特权运行。
- `nodev` 会忽略设备节点，因此在那里创建的设备文件无法绕过 `/dev` 上的权限来访问底层磁盘。

传递给 `mount -o` 的选项会随挂载的卸载而失效。
持久化的版本位于 `/etc/fstab` 行的第 4 字段，在其中靠后的选项优先（`defaults,noexec` 最终仍然生效 `noexec`），而 `nofail` 允许在缺少该磁盘时系统继续启动：

```text
UUID=... /srv/ops/uploads ext4 noexec,nosuid,nodev,nofail 0 2
```

在挂载之前使用 `sudo findmnt --verify` 检查该文件：它会解析每一行并检查每个源设备是否存在且类型与声明的一致。
如果不加 `sudo`，它将无法读取设备，并会用 "Permission denied" 警告掩盖真正的错误。
运行 `sudo systemctl daemon-reload` 使 systemd 生成的挂载单元与该文件保持同步，然后运行 `sudo mount /srv/ops/uploads`，该命令会从该行中获取设备和选项。
当前生效的挂载选项位于 `/proc/self/mountinfo` 中该挂载行的第 6 字段，按固定顺序排列（`rw` 或 `ro`、`nosuid`、`nodev`、`noexec`、`relatime`）；`findmnt -o TARGET,OPTIONS /srv/ops/uploads` 会打印该字段。

### 无需卸载即可设为只读

`umount` 会拒绝卸载繁忙的挂载点（包含某个进程的工作目录或处于打开状态的文件），并提示 `target is busy.`。

`sudo mount -o remount,ro /srv/ops/reports` 可以在原地更改现有挂载的标志：进程继续保留其目录和文件，但在写入时会收到 "Read-only file system"。
只有在该挂载点下有文件以写入模式打开时，remount 才会失败。

### 任务

`/dev/sda1` 是一个未挂载的 ext4 文件系统，标签为 `ops-uploads`，UUID 为 `b7e2a4d9-1c3f-4e8a-9b6d-5f0c2e7a1d48`（`sudo blkid /dev/sda1` 会打印它）。
`/dev/sda2` 以读写模式挂载在 `/srv/ops/reports`，但在 fstab 中没有对应行，且 `ops-reader.service` 正在其中运行。
使用 `sudo`：

- 在 `/etc/fstab` 中添加一行，通过该 UUID 将 `/srv/ops/uploads` 挂载为 `ext4`，带有 `noexec`、`nosuid`、`nodev` 和 `nofail` 选项，并将其挂载为读写模式，且这三个选项均已生效；
- 立即将 `/srv/ops/reports` 设置为只读，而无需停止或重启 `ops-reader.service`。
  读取程序每次启动时都会向 `/run/ops/reader-starts` 追加一行。
  读取程序当前正在其中工作的目录必须停止接受写入：在 `/srv/ops/reports` 上覆盖挂载一个只读文件系统会使读取程序仍保留在旧的读写挂载上，因此不计入完成；
- 保持 `host9p` 根目录行完全不变。

### 解答

```bash
# 确认 /dev/sda1 的 UUID
sudo blkid /dev/sda1

# 在 fstab 末尾追加 uploads 行（host9p 根目录行保持不变）
echo 'UUID=b7e2a4d9-1c3f-4e8a-9b6d-5f0c2e7a1d48 /srv/ops/uploads ext4 noexec,nosuid,nodev,nofail 0 2' | sudo tee -a /etc/fstab

# 挂载前检查 fstab，并让 systemd 同步生成的挂载单元
sudo findmnt --verify
sudo systemctl daemon-reload

# 按 fstab 行挂载（默认读写），确认 rw,nosuid,nodev,noexec 均已生效
sudo mkdir -p /srv/ops/uploads
sudo mount /srv/ops/uploads
findmnt -o TARGET,OPTIONS /srv/ops/uploads

# 原地把正在使用的 reports 挂载改为只读，不停止 ops-reader.service
sudo mount -o remount,ro /srv/ops/reports
findmnt -o TARGET,OPTIONS /srv/ops/reports

# 确认读取程序没有被重启
cat /run/ops/reader-starts
```
