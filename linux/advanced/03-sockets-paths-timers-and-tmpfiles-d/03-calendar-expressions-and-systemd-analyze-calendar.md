`ops-digest.timer` 从未启动过。
`systemctl status ops-digest.timer` 显示 `Loaded: bad-setting`，并且 `sudo journalctl -u ops-digest.timer` 会给出两行原因说明，每次像 `systemctl status` 这样的命令促使 systemd 重新尝试读取该文件时，这两行都会重复出现：

```text
systemd[1]: /etc/systemd/system/ops-digest.timer:5: Failed to parse calendar specification, ignoring: weekdays 9:30
systemd[1]: ops-digest.timer: Timer unit lacks value setting. Refusing.
```

systemd 会跳过其无法解析的 `OnCalendar=` 行。
由于此定时器没有其他行，因此 systemd 完全拒绝加载它：
损坏的表达式导致定时器处于停滞状态，永远无法处于 active 状态，并且一直在等待一个永远无法到来的时间。
如果第二行解析成功，定时器本应仅基于该行启动，而遗失的计划安排只会显示在日志中。

### 日历表达式（Calendar expressions）

`OnCalendar=` 的值包含三个字段：`DayOfWeek Year-Month-Day Hour:Minute:Second`：

```ini
OnCalendar=Mon..Fri *-*-* 09,17:30:00
```

星期字段是可选的，采用英文星期名称。
两个点表示范围，因此 `Mon..Fri` 代表周一到周五；并没有 `weekdays` 这个关键字。
省略日期则默认为 `*-*-*`（每天）；省略秒数则默认为 `:00`。

在任何字段内，逗号表示列表，`/` 表示重复间隔：`08..17:00/20` 表示从 08:00 到 17:40 每 20 分钟触发一次。

每个列表必须保留在自己的字段内。
`09,17:30` 是第 9 和第 17 个小时的第 30 分钟，即上述的两个时间点。
如果按平时的口语习惯写成 `9:30,17:30`，systemd 会将其解析为第 30 和第 17 分钟以及 30 秒。
当一天中的两个时间点分钟数不同，或者日期不同时，请为每个时间单独分配一行 `OnCalendar=`。

定时器会在其任何一行条件满足时触发（elapse）。

`systemd-analyze calendar` 可以在不涉及 unit 的情况下解析表达式。
对于每个表达式，它会打印原始形式（original form）、规范化形式（normalized form，即填充了省略字段并补齐了数字位数的表达式，例如 `9:30` 变为 `*-*-* 09:30:00`）以及下一次触发时间，而 `--iterations=3` 则会列出接下来的三次触发时间：

```console
$ systemd-analyze calendar --iterations=3 'Mon..Fri 9:30,17:30'
  Original form: Mon..Fri 9:30,17:30
Normalized form: Mon..Fri *-*-* 09:17,30:30
    Next elapse: Wed 2026-10-07 09:17:30 UTC
       From now: 3h 44min left
       Iter. #2: Wed 2026-10-07 09:30:30 UTC
       From now: 3h 57min left
       Iter. #3: Thu 2026-10-08 09:17:30 UTC
       From now: 1 day 3h left
```

它解析成功了，但它会在每个工作日的 09:17:30 和 09:30:30 触发，绝不会在傍晚触发。
改用 `systemd-analyze calendar --iterations=3 'Mon..Fri 09,17:30'`，触发时间就会落在 09:30 和 17:30。
时间均采用虚拟机的时区，即 UTC。

### 分散运行（Spreading the runs）

`AccuracySec=`（默认为一分钟）允许 systemd 在触发点之后的该时间窗口内的任意时刻启动定时器，这样一次唤醒就可以同时服务多个定时器。
`RandomizedDelaySec=` 在每次触发时添加一个介于 0 到其设定值之间的全新随机延迟，这样多台共享相同计划任务的机器就不会在同一秒同时访问同一台服务器。
`RandomizedDelaySec=10m` 允许最多十分钟的延迟。

### 任务

digest 任务必须在周一至周五的 09:30 和 17:30 运行，以及周六的 12:00 运行，每次运行最多可延迟十分钟。

- 使用 `systemd-analyze calendar` 检查你的表达式，并将定时器使用的每个表达式所输出的 `Normalized form:` 行保存到 `/home/learner/ops/calendar.txt`。
  写成一个工作日表达式或每个时间单独一个表达式均可，保存完整输出也同样有效。
- 使用 `sudo` 重写 `/etc/systemd/system/ops-digest.timer`，保留其 `[Unit]` 和 `[Install]` 部分，使 `[Timer]` 包含以 `OnCalendar=` 行形式呈现的调度计划（仅包含你已检查过的表达式）以及 `RandomizedDelaySec=10m`。
- 重新加载 systemd 并重启定时器。`ops-digest.timer` 必须处于 active 状态，且 `systemctl show -p TimersCalendar ops-digest.timer` 必须列出当前文件中包含的计划任务。

### 解答

```bash
# 检查两个表达式，确认触发时间正确
systemd-analyze calendar --iterations=3 'Mon..Fri 09,17:30' 'Sat 12:00'

# 保存每个表达式的 Normalized form 行
systemd-analyze calendar 'Mon..Fri 09,17:30' 'Sat 12:00' | grep 'Normalized form:' > /home/learner/ops/calendar.txt
cat /home/learner/ops/calendar.txt

# 查看原文件
cat /etc/systemd/system/ops-digest.timer

# 删除旧的 OnCalendar= 行，并在 [Timer] 下写入新的计划和随机延迟，[Unit] 与 [Install] 保持不变
sudo sed -i -e '/^OnCalendar=/d' -e '/^RandomizedDelaySec=/d' \
  -e '/^\[Timer\]/a OnCalendar=Mon..Fri 09,17:30\nOnCalendar=Sat 12:00\nRandomizedDelaySec=10m' \
  /etc/systemd/system/ops-digest.timer
cat /etc/systemd/system/ops-digest.timer

# 重新加载并重启定时器
sudo systemctl daemon-reload
sudo systemctl restart ops-digest.timer

# 验证
systemctl is-active ops-digest.timer
systemctl show -p TimersCalendar ops-digest.timer
```
