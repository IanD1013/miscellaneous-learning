sshd（即 SSH 服务器）会将每次登录尝试作为安全事件记录下来：尝试的账户、来源地址以及是否登录成功。
失败记录表明某个地址正在尝试密码，而只有成功记录才能表明其已成功侵入，因此发现入侵行为需要兼顾两者。
rsyslog 是将这些行写入 `/var/log/auth.log` 的程序。
Ubuntu Server 默认安装了它；Debian 12 则没有，因此除非有人安装了 rsyslog，否则 Debian 12 服务器只会将 sshd 的日志保存在 systemd journal 中。
本课程的机器运行未安装 rsyslog 的 Debian 12，且自身没有登录记录，因此没有 auth.log。
在你的 Shell 起始目录 `~/review` 中，本课程放置了一个 `auth.log`，它是某台运行 rsyslog 的服务器一整天的 `/var/log/auth.log` 副本。
其中的所有地址均来自为文档保留的网段，因此没有一个是真实的机器。

### 查看 sshd 日志行

每一行均以 UTC 时间（即 `+00:00`）、服务器的主机名以及写入该行的程序及其括号中的进程 ID 开头。
同一次连接的 sshd 日志行会共享该 ID。
来自另一台服务器的四行示例：

```text
2026-09-02T22:10:41.118204+00:00 db2 sshd[1844]: Invalid user oracle from 203.0.113.50 port 40112
2026-09-02T22:10:43.130511+00:00 db2 sshd[1844]: Failed password for invalid user oracle from 203.0.113.50 port 40112 ssh2
2026-09-02T22:11:02.442907+00:00 db2 sshd[1851]: Failed password for root from 203.0.113.50 port 40180 ssh2
2026-09-02T23:05:17.902655+00:00 db2 sshd[2210]: Accepted password for anna from 198.51.100.8 port 50331 ssh2
```

- `Failed password for root`：root 账户存在，但密码错误。
- `Failed password for invalid user oracle`：服务器上没有名为 oracle 的账户，因此无论输入什么密码，该尝试都不可能成功。
  它上面那行 `Invalid user` 属于同一次连接。
- `Accepted password for anna`：密码匹配，且已登录 anna 的账户。
  sshd 只检查密码，而不检查输入密码的人，因此猜出的密码生成的日志行与 anna 本人输入密码完全相同。
- `Accepted publickey` 行（副本中也存在）表示使用私钥登录，其对应的公钥位于该账户的 `authorized_keys` 中。

该副本还包含 pam_unix、systemd-logind 和 CRON 行。
它们用其他方式描述了相同的登录过程，或是计划任务，你可以忽略它们。

### 使用 grep、sort 和 uniq -c 进行计数

`grep 'Invalid user' auth.log` 会输出包含该文本的所有行。
引号将模式保持为一个整体；如果没有引号，grep 会将 `user` 视为文件名。
`grep -o` 仅输出每行中匹配的部分，每行一个匹配项。
在模式中，`[a-z]` 代表任意单个小写字母，后面的 `*` 会尽可能多地匹配连续的小写字母，因此 `[a-z]*` 会匹配整个名称并在其后的空格处停止。
`head -n 3` 保留前三行：

```text
$ grep -o 'Invalid user [a-z]*' auth.log | head -n 3
Invalid user admin
Invalid user user
Invalid user test
```

在没有指定文件名的情况下，grep 会读取通过 `|` 传入的行，因此一个 grep 可以筛选行，第二个 grep 可以从每行中截取一部分。
方括号还可以列出多个范围和字符：`[0-9:]` 表示数字或冒号。
这将输出针对 admin 的前几次尝试的时间：

```text
$ grep 'Invalid user admin' auth.log | grep -o 'T[0-9:]*' | head -n 3
T01:42:51
T01:53:49
T02:01:55
```

`uniq -c` 将连续的重复行折叠为一行，并在前面显示出现次数。
它仅将每行与其前一行进行比较，因此先执行 `sort` 将相同行汇集在一起。
然后 `sort -rn` 按该数字（`-n`）对结果进行排序，从大到小（`-r`）：

```text
$ grep -o 'Invalid user [a-z]*' auth.log | sort | uniq -c | sort -rn | head -n 4
      8 Invalid user test
      8 Invalid user admin
      5 Invalid user user
      5 Invalid user oracle
```

这些是在服务器上没有账户但被反复尝试的用户名。
root 不在列表中，因为 root 账户是存在的：对它的尝试显示为 `Failed password for root`。

### 记录入侵信息

按地址统计 Failed password 行的数量可以告诉你哪个地址尝试得最频繁，但不能告诉你哪个地址成功侵入。
一个地址可能失败数十次后放弃，而另一个地址尝试较少次数后就成功进入。
你要找的那个地址会有 Failed password 行，且随后出现了 Accepted password 行。

- 在 `auth.log` 中找到该地址，以及其 Accepted password 行中指定的账户。
- 将它们写入 `~/review` 下的 `findings.txt` 中：第一行为该地址，第二行为该账户，文件中不要包含其他任何内容，因此不要包含标签、计数或 `from`。

可以使用 nano 或 vim 编写该文件，也可以使用 `printf`，它会对其后的每个参数复用其格式：`printf '%s\n' red blue > /tmp/colors.txt` 会将 `red` 和 `blue` 分别写入不同行。
`>` 每次都会替换文件的内容，而 `>>` 则会追加到先前尝试留下的内容之后。
