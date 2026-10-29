在 `/run` 下使用 `mkdir` 和 `chown` 创建的目录在下次启动后就会消失，因为 `/run` 是一个 tmpfs，每次启动时都会从空目录开始。
必须在系统启动后就存在的路径需要在 **tmpfiles.d** 中声明：
软件包提供的 `.conf` 文件位于 `/usr/lib/tmpfiles.d`，而供你自定义的位于 `/etc/tmpfiles.d`。

`/etc/tmpfiles.d` 中的文件会替换 `/usr/lib/tmpfiles.d` 中的同名文件。
在系统启动时，`systemd-tmpfiles-setup.service` 会应用每一行规则。
一行的字段依次为 type（类型）、path（路径）、mode（权限模式）、user（用户）、group（用户组）、age（生命周期）和 argument（参数），使用 `-` 表示该字段未设置：

```text
d /run/ops-cache 0750 www-data www-data -
```

第一个字段是行类型。
`d` 会以该权限模式和属主创建目录；如果目录已经存在，它会将权限模式和属主重置为所声明的值。
`f` 创建文件，`L` 创建软链接（symlink），而 `z` 仅调整已存在路径的权限模式和属主。
无需重启即可进行测试：
`sudo systemd-tmpfiles --create /etc/tmpfiles.d/ops-cache.conf` 会立即应用该文件。

### 按生命周期清理

age 字段会让 `systemd-tmpfiles --clean` 删除路径中早于指定存活时间（age）的条目，同时保留目录本身。
`systemd-tmpfiles-clean.timer` 会在系统启动 15 分钟后运行该操作，之后每天运行一次。
默认情况下，条目的存活时间取决于其访问时间（access time）、修改时间（modification time）和变更时间（change time）中最晚的一个，这对于使用 `touch -d` 倒推时间的文件来说尤为重要。
以下是 `/var/cache/ops-thumbs` 中的一个缩略图：

```bash
$ stat -c '%n  Modify: %y  Change: %z' /var/cache/ops-thumbs/old-0001.png
/var/cache/ops-thumbs/old-0001.png  Modify: 2026-09-27 02:58:03.000000000 +0000  Change: 2026-10-07 02:58:05.000000000 +0000
```

`touch -d` 可以倒推访问时间和修改时间，但绝不能倒推变更时间，因为内核会在每次此类修改时将变更时间设置为当前时间。
因此，仅仅设置 `7d` 会将此文件视为几分钟前的文件并将其保留。
通过 age 前缀可以指定使用哪个时间戳，而 `m:` 表示仅依据修改时间：

```bash
d /var/cache/ops-thumbs 0755 root root m:7d
```

当目录已经存在且只需要清理功能时，`e` 行可以仅应用 age 规则，而不创建或修改该目录：`e /var/cache/ops-thumbs - - - m:7d`。

`D` 行在创建时的行为类似于 `d`，但 `systemd-tmpfiles --remove` 也会清空它，并且开机启动服务是以 `--remove` 运行的，因此 `D` 行会在每次系统启动时删除该目录下的所有内容。
`--create` 绝不会删除任何内容，因此请使用 `sudo systemd-tmpfiles --clean /etc/tmpfiles.d/ops-cache.conf` 自行触发清理，而无需等待定时器。
两个命令在成功执行时都不会输出任何内容。

### 任务

一个以现有 `www-data` 账户运行的缓存服务需要在每次启动时重新创建其运行时目录。
每个用于写入或应用配置的命令都需要使用 `sudo`。


- 创建 `/etc/tmpfiles.d/ops-cache.conf`，并在其中添加一行声明：将 `/run/ops-cache` 设置为目录，权限模式为 0750，用户为 `www-data`，用户组为 `www-data`。
- 在同一个文件中，为 `/var/cache/ops-thumbs` 添加一行规则，使得每日清理操作会移除修改时间超过 7 天的条目，并保留较新的条目。
  该行绝不能在系统启动时删除缩略图。
- 立即应用这两条规则。`/run/ops-cache` 必须存在且拥有指定的权限模式和属主。
  在 `/var/cache/ops-thumbs` 中，最后修改时间为 10 天前的 `old-0001.png` 到 `old-0004.png` 必须已被清理，而 1 天前修改的 `new-0001.png` 和 `new-0002.png` 必须被保留。

### 解答

```bash
# 写入配置：创建运行时目录，并按修改时间清理缩略图（e 行不会在启动时清空目录）
sudo tee /etc/tmpfiles.d/ops-cache.conf <<'EOF'
d /run/ops-cache 0750 www-data www-data -
e /var/cache/ops-thumbs - - - m:7d
EOF

# 立即创建目录
sudo systemd-tmpfiles --create /etc/tmpfiles.d/ops-cache.conf

# 立即执行按 age 清理
sudo systemd-tmpfiles --clean /etc/tmpfiles.d/ops-cache.conf

# 验证：0750 www-data www-data，且只剩 new-0001.png 和 new-0002.png
stat -c '%a %U %G %n' /run/ops-cache
ls -l /var/cache/ops-thumbs
```
