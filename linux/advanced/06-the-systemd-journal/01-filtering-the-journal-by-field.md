每个 journal 条目都是一组 `FIELD=value`（字段=值）键值对，`journalctl` 可以根据其中的任何字段来筛选条目。
名称以 `_` 开头的字段属于可信字段：journald 会根据内核报告的发送进程信息来添加它们（例如 `_PID`、`_UID`、`_COMM`、`_SYSTEMD_UNIT`），因此程序无法伪造它们。
其他字段（其中包括 `MESSAGE`、`PRIORITY` 和 `SYSLOG_IDENTIFIER`）则保存发送方写入的任何内容。

当前环境下 `learner` 不在 `adm` 或 `systemd-journal` 组中，因此每次执行 `journalctl` 都需要 `sudo`；否则会收到 `No journal files were opened due to insufficient permissions.`。

在进行筛选之前，先查看存在哪些字段和值：

```bash
sudo journalctl --no-pager -F SYSLOG_IDENTIFIER
sudo journalctl --no-pager -o verbose -n 1 -t ops-billing
```

`-F FIELD` 列出某个字段所包含的所有不重复值。
`-o verbose` 逐行打印每个条目的所有字段，而 `-o json` 则将相同字段按每行一个 JSON 对象的格式打印。

### 组合匹配条件

每个 `FIELD=value` 参数都是针对存储的精确字符串进行匹配。
不同字段的匹配条件通过 AND 组合，相同字段的重复匹配通过 OR 组合，而 `+` 则用于分隔通过 OR 组合的整个条件组。
假设在标识符 `lab` 下记录了三行日志，级别分别为 crit (2)、err (3) 和 warning (4)：

```text
$ sudo journalctl --no-pager SYSLOG_IDENTIFIER=lab PRIORITY=2 PRIORITY=4 -o cat
lab crit line
lab warning line
```

`-o cat` 仅打印 `MESSAGE`。

`-t NAME` 是 `SYSLOG_IDENTIFIER=NAME` 的简写形式，而 `-u UNIT` 则匹配 `_SYSTEMD_UNIT` 以及 systemd 自身关于该 unit 的启动和停止消息。
`-p err` 是一个优先级阈值，会保留 err 以及所有更严重的级别（包含 crit）。
如果只想匹配 err 单个级别，请使用 `PRIORITY=3`（该字段存储 0 到 7 的数字，绝不会是名称）或者传入范围 `-p err..err`。


发送方自行决定其标识符。
`logger -t ops-billing -p user.err "message"` 和 `printf 'msg\n' | systemd-cat -t ops-billing -p warning` 允许任何 shell 以指定的优先级写入带有 `ops-billing` 标签的条目，而服务则可以通过在其 unit 中设置 `SyslogIdentifier=` 并在每行 stdout 前加上 `<N>` 前缀来设置相同的两个字段。
两个 unit 可以共享同一个标识符，一个 unit 也可以使用多个标识符，因此只有 `_SYSTEMD_UNIT` 能够说明是哪个 unit 发送了条目。

### 任务

大约有 60 条级别为 crit、err、warning 和 info 的 `ops-billing` 条目，它们分别来自 `ops-billing.service`、`ops-billing-retry.service`（两者都设置了 `SyslogIdentifier=ops-billing`）以及 root shell 中的 `logger` 调用。
retry unit 还在第二个标识符下记录了日志。

编写 `/home/learner/ops/billing-errors`，其中仅包含由 `ops-billing-retry.service` 发送、带有标识符 `ops-billing` 且优先级正好为 err 的每个条目的消息文本（不能包含其他任何内容）：每行一条消息，按 journal 顺序排列。
`~/ops` 属于你的用户，因此重定向本身不需要 `sudo`。


### 解答

```bash
# 三个不同字段的条件通过 AND 组合：发送 unit、标识符、优先级正好为 err (3)
# -o cat 只输出 MESSAGE，重定向由自己的 shell 完成，不需要 sudo
sudo journalctl --no-pager _SYSTEMD_UNIT=ops-billing-retry.service SYSLOG_IDENTIFIER=ops-billing PRIORITY=3 -o cat > /home/learner/ops/billing-errors

# 验证
cat /home/learner/ops/billing-errors
```
