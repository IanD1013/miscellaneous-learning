`ops-ledger.service` 无法启动，而使其启动只是修复工作的一部分。
它必须在沙箱完好无损且具有实际内存限制的情况下恢复运行，并按照打包 unit 的方式进行修复。
在更改任何内容之前，请先从故障排查入手，从 systemd 和 journal 中收集证据：
该 unit 存在四个独立的故障，每个故障表现在不同的地方，其中一个只有在服务运行后才会显现。

```console
$ systemctl status --no-pager ops-ledger.service
× ops-ledger.service - Ops ledger worker
     Loaded: loaded (/run/systemd/system/ops-ledger.service; disabled; preset: enabled)
     Active: failed (Result: resources)
```

在这台虚拟机上，每次读取 journal 都需要 `sudo`。


### 服务的预期运行方式

- 厂商 unit 为 `/usr/lib/systemd/system/ops-ledger.service`。
  它在 `ProtectSystem=strict` 下运行 `/usr/local/lib/ops/ledger-worker`，并带有一个站点计划添加的例外：
  保持 `/srv/ops/ledger/data` 可写。
- worker 从 `/etc/ops/ledger.env` 读取 `LEDGER_DATA`。
  `/etc/ops/ledger.local.env` 用于特定主机的覆盖配置，而此主机没有该配置。
- worker 每 3 秒尝试写入 `/etc/ops` 以及其数据目录之外的 `/srv/ops/ledger`，并将结果记录在 `/srv/ops/ledger/data/access` 中。
  然后它会作为子进程运行其打包辅助程序 `/usr/local/lib/ops/ledger-pack`，并且仅当该辅助程序以状态码 0 退出时，才会写入 `/srv/ops/ledger/data/heartbeat`。
  worker 每次启动时都会删除心跳文件，因此在重启后请等待几秒钟。

在该镜像上，`/lib` 与 `/usr/lib` 是同一个目录，因此报告在 `/lib/systemd/system` 下的路径即为厂商文件。

### 要求达到的最终状态

- `ops-ledger.service` 处于 active 状态，且 `/srv/ops/ledger/data/heartbeat` 存在。
- `/srv/ops/ledger/data/access` 的内容必须恰好是 `etc=denied` 然后是 `srv=denied`，每行一个。
  这两次写入仅是对沙箱的抽样检验，因此 `systemctl show -p ProtectSystem ops-ledger.service` 必须仍报告 `strict`，并且数据目录之所以可写，是因为 systemd 为该 unit 加载了 `ReadWritePaths=/srv/ops/ledger/data`（`systemctl show -p ReadWritePaths`），且未开放其他任何路径的写入权限。
  更低的级别是不够的：
  `ProtectSystem=full` 会使 `/srv` 和 `/var` 保持可写。
  正在运行的进程也必须具备该沙箱：
  systemd 仅在服务启动时应用沙箱设置，因此在任何更改了沙箱设置的 `daemon-reload` 之后都必须重启服务。
- `systemctl show -p MemoryMax ops-ledger.service` 报告 32M 到 64M（含两端），且运行中服务的 `memory.max` 读取值与之一致，介于 33554432 和 67108864 之间。
  手动写入 `memory.max` 只会改变当前运行实例：
  下次重启将应用 systemd 保存的配置。
  请根据 worker 的实际使用情况设定限制；`infinity` 只是测量的一种手段，绝不能作为最终值。
- systemd 从 `/usr/lib/systemd/system/ops-ledger.service` 运行该 unit（`systemctl show -p FragmentPath`），且该文件逐字节保持未修改；`/run/systemd/system/ops-ledger.service` 已被移除，并且在 systemd 优先于 `/usr/lib/systemd/system` 搜索的任何 unit 目录（例如 `/etc/systemd/system` 或 `/usr/local/lib/systemd/system`）中均不存在其他完整的 `ops-ledger.service` 文件。
  对该 unit 的所有更改都必须放入 drop-in 中，使用 `systemctl set-property` 也算，因为它会写入 drop-in。
- 修复在重启后依然有效。
  `/run` 在开机时为空，因此该 unit 的 drop-in 不能存放在此处，这排除了 `set-property --runtime`；且 systemd 使用的每个 drop-in 在磁盘上依然存在。
  `systemctl show -p NeedDaemonReload ops-ledger.service` 还必须报告 `no`：
  systemd 已加载磁盘上当前状态的所有 unit 文件和 drop-in。
- `/etc/ops/ledger.local.env` 依然不存在，且下次启动在没有它的情况下也能成功：
  `systemctl show -p EnvironmentFiles ops-ledger.service` 依然列出 `/etc/ops/ledger.env`，并且标记为 `ignore_errors=no` 的每个文件均存在。
  该 unit 必须能够在没有任何本地覆盖的主机上启动，因此创建该文件（即使是空文件或仅用于单次重启）都不算作修复。

一旦运行了 `set-property`，每次重启都会打印一条警告，提示该 unit 在磁盘上已更改并建议执行 `daemon-reload`，且 `NeedDaemonReload` 会一直保持为 `yes`，直到执行 `sudo systemctl daemon-reload` 清除这两者。
`set-property` 写入的值已经应用于运行中的服务，因此该警告并不意味着更改失败，但在判定修复完成之前请务必执行该重载。

### 解答

```bash
# 排查：查看 systemd 实际加载的所有 unit 文件和 drop-in
systemctl status --no-pager ops-ledger.service
systemctl cat ops-ledger.service
systemd-delta --type=overridden,extended | grep ops-ledger
systemctl show -p FragmentPath,DropInPaths,EnvironmentFiles,ProtectSystem,ReadWritePaths,MemoryMax ops-ledger.service
sudo journalctl -u ops-ledger.service -b --no-pager -n 50

# 移除所有遮蔽厂商 unit 的完整副本，以及存放在 /run 中（重启即丢失）的 drop-in
sudo rm -f /run/systemd/system/ops-ledger.service /etc/systemd/system/ops-ledger.service /usr/local/lib/systemd/system/ops-ledger.service
sudo rm -rf /run/systemd/system/ops-ledger.service.d /run/systemd/system.control/ops-ledger.service.d

# 写入持久 drop-in；文件名以 zz 开头，在所有目录的 drop-in 中最后应用
sudo mkdir -p /etc/systemd/system/ops-ledger.service.d
sudo tee /etc/systemd/system/ops-ledger.service.d/zz-ops-fix.conf >/dev/null <<'EOF'
[Service]
# 沙箱保持 strict，只开放数据目录（先清空列表再添加）
ProtectSystem=strict
ReadWritePaths=
ReadWritePaths=/srv/ops/ledger/data
# 本地覆盖文件可选：清空列表后重新加入，local.env 前加 - 表示缺失时忽略
EnvironmentFile=
EnvironmentFile=/etc/ops/ledger.env
EnvironmentFile=-/etc/ops/ledger.local.env
# 先不限制内存，用于测量 worker 及其子进程的实际用量
MemoryMax=infinity
EOF
sudo systemctl daemon-reload
sudo systemctl restart ops-ledger.service

# 测量：等待几轮循环后查看内存峰值
sleep 10
systemctl show -p MemoryCurrent,MemoryPeak ops-ledger.service

# 按测量结果设定 32M 到 64M 之间的最终限制
sudo tee /etc/systemd/system/ops-ledger.service.d/zz-ops-fix.conf >/dev/null <<'EOF'
[Service]
# 沙箱保持 strict，只开放数据目录（先清空列表再添加）
ProtectSystem=strict
ReadWritePaths=
ReadWritePaths=/srv/ops/ledger/data
# 本地覆盖文件可选：清空列表后重新加入，local.env 前加 - 表示缺失时忽略
EnvironmentFile=
EnvironmentFile=/etc/ops/ledger.env
EnvironmentFile=-/etc/ops/ledger.local.env
# 根据实测峰值设定的内存上限
MemoryMax=64M
EOF
sudo systemctl daemon-reload
sudo systemctl restart ops-ledger.service

# 验证
sleep 8
systemctl is-active ops-ledger.service
ls -l /srv/ops/ledger/data/heartbeat
cat /srv/ops/ledger/data/access
systemctl show -p FragmentPath,DropInPaths,ProtectSystem,ReadWritePaths,MemoryMax,EnvironmentFiles,NeedDaemonReload ops-ledger.service
cat /sys/fs/cgroup/system.slice/ops-ledger.service/memory.max
sudo journalctl -u ops-ledger.service -b --no-pager -n 20
```
