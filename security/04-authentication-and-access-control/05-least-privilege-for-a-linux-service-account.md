reports 服务以 `reports` 身份运行 `run-report.sh`，这是一个**服务账户**：一种仅为了运行单个程序而存在的系统用户。
该脚本从 `report.conf` 加载其配置，并将磁盘使用情况报告写入 `data` 目录，这三者都位于 `/srv/reports`（你的 shell 起始目录）中。
reports 允许执行的任何操作，通过漏洞控制该服务的攻击者也同样可以执行。
该账户的最小权限原则取决于其唯一工作所需的操作：运行脚本、读取配置以及写入 `data`。
而目前它拥有的权限远多于此。

### 账户

运行 `id reports`。
它会列出该账户所属的用户组，其中的 `27(sudo)` 将 reports 置于 **sudo group** 中，该组成员在输入自己的密码后可以以 root 身份运行任何命令。
在这台练习机上，有一条单独的规则允许你的账户 learner 无需密码即可使用 `sudo`。
reports 没有密码，因此目前无法使用 sudo，但该组成员身份赋予了服务从未需要的 root 访问权限，并且一旦有人为该账户设置了密码，它就会立即生效。

`getent passwd reports` 会打印 `/etc/passwd` 中该账户对应的一行。
在最后一个冒号之后的字段是**登录 shell**（login shell），即当有人以此账户登录或使用 `su` 切换到该账户时启动的程序。
以下是 Debian 为 Web 服务器保留的账户：

```text
$ getent passwd www-data
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

`nologin` 会打印 `This account is currently not available.` 并退出，因此以 www-data 登录的过程在出现可供输入的 shell 之前就会结束。
reports 的登录 shell 则是 `/bin/bash`，但该服务根本用不上它：无论是什么进程启动 `run-report.sh`，都会直接运行该文件，并且脚本的第一行 `#!/bin/sh` 指定了解析它的程序。

`usermod -s` 为账户赋予新的登录 shell，先指定 shell，后指定账户。
`gpasswd -d` 将账户移出用户组，先指定账户，后指定用户组。
对于另一台服务器上名为 mailer 的账户，剥夺其 shell 以及在 adm 组中的成员身份如下所示：

```bash
sudo usermod -s /usr/sbin/nologin mailer
sudo gpasswd -d mailer adm
```

`gpasswd -d` 仅移除组成员身份；账户及其文件保持不变。

### 所有者与模式

`ls -l` 显示每个文件的**所有者**（owner）、**所属组**（group）和**模式**（mode）。
模式由三组 `r`（读）、`w`（写）和 `x`（执行）组成：一组针对所有者，一组针对所属组的成员，一组针对其他所有账户。

```text
$ ls -l /etc/shadow /usr/sbin/nologin
-rw-r----- 1 root shadow   628 Oct 18 15:44 /etc/shadow
-rwxr-xr-x 1 root root   13796 Jul 17  2025 /usr/sbin/nologin
```

第一个字符在表示文件时为 `-`，在表示目录时为 `d`。
每组权限相加为一个数字，其中读为 4，写为 2，执行为 1。
`rwxr-xr-x` 为 755：root 可以修改 `nologin`，且每个账户都可以读取和运行它。
`rw-r-----` 为 640：root 可读写 `/etc/shadow`，shadow 组可以读取它，而其他账户没有任何权限。
在目录上，`r` 允许列出其中的名称，`x` 允许账户进入目录并访问文件，`w` 允许在其中创建、重命名和删除文件，包括不属于该账户的文件。

现在在这里运行 `ls -l`。
reports 拥有这全部三个项目，且所有者的数字包含写权限，因此该服务可以重写自己的脚本。
它还可以重写 `report.conf`，而 `cat run-report.sh` 显示脚本使用 `.` 加载该文件，这会将其中的每一行都作为 shell 命令运行。
一旦攻击者侵入一次，就可以向任一文件添加命令，随后每次运行都会执行这些命令，即便导致入侵的漏洞已被修复。
`data` 的权限是 777，因此该机器上的二十几个账户中的任何一个都可以读取、删除或替换这些报告。

`chown owner:group` 设置文件的所有者和所属组，而 `chmod` 通过数字设置其模式。
两者也适用于目录，并且都可以在一条命令中接受多个名称。
你拥有自己的 home 目录，因此可以在那里尝试：

```text
$ touch ~/tidy.sh
$ chmod 750 ~/tidy.sh
$ sudo chown root:root ~/tidy.sh
$ ls -l ~/tidy.sh
-rwxr-x--- 1 root root 0 Oct 18 15:44 /home/learner/tidy.sh
$ echo date >> ~/tidy.sh
-bash: /home/learner/tidy.sh: Permission denied
$ rm -f ~/tidy.sh
```

当文件属于你时，`chmod` 不需要 `sudo`；将其所有权交给 root 后则需要。
在所有者和所属组均为 root 的 750 权限下，你的账户没有任何权限，因此写入失败，但 `rm` 却能成功执行：删除文件需要对目录具有 `w` 权限，而该目录属于你。
拥有其代码所在目录的服务也可以通过相同方式替换由 root 拥有的脚本。
`chmod 755` 则本应允许每个账户读取和运行 `tidy.sh`。

### 锁定 reports

使用 `sudo` 运行每项更改：只有 root 可以编辑账户，且这些文件属于 reports。
请直接就地修改现有账户，而不要删除并重新创建它。

- 给 reports 指定登录 shell `/usr/sbin/nologin`。
- 将 reports 从 sudo 组中移除。你自己的账户 learner 保留在该组中。
- `run-report.sh`：所有者为 root，模式设为 755，或者所属组设为 reports 且模式设为 750，以便服务通过组权限访问它，而其他账户没有任何权限。
- `report.conf`：所有者为 root，模式设为 644，或者所属组设为 reports 且模式设为 640。
- `data`：仍由 reports 拥有，模式设为 750 或 700。
- `/srv/reports` 由 root 拥有且模式为 755，可以保持不变。你也可以将其限制为 root:reports 750，但 reports 绝不能拥有它或能够写入它。你的账户不在 reports 组中，因此在该更改后，列出该目录的内容需要使用 `sudo`。

要检查你的成果，`id reports` 应该不再列出 sudo，并且 `sudo su reports` 应该打印 nologin 消息。
`sudo -u reports ./run-report.sh` 会在不经过任何登录 shell 的情况下以 reports 身份运行脚本。
它应该在没有输出的情况下完成，然后 `sudo ls -l data` 应该显示一份日期为今天的 `disk-` 报告。
若不使用 `sudo`，`ls data` 现在应该因 Permission denied 而失败，因为你的账户属于其他账户之一。
