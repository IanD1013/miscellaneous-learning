`ops-render.service` 和 `ops-archive.service` 是与其他所有服务一同运行在 `system.slice` 中的批处理任务，因此当 CPU 繁忙时，它们中的每一个都会与其他服务平等竞争资源。
**slice** 是一种仅作为 cgroup 树中节点的 systemd unit：
服务置于其中，并且 slice 上的资源设置会作为一个整体应用到其中的所有内容。

### slice 所在的位置

Slice 的名称使用连字符（dash）表示嵌套层级：
每个连字符代表在树中向下深入一层。
`ops-batch.slice` 是 `ops.slice` 的 `batch` 子节点，因此它的 cgroup 路径是 `/sys/fs/cgroup/ops.slice/ops-batch.slice`，并且 systemd 会隐式创建 `ops.slice`。

没有连字符的名称（例如 `opsbatch.slice`）则直接位于根节点下，与 `system.slice` 和 `user.slice` 并列。

slice unit 文件只需要包含带有其配置设置的 `[Slice]` 节。
以下是 `/etc/systemd/system/opsbatch.slice`：

```ini
[Slice]
CPUWeight=20
```

服务通过在 `[Service]` 中指定 `Slice=` 来加入该 slice，这里可以通过 drop-in 文件实现，例如 `/etc/systemd/system/ops-render.service.d/override.conf`：

```ini
[Service]
Slice=opsbatch.slice
```

在执行 `sudo systemctl daemon-reload` 之后，`systemctl show -p Slice ops-render.service` 已经会报告 `Slice=opsbatch.slice` 并且该 slice 的目录也会出现，但 `/proc/<PID>/cgroup` 仍显示为 `0::/system.slice/ops-render.service`。

systemd 仅在启动服务进程时对其进行归类定位，因此它们只有在重启后才会移动。

### weight 的作用

`CPUWeight=` 的取值范围为 1 到 10000，默认值为 100，并会写入该 group 的 `cpu.weight` 文件中。
只有当 systemd 为该 group 开启 CPU controller 时，该文件才会存在；当 slice 或其内部的 unit 设置了 weight 时，systemd 就会开启它。
如果没有任何地方设置 weight，即使两个服务都在其中，`cat /sys/fs/cgroup/opsbatch.slice/cpu.weight` 也会报错 `No such file or directory`。

内核仅在发生资源争用（即处于可运行状态的任务所需时间超过 CPU 时间）时才会应用 weight，且仅在同级（即具有相同父节点的 cgroup）之间生效。
如果权重为 20 的 `opsbatch.slice` 和权重为 100 的 `system.slice` 都处于繁忙状态，该批处理 slice 将获得六分之一的 CPU 资源。
而在空闲机器上，它仍然可以获取全部 CPU 资源：
weight 是一种配额比例（share），绝非资源上限（ceiling）。

weight 所处的位置决定了它与谁竞争。
如果在没有 slice 的情况下在每个服务上设置 `CPUWeight=20`，它们仍会保留在 `system.slice` 中，各自与其他所有系统服务进行竞争。
而在 `opsbatch.slice` 上设置时，这两个服务将作为一个整体与 `system.slice` 和 `user.slice` 竞争。
在 `ops-batch.slice` 上设置 weight 则仅会在 `ops.slice` 的子节点之间分配时间，而 `ops.slice` 本身仍然与权重为 100 的 `system.slice` 进行竞争。

### 任务

在 `/etc/systemd/system` 下写入、执行 `daemon-reload` 和 `restart` 需要 `sudo`。


- 在 cgroup 根目录下直接创建 `opsbatch.slice`，并在该 slice 上设置 `CPUWeight=20`，以便 `cat /sys/fs/cgroup/opsbatch.slice/cpu.weight` 输出 `20`。
- 使用 drop-in 文件（通过 `sudo systemctl edit` 或自行编写文件）将 `ops-render.service` 和 `ops-archive.service` 移动到其中。
- 保持两个服务均处于 active 状态，且各自在 `/sys/fs/cgroup/opsbatch.slice/` 下拥有独立的目录。
- 保存这两项更改，使其在系统重启后仍然有效：它们必须保存在 `/run` 之外的文件中（系统重启会清空 `/run`），因此在使用 `systemctl edit` 和 `systemctl set-property` 时不要带上 `--runtime` 参数。

### 解答

```bash
# 创建位于 cgroup 根目录下的 slice（名称不含连字符），并设置 CPUWeight=20
sudo tee /etc/systemd/system/opsbatch.slice <<'EOF'
[Slice]
CPUWeight=20
EOF

# 用 drop-in 把两个服务移入该 slice
for svc in ops-render ops-archive; do
  sudo mkdir -p /etc/systemd/system/$svc.service.d
  printf '[Service]\nSlice=opsbatch.slice\n' | sudo tee /etc/systemd/system/$svc.service.d/override.conf
done

# 重新加载并重启服务，让进程真正移动到新 slice
sudo systemctl daemon-reload
sudo systemctl restart ops-render.service ops-archive.service

# 验证：weight 为 20，两个服务各有目录且为 active
cat /sys/fs/cgroup/opsbatch.slice/cpu.weight
ls -d /sys/fs/cgroup/opsbatch.slice/*.service
systemctl is-active ops-render.service ops-archive.service
```
