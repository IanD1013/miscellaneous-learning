值班账户 `oncall`（uid 2400）应该能够使用其 SSH 密钥登录、读取 ops-web 日志并重启 `ops-web.service`，但目前这三项操作它都无法执行。
下面的检查会以 `oncall` 本身的身份尝试每种操作能力，因此在进行任何更改之前，请先运行一次并阅读输出结果。
该结果就是你的事件排查依据：
sshd 决定登录，`/srv/ops/logs` 上的权限决定读取，而 sudo 决定重启，因此每一行被拒绝（refused）的记录都会告诉你该检查这三者中的哪一个。
请使用能够满足需求的最窄权限授予来恢复各项能力。

### 系统现状

- `oncall` 的密码已被锁定，因此其密钥是唯一的登录途径。
  密钥对位于 `/home/learner/ops/keys/oncall_ed25519` 和 `oncall_ed25519.pub`；公钥部分已为 `oncall` 安装，且 `ssh.service` 正在运行。
- `/srv/ops/logs` 存放着 `ops-web.log` 和 `ops-web.log.1`，其所有者为 `root:adm`，创建时的权限模式为 0640，尽管 `ls -l` 目前将它们显示为 `-rw-------+`。
  该目录是一个为此练习挂载的 tmpfs，因为该虚拟机的根文件系统不支持存储 ACL。
  日志服务以 root 身份并在 umask 为 027 的情况下在此创建新日志。
  在目录上运行 `getfacl` 无需 `sudo`；在文件上运行则需要 `sudo`。
- `/etc/sudoers.d/` 下已添加了一条针对 `oncall` 的 sudo 规则。
  `sudo sudo -l -U oncall` 会列出 sudo 实际应用于 `oncall` 的规则；如果没有外层的 `sudo`，它会提示输入你并未拥有的密码。

### 检查机制

`sudo ops-oncall-check` 会以实际账户身份测试所有操作并输出结果。
每次你运行命令后，本练习都会运行相同的测试，并将结果写入 `/run/dometrain-state/oncall-check`（`sudo cat` 可以查看最新结果）。
每一行报告一项测试：

- `login`：使用该密钥以 `oncall@127.0.0.1` 身份执行 `ssh`。
- `log-read`、`new-log-read`：`oncall` 读取 `ops-web.log`，然后读取检查脚本模拟日志服务创建的新日志。
- `restart`：`oncall` 运行 `sudo -n /usr/bin/systemctl restart ops-web.service`。
- `stop-ssh`、`restart-ssh`、`read-shadow`：sudo 是否允许 `oncall` 运行 `/usr/bin/systemctl stop ssh.service`、`/usr/bin/systemctl restart ssh.service` 以及 `/usr/bin/cat /etc/shadow`。
- `restart-extra`、`restart-extra-first`：在允许的重启命令中，在 `ops-web.service` 之后或之前追加 `ssh.service` 时的测试情况。
- `other-command`：对任何规则中未命名的程序进行相同的检查。
- `guest-log-read`：`opsguest` 尝试读取日志。

### 要求

- 检查的最终输出结果必须为：

```text
login=ok
log-read=read
new-log-read=read
restart=allowed
stop-ssh=denied
restart-ssh=denied
restart-extra=denied
restart-extra-first=denied
read-shadow=denied
other-command=denied
guest-log-read=denied
```

- `oncall` 的规则位于 `/etc/sudoers.d/oncall`，所有者为 `root:root`，权限模式为 0440，并且在安装前必须通过 `sudo visudo -cf` 验证。
  权限仅授予 `oncall` 单独账户：
  在规则中指明 `oncall`，而不是 `%ops`（`opsdeploy` 也在该用户组中）或 `ALL`，以确保没有其他账户可以通过 sudo 重启 `ops-web`（无论是否带有 `.service` 后缀）。
  针对 `oncall` 的 sudo 规则必须严格且完整地允许 `/usr/bin/systemctl restart ops-web.service`，不能包含通配符或任何其他内容。
  `*` 的匹配范围比看起来更宽，因为 sudo 允许它匹配空格：
  `restart ops-web*` 也会允许 `restart ops-web.service debug-shell.service`，而该 unit 会在 tty9 上打开一个 root shell。
  即使使用 `!` 排除了某些命令，`ALL` 仍然保持完整的 sudo 权限：
  排除项仅阻止其指定的路径，因此任何其他程序，或者重命名后的被排除程序副本，仍然可以运行。
- `/etc/sudoers.d/learner` 保持完全原样。
- 日志访问权限来自 `/srv/ops/logs` 上的 ACL。
  不要给 other 赋予任何权限位，也不要修改用户组成员身份：
  将 `oncall` 添加到 `adm` 组中同时也会让它获得该组可读的所有其他日志的访问权限。
  该目录和两个日志文件的所有者必须保持为 `root:adm`，且你添加的每个 ACL 条目都必须是只读的并且仅针对 `oncall`，最终使 `ls -l` 在目录上显示为 `drwxr-x---+`，在每个日志文件上显示为 `-rw-r-----+`。
  如果通过 `chown` 将日志的所有权交给 `oncall`，则会允许它改写日志。
- 完成后，`/home/oncall/.ssh/authorized_keys` 的所属组（group）和其他人（other）不得具有写权限位，确保除 `oncall` 和 root 之外，没有人能够更改哪些密钥可以作为 `oncall` 登录。
  即使是 sshd 可以接受的 `oncall` 专属私有组也是如此：
  该写权限位仍会将写权限授予日后添加到该组的任何人。
  请修复文件权限，而不是修改 sshd：
  sshd 自带的所有权和模式检查（`StrictModes`）必须保持开启状态。

### 解答

```bash
# 排查：先运行一次检查，再查看三处相关配置
sudo ops-oncall-check
sudo ls -ld /home/oncall /home/oncall/.ssh /home/oncall/.ssh/authorized_keys
sudo journalctl -u ssh.service -b --no-pager -n 20
getfacl /srv/ops/logs
sudo getfacl /srv/ops/logs/ops-web.log /srv/ops/logs/ops-web.log.1
sudo ls -l /etc/sudoers.d/
sudo sh -c "grep -n -E 'oncall|%ops' /etc/sudoers.d/*"
sudo sudo -l -U oncall
sudo sudo -l -U opsdeploy

# 1. 登录：authorized_keys 去掉组和其他人的写权限，.ssh 与主目录也不可被他人写
sudo chown oncall /home/oncall/.ssh /home/oncall/.ssh/authorized_keys
sudo chmod 0600 /home/oncall/.ssh/authorized_keys
sudo chmod 0700 /home/oncall/.ssh
sudo chmod go-w /home/oncall

# 2. 日志：清除已有的扩展 ACL，恢复 root:adm 与基础权限
sudo setfacl -b /srv/ops/logs /srv/ops/logs/ops-web.log /srv/ops/logs/ops-web.log.1
sudo chown root:adm /srv/ops/logs /srv/ops/logs/ops-web.log /srv/ops/logs/ops-web.log.1
sudo chmod 0750 /srv/ops/logs
sudo chmod 0640 /srv/ops/logs/ops-web.log /srv/ops/logs/ops-web.log.1

# 仅为 oncall 添加只读条目：目录需要 r-x 才能进入，文件只给 r
sudo setfacl -m u:oncall:rx /srv/ops/logs
sudo setfacl -m u:oncall:r /srv/ops/logs/ops-web.log /srv/ops/logs/ops-web.log.1
# 默认 ACL：日志服务新建的日志也自动对 oncall 只读
sudo setfacl -d -m u:oncall:r /srv/ops/logs
ls -ld /srv/ops/logs
sudo ls -l /srv/ops/logs

# 3. sudo：先写规则到临时文件并验证
echo 'oncall ALL=(root) NOPASSWD: /usr/bin/systemctl restart ops-web.service' > /tmp/oncall.sudoers
sudo visudo -cf /tmp/oncall.sudoers

# 删除 sudoers.d 中其他授予 oncall 或 %ops 的文件（learner 文件保持原样）
sudo sh -c "grep -l -E 'oncall|%ops' /etc/sudoers.d/*" | grep -v -x '/etc/sudoers.d/learner' | xargs -r sudo rm -f

# 以 root:root 0440 安装规则，并检查整体配置
sudo install -o root -g root -m 0440 /tmp/oncall.sudoers /etc/sudoers.d/oncall
rm /tmp/oncall.sudoers
sudo visudo -c
sudo sudo -l -U oncall
sudo sudo -l -U opsdeploy

# 验证最终结果
sudo ops-oncall-check
```
