sudoers 规则的格式为 `USER HOST=(RUNAS) COMMANDS`，而 `Cmnd_Alias` 可以为一组命令赋予一个别名，以便规则保持简短。
下面两行可以让系统账户 `backup` 以 root 身份启动 `backup-run.service` 并读取该 unit 的日志（journal），仅此而已：

```text
Cmnd_Alias BACKUP_RUN = /usr/bin/systemctl start backup-run.service, /usr/bin/journalctl -u backup-run.service
backup ALL=(root) NOPASSWD: BACKUP_RUN
```

主机字段（host 字段）中的 `ALL` 使该规则适用于读取该文件的任何机器。
`(root)` 是 runas 列表，即 `backup` 可以以其身份运行这些命令的账户。
`NOPASSWD:` 用于免除后续命令的密码提示。
别名（Alias）名称只能包含大写字母、数字和下划线，且必须以大写字母开头。

命令必须使用绝对路径，并且 sudo 还会比对它们的参数。
带有参数列出的命令仅匹配完全相同的参数；未列出任何参数的命令则匹配所有参数列表。
针对纯 `/usr/bin/systemctl` 的规则将允许 `deployer` 运行 `systemctl stop ssh.service`，或者 `systemctl edit ops-web.service`（后者会以 root 身份打开编辑器，而 root 编辑器可以启动 root shell）。
通配符也无法安全地限制范围：
sudo 将参数作为一个整体字符串进行匹配，因此 `*` 也会匹配空格以及其后的任何额外参数。

Sudo 会读取 `/etc/sudoers`，其中的 `@includedir /etc/sudoers.d` 行会按名称顺序引入该目录下的文件，并跳过任何包含点号或以 `~` 结尾的文件名。
名为 `ops-deploy.conf` 的文件永远不会被读取。
当有多条规则匹配同一命令时，以最后匹配到的规则为准。
你自己的账户就体现了这一点：
`/etc/sudoers` 授予了 `sudo` 组规则 `ALL=(ALL:ALL) ALL`（该规则需要输入密码），而稍后读取的 `/etc/sudoers.d/learner` 则授予了 `NOPASSWD: ALL`，因此你的 `sudo` 永远不会提示输入密码。

### 在 sudo 读取规则之前进行检查

在 `/etc/sudoers.d` 中保存文件不会经过任何检查，而且 sudo 每次运行时都会解析每个 sudoers 文件。
当某一行无法解析时，sudo 1.9.13 会在每次运行时为每个用户输出错误，跳过该行并应用其余部分。
被跳过的行正是最容易出问题的地方：
`NOPASSWD` 后面漏掉冒号会导致 `deployer` 完全没有任何有效规则，而在 `/etc/sudoers.d/learner` 中出现相同的拼写错误，将导致你只剩下 `sudo` 组规则，而该规则需要输入你并未拥有的密码。
请将规则写在 sudo 不会检查的地方，例如 `/home/learner/ops` 中的某个文件（使用 `tee`、`printf` 或编辑器），并在该处进行检查。
将上述 `backup` 的两行保存为 `/home/learner/ops/demo` 后：

```text
$ sudo visudo -cf /home/learner/ops/demo
/home/learner/ops/demo: parsed OK
```

`visudo -cf FILE` 仅解析该文件并输出 `parsed OK`，或者输出每个错误的行号和列号。
经过检查的文件可以使用 `sudo install -m 0440 -o root -g root FILE /etc/sudoers.d/NAME` 安装，该命令会在同一操作中完成复制并设置所有者为 `root:root` 以及权限模式为 0440，因此它绝不会以其他权限留在 `/etc/sudoers.d` 中；0440 也是该目录下已有文件所采用的权限。
接下来，`sudo sudo -l -U USER` 会列出适用于 `USER` 的规则。
如示例所示，请以 root 身份运行它：
除非 `learner` 自己的所有规则都带有 `NOPASSWD`，否则列出另一个用户的权限会让 sudo 要求 `learner` 输入密码。
`sudo` 组规则并未带此标记，而 `learner` 也没有可用的密码。
`sudo -u USER sudo -n -l` 则从该用户的视角给出相同的列表。
目前 `deployer` 没有任何规则：

```text
$ sudo sudo -l -U deployer
User deployer is not allowed to run sudo on dometrain-linux.
```

### 要求

- `deployer` 是一个已存在的账户，拥有 home 目录和 bash shell，它只能通过 `sudo` 免密以 root 身份运行 `/usr/bin/systemctl restart ops-web.service` 和 `/usr/bin/systemctl status ops-web.service`，除此以外不能运行任何其他命令。
  该规则仅针对 `deployer`，不授予任何其他账户任何权限，并且仅允许 `deployer` 以 root 身份运行这两个命令，绝不能以其他用户或组的身份运行，甚至不能通过要求输入密码的规则来运行。
  该规则可以使用别名，也可以直接列出这两个命令。
- 该规则必须直接编写在 `/etc/sudoers.d/ops-deploy` 本身中，而不是通过 `@include` 从其他文件引入，并且该文件的所有者必须为 `root:root`，权限模式为 0440。
  其他任何 sudoers 文件都不得包含通过名称、uid、所属组或 `ALL` 作用于 `deployer` 的规则。
  对该目录的每次修改都需要使用 `sudo`。
- `/etc/sudoers.d/learner` 保持原样不变：仅包含单行 `learner ALL=(ALL:ALL) NOPASSWD: ALL`，所有者为 `root:root`，权限模式为 0440。
- 在你运行每条命令后，会有一个检查程序以 `deployer` 的身份在无密码的情况下检查七条命令是否被允许执行：restart 和 status，`systemctl stop ssh.service`，`systemctl edit ops-web.service`，`systemctl restart ssh.service`，以及在 `ops-web.service` 后面追加了 `ssh.service` 的 restart 和 status。
  检查程序将结果写入 `/run/dometrain-state/sudo-check`（可以使用 `sudo cat` 查看最新结果），其内容必须为：

```text
restart=allowed
status=allowed
stop-ssh=denied
edit=denied
restart-ssh=denied
restart-extra=denied
status-extra=denied
```

- `deployer` 的 sudo 规则必须确切指定这两个命令，每个命令均完整写出路径和确切参数，不包含通配符，也不包含其他内容。
  同一个检查程序会将 `sudo -ll -U deployer` 列出的每条命令（`-l` 的完整格式，每行一条命令）写入 `/run/dometrain-state/sudo-commands`，其内容必须为：

```text
/usr/bin/systemctl restart ops-web.service
/usr/bin/systemctl status ops-web.service
```


### 解答

```bash
# 先在 sudo 不会读取的位置编写规则
mkdir -p /home/learner/ops
cat > /home/learner/ops/ops-deploy <<'RULES'
Cmnd_Alias OPS_WEB = /usr/bin/systemctl restart ops-web.service, /usr/bin/systemctl status ops-web.service
deployer ALL=(root) NOPASSWD: OPS_WEB
RULES
# 检查语法，必须输出 parsed OK
sudo visudo -cf /home/learner/ops/ops-deploy
# 以 root:root、0440 一步安装到 /etc/sudoers.d/ops-deploy
sudo install -m 0440 -o root -g root /home/learner/ops/ops-deploy /etc/sudoers.d/ops-deploy
# 带点号的文件不会被读取，若存在旧的 ops-deploy.conf 则删除
sudo rm -f /etc/sudoers.d/ops-deploy.conf
# 确认其他 sudoers 文件中没有涉及 deployer 的规则，learner 文件保持原样
sudo grep -rn deployer /etc/sudoers /etc/sudoers.d
sudo cat /etc/sudoers.d/learner
ls -l /etc/sudoers.d
# 检查整个 sudoers 配置并列出 deployer 的规则
sudo visudo -c
sudo sudo -l -U deployer
sudo cat /run/dometrain-state/sudo-check
sudo cat /run/dometrain-state/sudo-commands
```
