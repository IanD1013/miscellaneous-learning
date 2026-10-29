名为 `name@.service` 的 unit 文件是一个模板 unit（template unit）。
它绝不会以此名称直接运行：
你需要通过在 `@` 和 `.service` 之间写入一个字符串来启动一个实例，例如 `sudo systemctl start ops-sync@alpha.service`，systemd 会通过单个文件 `/etc/systemd/system/ops-sync@.service` 来构建该实例。
在读取该文件时，它会展开说明符（specifiers），即代表 unit 名称各部分的 `%` 代码：

```ini
[Service]
EnvironmentFile=/etc/ops/sync/%i.env
ExecStart=/usr/local/sbin/ops-sync --instance %i
```

`%i` 是实例字符串，因此 `ops-sync@alpha.service` 会加载 `EnvironmentFile=/etc/ops/sync/alpha.env` 并将 `alpha` 传递给程序，而 `ops-sync@beta.service` 则从相同的配置行中获取 `beta`。

`%n` 是完整的 unit 名称。
另一个站点只需要另一个 `.env` 文件即可，无需其他配置。
直接启动裸模板名称会被拒绝：

```text
Failed to start ops-sync@.service: Unit name ops-sync@.service is missing the instance name.
```

启用（enable）服务同样需要指定实例名称：
包含 `[Install]` 部分的模板通过类似 `sudo systemctl enable ops-sync@alpha.service` 的命令来启用。

`%i` 会提供与 unit 名称中完全一致的原样实例字符串（经过转义）。
unit 名称中不能包含 `/`，因此路径各部分之间会用 `-` 表示，而 `systemd-escape` 可以生成这种形式：
`systemd-escape --path /srv/ops/feeds` 会输出 `srv-ops-feeds`。

`%I` 则用于反转义。
在 `ops-sync@srv-ops-feeds.service` 中，`%i` 是 `srv-ops-feeds`，而 `%I` 是 `srv/ops/feeds`（unit 中可通过编写 `/%I` 来获取绝对路径）；在 `ops-sync@eu-west.service` 中，`%I` 会将连字符转为斜杠，即 `eu/west`。

真正包含连字符的名称在书写时需要转义：
`systemd-escape eu-west` 会输出 `eu\x2dwest`，而 `%I` 会将其还原为 `eu-west`。

对于类似 `alpha` 这样的名称，它们会展开为相同的字符串；当实例名称代表路径时，请使用 `%I`。


### 将两个 unit 合并为一个模板

`/etc/systemd/system` 中的 `ops-sync-alpha.service` 和 `ops-sync-beta.service` 当前正在运行，它们仅在站点名称上有所不同。
它们的环境文件分别在 `/etc/ops/sync/alpha.env` 中设置了 `SOURCE=/srv/ops/feeds/alpha`，在 `/etc/ops/sync/beta.env` 中设置了 `SOURCE=/srv/ops/feeds/beta`。

当 `/usr/local/sbin/ops-sync --instance NAME` 启动时，它会写入包含 `NAME $SOURCE`（取自实例接收到的环境变量）的 `/run/ops/sync/NAME.status`，以及 `/run/ops/sync/NAME.loaded`（用于展示 systemd 为该实例加载的内容，对应 `systemctl show` 输出的 `Id=` 和 `EnvironmentFiles=` 行）。
两个文件都会在实例停止时被删除。
要查看模板单独为新站点提供了什么配置，可以查询一个未运行的实例：
`systemctl show -p EnvironmentFiles ops-sync@gamma.service` 会从模板加载它而不启动，并且仅在 `EnvironmentFile=` 路径由实例名称构建时才会列出 `/etc/ops/sync/gamma.env`。


使用 `sudo` 执行以下操作：

- 编写 `/etc/systemd/system/ops-sync@.service`，使每个实例通过由 `%i`（或 `%I`）构建的 `EnvironmentFile=` 路径加载其自身的 `.env` 文件。
  该路径必须在模板中基于实例名称构建，而不是为每个实例单独设置，以便第三个站点除了自身的 `.env` 文件外无需任何其他配置。
- 停止这两个旧 unit，因为删除 unit 文件仍会使正在运行的 unit 保持运行状态；然后删除它们的 unit 文件，而不是将它们移动到另一个 unit 目录。
- 运行 `systemctl daemon-reload`，然后启动 `ops-sync@alpha.service` 和 `ops-sync@beta.service`。
- 不要在 systemd 加载 unit 的任何目录中留下针对单个实例命名的文件（例如 `ops-sync@alpha.service`）。
  因为无论在 `/etc/systemd/system`、`/run/systemd/system`、`/usr/local/lib/systemd/system` 还是 `/usr/lib/systemd/system` 中，systemd 都会优先加载此类文件以替代模板（`systemd-analyze unit-paths` 可以输出完整的搜索路径列表）。

完成后，两个实例均处于 active 状态，旧 unit 已停止。
`/run/ops/sync/alpha.status` 的内容为 `alpha /srv/ops/feeds/alpha`，且 `/run/ops/sync/alpha.loaded` 显示 `Id=ops-sync@alpha.service` 和 `EnvironmentFiles=/etc/ops/sync/alpha.env`；beta 对应的文件对于 `beta` 也会显示相同格式的内容。

### 解答

```bash
# 编写模板 unit，EnvironmentFile= 路径由实例名 %i 构建
sudo tee /etc/systemd/system/ops-sync@.service >/dev/null <<'UNIT'
[Unit]
Description=ops sync %i

[Service]
EnvironmentFile=/etc/ops/sync/%i.env
ExecStart=/usr/local/sbin/ops-sync --instance %i
UNIT

# 先停止两个旧 unit，再删除它们的 unit 文件
sudo systemctl stop ops-sync-alpha.service ops-sync-beta.service
sudo rm /etc/systemd/system/ops-sync-alpha.service /etc/systemd/system/ops-sync-beta.service

sudo systemctl daemon-reload
sudo systemctl start ops-sync@alpha.service ops-sync@beta.service

# 检查
systemctl is-active ops-sync@alpha.service ops-sync@beta.service
cat /run/ops/sync/alpha.status /run/ops/sync/alpha.loaded
cat /run/ops/sync/beta.status /run/ops/sync/beta.loaded
```
