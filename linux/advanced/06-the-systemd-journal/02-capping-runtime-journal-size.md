在这台虚拟机上，日志仅保存在内存中。
journald 的 `Storage=` 设置决定了存储位置：`volatile` 将条目保存在 `/run/log/journal` 中，`persistent` 将其写入 `/var/log/journal`，而默认的 `auto` 仅在 `/var/log/journal` 存在时才写入磁盘。
该目录在这里虽然存在，但 journald 无法在这台虚拟机的根文件系统上打开日志文件，因此所有内容都保留在 `/run/log/journal/<machine-id>/` 下的运行时日志（runtime journal）中。
在这台虚拟机上，`/run` 是一个约 46M 的 tmpfs，因此日志在其中占用的每一兆字节都是从系统其他部分夺取的 RAM。

`RuntimeMaxUse=` 用于限制运行时日志的上限：包括当前活动文件及其旁边的所有已归档日志文件。
第二项设置 `RuntimeMaxFileSize=` 决定何时归档活动文件并启动新文件，其默认值为上限值的八分之一。
类似 `SystemMaxUse=` 这样的 `System*` 设置仅管理 `/var/log/journal`，因此在这台机器上它们不会产生任何效果。

使用 drop-in 文件设置上限，不要修改系统自带的 `/etc/systemd/journald.conf`，这与 unit drop-in 的理念相同。
journald 会首先读取 `journald.conf`，然后按名称顺序读取 `/etc/systemd/journald.conf.d/` 中所有以 `.conf` 结尾的文件，后读取的值会覆盖先前的值。
没有 `.conf` 后缀的文件会被忽略，并且配置中必须包含 section 标头：

```ini
[Journal]
RuntimeMaxUse=8M
```

journald 仅在启动时读取其配置，因此在执行 `sudo systemctl restart systemd-journald` 之前，任何更改都不会生效。
在启动过程中，它会删除最旧的归档文件，直到日志大小符合上限，然后记录其最终确定的限制值。
`sudo journalctl -u systemd-journald` 会显示这些行（打印到屏幕时可添加 `--no-pager`）。
目前最新的一行显示：

```text
Runtime Journal (/run/log/journal/<machine-id>) is 13.5M, max 16.0M, 2.4M free.
```

### 清理（Vacuuming）归档文件

`sudo journalctl --vacuum-size=8M` 会按从旧到新的顺序删除已归档的日志文件，直到总量符合要求；`--vacuum-time=` 和 `--vacuum-files=` 则分别按时间或数量执行相同的清理操作。
它绝不会删除活动文件；如果该文件也需要清理，可以先使用 `sudo journalctl --rotate` 将其归档并启动一个新文件。
清理（Vacuuming）是在不重启 journald 的情况下压缩正在运行的日志或将其降至上限以下的方法。
`sudo journalctl --disk-usage` 会以 `Archived and active journals take up X in the file system.` 的格式输出总占用量。

### 将此日志限制为 8M

本实验在 `journald.conf` 中设置了 `RuntimeMaxUse=16M`，重启了 journald，并将日志填充到了大约 14.4M。

1. 使用 `sudo` 创建 `/etc/systemd/journald.conf.d/size.conf`，在 `[Journal]` 下添加 `RuntimeMaxUse=8M`，然后重启 systemd-journald。
2. 将 journald 在重启时记录的 `Runtime Journal` 行（即报告 `max 8.0M` 的那一行）保存到 `/home/learner/ops/journal-limits`。
   实验初始设置留下的旧记录仍然显示 `max 16.0M`，因此仅保留最新的一行；日期和主机名前缀可以保留或去除（`-o cat` 可去除它们）。
3. 重启仅清理了刚好能容纳在上限之内的部分，因此 `sudo journalctl --disk-usage` 仍会报告约 6.9M。
   保持 8M 作为新条目的上限，但现在使用 `sudo journalctl --vacuum-size=4M` 将 RAM 释放归还。
   它会删除两个最旧的 2.0M 归档文件，留下约 2.9M（活动文件加上一个归档文件），因此在这里事先执行 `--rotate` 是可选的。
   将清理后执行 `sudo journalctl --disk-usage` 的输出保存到 `/home/learner/ops/journal-usage`；其报告的大小必须为 4M 或更小。

### 解答

```bash
# 1. 用 drop-in 设置运行时日志上限（不修改 journald.conf），然后重启 journald
sudo mkdir -p /etc/systemd/journald.conf.d
sudo tee /etc/systemd/journald.conf.d/size.conf > /dev/null <<'EOF'
[Journal]
RuntimeMaxUse=8M
EOF
sudo systemctl restart systemd-journald

# 2. 只保存最新一条 Runtime Journal 行（应显示 max 8.0M）
sudo journalctl --no-pager -u systemd-journald -o cat | grep 'Runtime Journal' | tail -n 1 > /home/learner/ops/journal-limits
cat /home/learner/ops/journal-limits

# 3. 清理归档文件，释放 RAM，然后保存占用量（必须为 4M 或更小）
sudo journalctl --vacuum-size=4M
sudo journalctl --disk-usage > /home/learner/ops/journal-usage
cat /home/learner/ops/journal-usage
```
