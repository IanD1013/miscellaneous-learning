`MemoryHigh=` 和 `MemoryMax=` 都可以用来限制服务的内存用量，但当内存使用量攀升时，它们的行为有所不同。
`MemoryHigh=` 是一种节流（throttle）机制：
一旦服务的 cgroup 超过该值，内核就会对该 cgroup 的页面执行强制回收（reclaim）并减缓其进程运行速度，但不会终止任何进程。
`MemoryMax=` 则是硬性上限：
如果回收无法将使用量控制在其之下，OOM killer 就会杀死该 cgroup 内的一个进程。
当节流值设置在硬上限以下时，持续增长内存的服务会在其中的进程被杀死之前很久就变得迟缓。

systemd 会以字节（bytes）为单位将这两个值写入该 unit 的 cgroup 目录下的接口文件中，内核正是通过这些文件报告并强制执行 cgroup 设置的。
读取它们无需 `sudo`：

```bash
cat /sys/fs/cgroup/system.slice/ops-cache.service/memory.current
cat /sys/fs/cgroup/system.slice/ops-cache.service/memory.max
```

`memory.current` 是 cgroup 当前使用的字节数，对于 `ops-cache.service` 而言大约为 16 MB，该服务在 bash 变量中保存了一个 16 MB 的字符串（`memory.stat` 会细分具体数据；其中几乎全部为 `anon`）。
在启动构建该字符串期间，其峰值接近 32 MB。
`memory.max` 和 `memory.high` 会输出字面量 `max`，表示无限制。
无论 unit 文件写了什么，这些文件反映的都是内核当前实际应用的值。

### 应用并持久化这些限制

```bash
sudo systemctl set-property ops-cache.service MemoryHigh=48M MemoryMax=64M
```

`set-property` 会立即更改正在运行的 unit 的 cgroup。
对于由 unit 文件支持的 unit，它还会将每个属性作为单独的 drop-in 文件分别保存为 `/etc/systemd/system.control/ops-cache.service.d/` 下的 `50-MemoryHigh.conf` 和 `50-MemoryMax.conf`，其值会自动转换为字节，systemd 会在每次系统启动时读取它们。
加上 `--runtime` 参数后，它们会改存到 `/run/systemd/system.control/` 下，该目录在下次启动后会被清空。

如果你自己编写 drop-in 文件（例如在 `/etc/systemd/system/ops-cache.service.d/override.conf` 中的 `[Service]` 下配置 `MemoryHigh=48M` 和 `MemoryMax=64M`），在执行 `sudo systemctl daemon-reload` 之前不会发生任何更改。
在此 systemd 版本中，reload 本身就会将内存限制应用到正在运行的服务，因此无需重启服务。
systemd 会跨两个目录按照文件名顺序读取 unit 的 drop-in 文件，因此在 `override.conf` 中设置的限制优先级高于 `50-MemoryMax.conf` 或 `50-MemoryHigh.conf` 中的相同限制。

`K`、`M` 和 `G` 是 1024 的幂次方，因此 `64M` 表示 67108864 字节。
`64MB` 不是 systemd 能识别的后缀：
它会记录 `Invalid memory limit`，且 `memory.max` 仍会保持为 `max`。


限制 `ops-cache.service`，使其启动峰值保持在节流阈值之下：

- 服务运行时，`memory.high` 读取为 `50331648`（48 MiB），且 `memory.max` 读取为 `67108864`（64 MiB）。
- 两个限制都已持久化以供下次启动生效，可以通过不带 `--runtime` 的 `set-property`，或者在 `override.conf` 中使用 `M` 后缀或字节数来编写配置。
- `ops-cache.service` 保持 active 状态。

### 解答

```bash
# 立即应用并持久化两个限制（不带 --runtime，写入 /etc/systemd/system.control/）
sudo systemctl set-property ops-cache.service MemoryHigh=48M MemoryMax=64M

# 验证内核实际应用的值：应为 50331648 和 67108864
cat /sys/fs/cgroup/system.slice/ops-cache.service/memory.high
cat /sys/fs/cgroup/system.slice/ops-cache.service/memory.max

# 验证 drop-in 已写入磁盘，且服务仍为 active
ls /etc/systemd/system.control/ops-cache.service.d/
systemctl is-active ops-cache.service
```
