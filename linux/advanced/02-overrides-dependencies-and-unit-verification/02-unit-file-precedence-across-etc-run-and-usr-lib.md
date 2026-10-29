`ops-api.service` 在此机器上存在两份。
供应商文件 `/usr/lib/systemd/system/ops-api.service` 设置了 `API_VERSION=2.4`；而位于 `/etc/systemd/system/ops-api.service` 的一个被遗忘的完整副本设置了 `API_VERSION=1.9`，并且当前运行的正是 1.9。
`FragmentPath` 指明了 systemd 实际加载的文件：

```console
$ systemctl show -p FragmentPath,DropInPaths ops-api.service
FragmentPath=/etc/systemd/system/ops-api.service
DropInPaths=/etc/systemd/system/ops-api.service.d/workers.conf
```

systemd 沿着搜索路径查找 unit 名称，并使用它找到的第一个完整 unit 文件。
你所编辑的三个目录按以下优先级排序：用于本地配置的 `/etc/systemd/system`、用于运行时更改的 `/run/systemd/system`，以及软件包安装其 unit 的 `/usr/lib/systemd/system`。

`systemd-analyze unit-paths` 会输出完整的路径列表，包括 systemd 自身填充的目录。
由于第一个完整文件具有最高优先级，因此 `/etc` 中的副本遮蔽（shadow）了供应商文件，供应商文件的任何设置均未生效。
Drop-in 文件的运作机制有所不同。
来自各个层级的 `<unit>.d/*.conf` 文件会合并覆盖在胜出的完整文件之上，而绝不会替换它，这就是为什么 `workers.conf` 目前适用于 1.9 副本，并且在副本删除后将继续适用于供应商文件的原因。
`/run` 下的文件在下次开机时会消失，因此该目录用于仅需持续到下次重启前的更改。

`systemd-delta --no-pager --type=overridden,extended,masked` 会列出所有与软件包初始提供内容不同的 unit：`[OVERRIDDEN]` 表示产生遮蔽的完整副本（附带 diff 显示）、`[EXTENDED]` 表示 drop-in 文件，`[MASKED]` 则表示被屏蔽的项。
镜像中会包含一些系统默认的 Debian 行；只有 `ops-` 开头的行属于你的配置。

删除副本后，正在运行的进程不会发生任何改变，直到执行 `sudo systemctl daemon-reload` 重新读取搜索路径，并通过重启启动新进程。
Debian 将 `/lib` 链接到 `/usr/lib`，因此供应商目录在搜索路径上也显示为 `/lib/systemd/system`，这也是之后 `FragmentPath` 报告的名称：`/lib/systemd/system/ops-api.service`。


### 运行时屏蔽（Runtime masks）

`ops-metrics.service` 被屏蔽了（masked）：
它在 `/run/systemd/system` 中的名称是一个指向 `/dev/null` 的符号链接。
被禁用的 unit 仅仅缺少开机自启。
而被屏蔽的 unit 既无法手动启动，也无法作为依赖项拉起，并且 `systemctl enable` 会失败并报错 `Unit file /run/systemd/system/ops-metrics.service is masked.`。

对于位于 `/run` 中的链接，`systemctl is-enabled ops-metrics.service` 会输出 `masked-runtime`（若在 `/etc` 中则输出 `masked`）。
在 systemd 252 上，直接执行普通的 `systemctl unmask` 会以状态码 0 退出，但仍会保留 `/run` 链接；使用 `systemctl unmask --runtime ops-metrics.service` 则会将其删除并重新加载 systemd。

### 恢复两个 unit

使用 `sudo` 执行：

- 删除 `/etc/systemd/system/ops-api.service`，保留 `/etc/systemd/system/ops-api.service.d/workers.conf`，并让 `ops-api.service` 重新基于供应商文件处于 active 状态，其 drop-in 仅保留在该 `/etc` 目录中。
  启动时它会写入 `/run/ops/api.version`，其内容必须完全为 `version=2.4 workers=4`（在重启返回后片刻便会出现）。
- 清除 `ops-metrics.service` 上的运行时屏蔽并启动它，使其处于 active 状态。
  请直接移除该屏蔽本身：
  在 `/etc/systemd/system` 中放置一个完整副本虽然也能启动该 unit（因为在搜索路径上 `/etc` 优先于 `/run`），但这只是遮蔽了 `/dev/null` 链接，并留下了一个过时的多余副本。
  完成后，`/run/systemd/system/ops-metrics.service` 应已被清除，且该 unit 正常基于其供应商文件 `/usr/lib/systemd/system/ops-metrics.service` 运行。

### 解答

```bash
# 删除 /etc 中遮蔽供应商文件的完整副本，保留 workers.conf
sudo rm /etc/systemd/system/ops-api.service
sudo systemctl daemon-reload
sudo systemctl restart ops-api.service

# 移除 /run 中的运行时屏蔽（同时会重新加载 systemd），然后启动
sudo systemctl unmask --runtime ops-metrics.service
sudo systemctl start ops-metrics.service

# 检查
systemctl show -p FragmentPath,DropInPaths ops-api.service
cat /run/ops/api.version
systemctl is-active ops-api.service ops-metrics.service
systemctl show -p FragmentPath ops-metrics.service
ls -l /run/systemd/system/ops-metrics.service
```
