apt 并不是简单地安装版本号最高的包。
它会为每个可用版本分配一个 pin priority（固定优先级），并将具有最高优先级的版本作为 candidate（候选版本），即 `apt-get install` 和 `apt-get upgrade` 会安装或升级到的版本；只有在优先级相同时，才会回退到选择更高版本号。
`apt-cache policy ops-tool` 可以打印出完整的决策过程，且无需 `sudo` 即可运行。
在这台虚拟机上，`ops-tool` 1.0 和 2.0 都位于扁平仓库 `/srv/ops/repo` 中（即 `/etc/apt/sources.list.d/ops.list` 中的 `[trusted=yes]` 源），目前已安装的是 2.0：

```text
ops-tool:
  Installed: 2.0
  Candidate: 2.0
  Version table:
 *** 2.0 500
        500 file:/srv/ops/repo ./ Packages
        100 /var/lib/dpkg/status
     1.0 500
        500 file:/srv/ops/repo ./ Packages
```

每个版本后面的数字是其优先级，缩进行显示了该版本的来源：
普通仓库为 500，记录在 `/var/lib/dpkg/status` 中的已安装副本为 100（标记为 `***`）。
两个版本的优先级都是 500 并列，因此 2.0 胜出。

`/etc/apt/preferences.d/` 目录下文件中的配置段（stanza）可以更改这些数字。
它指定了软件包名称、匹配的版本以及赋予它们的优先级：

```text
Package: ops-tool
Pin: version 1.0*
Pin-Priority: 1001
```

`1.0*` 可以匹配 1.0 以及任何以此开头的版本，例如 `1.0-2`。

字段的出现顺序随意，并且允许添加一行供下一位管理员阅读的 `Explanation:`。

优先级决定了 apt 的执行力度。
从 501 到 999，apt 在全新安装时会优先选择 1.0，但绝不会将已安装的 2.0 进行降级。
从 1000 开始，它会执行降级以达到 1.0，并在后续的每次升级中都将其保留为候选版本。
`apt-get` 会将降级视为需要确认的操作，因此单独使用 `-y` 会拒绝执行并返回状态码 100；非交互式命令形式为 `apt-get install -y --allow-downgrades ops-tool`。


`apt-mark hold` 的作用则不同：
它会锁定当前已安装的版本以防止升级。
在这里，它只会保留 2.0，而不会做出其它选择。

### 要求

- `/etc/apt/preferences.d/ops-tool` 包含一个配置段，其中包含 `Package: ops-tool`、`Pin: version 1.0`（带或不带 `*` 均可）以及 1000 或更高的 `Pin-Priority`。
  写入该文件需要 `sudo` 权限，例如可以使用带有 here-document 的 `sudo tee`。
- 在不指定版本的情况下直接执行普通安装 `ops-tool` 后，系统已就绪 1.0 版本：
  `/usr/bin/ops-tool` 输出 `ops-tool 1.0`，且该软件包未处于 hold 状态。
  两个构建版本均已存在于仓库中，无需重新构建任何内容。

在安装之前，请先确认输出中显示 `Candidate: 1.0`。

安装期间 apt 打印的 `debconf: unable to initialize frontend` 提示信息在这台虚拟机上是无害的。

### 解答

```bash
# 写入 pin 配置段，优先级 1001 允许降级到 1.0
sudo tee /etc/apt/preferences.d/ops-tool >/dev/null <<'EOF'
Package: ops-tool
Pin: version 1.0*
Pin-Priority: 1001
EOF

# 确认 Candidate: 1.0
apt-cache policy ops-tool

# 确保软件包未处于 hold 状态
sudo apt-mark unhold ops-tool

# 不指定版本的普通安装，非交互地允许降级
sudo apt-get install -y --allow-downgrades ops-tool

# 验证：输出 ops-tool 1.0，且 hold 列表中没有 ops-tool
/usr/bin/ops-tool
apt-mark showhold
```
