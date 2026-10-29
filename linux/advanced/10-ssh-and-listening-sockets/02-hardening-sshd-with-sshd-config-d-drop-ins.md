该服务器上已经存在 `/etc/ssh/sshd_config.d/05-legacy.conf`，其中设置了 `PasswordAuthentication yes` 和 `PermitRootLogin yes`。

如果在其旁边名为 `50-hardening.conf` 的 drop-in 文件中写入 `PasswordAuthentication no`，`sudo sshd -T` 依然会输出 `passwordauthentication yes`。

sshd 解决配置冲突的方式与 systemd drop-in 以及 sysctl.d 相反（后者是最后读取的文件生效）：对于大多数关键字，sshd 会保留**首次获取的值**，并忽略后续所有对该关键字的设置行。
而设计为可重复出现的关键字（例如 `Port` 和 `HostKey`）则会进行累加。

Debian 的 `/etc/ssh/sshd_config` 第 12 行是 `Include /etc/ssh/sshd_config.d/*.conf`。

sshd 会在该位置按照文件名的字典顺序读取匹配的文件，早于主文件的其余部分。
因此，名为 `01-ops-hardening.conf` 的文件会在 `05-legacy.conf` 之前被读取，并且这两个文件都会覆盖主文件后面自身的 `PermitRootLogin prohibit-password`。

要覆盖你无权编辑的 drop-in 配置，只需为你的文件指定一个排序更靠前的名称，例如 `/etc/ssh/sshd_config.d/01-ops-hardening.conf`：

```text
PasswordAuthentication no
PermitRootLogin no
```

有两个命令可以检查 sshd 处理磁盘文件时的行为。
`sudo sshd -t` 会解析所有配置文件；如果文件有效，它不会输出任何内容并以状态码 0 退出；如果无效，则会指出出错的文件、行号和关键字。
`sudo sshd -T` 会打印处理 include 之后的每一项生效配置，每行一项，关键字转为小写并按照 sshd 固定的顺序排列。
只有当你传入连接详细信息（如 `sudo sshd -T -C user=learner,host=localhost,addr=127.0.0.1`）时，针对特定用户的 `Match` 覆盖项才会显示出来。
这两个命令都不会影响正在运行的守护进程，守护进程会一直保持启动时读取的配置，直到执行 `sudo systemctl reload ssh`；之后新的连接才会采用新配置。
因此，即使 `sshd -T` 已经显示为 `no`，运行中的服务器可能仍然接受密码认证。

### 加固此服务器

ssh.service 正在运行，且 `05-legacy.conf` 归平台团队所有，因此请保持其原样。
同样也请保持 `/etc/ssh/sshd_config` 完全不变（包括 `Include` 行等）：必须通过 drop-in 文件的名称来决定顺序，而不是通过修改主文件。
当前 `sudo sshd -T` 显示 `maxauthtries 6`、`permitrootlogin yes`、`passwordauthentication yes` 和 `kbdinteractiveauthentication no`。

系统提供的 ops-ssh-check 会尝试在 127.0.0.1 上以 learner 身份在无密钥且无提示的情况下登录，并将检测结果写入 `/run/ops/ssh-check`。

它已经运行过一次，每次执行 `sudo systemctl start ops-ssh-check.service` 都会重新运行并重写该文件。
第一行是登录结果。
下一行说明 `05-legacy.conf` 是否未被修改。
最后四行是 `sshd -T` 针对磁盘文件给出的值，即下一次 reload 或开机启动时将采用的配置。
现在运行 `cat /run/ops/ssh-check`，第一行显示为 `learner@127.0.0.1: Permission denied (publickey,password).`：表明密码仍是支持的认证方式之一。

使用 `sudo` 创建 `/etc/ssh/sshd_config.d/01-ops-hardening.conf`，设置 `PasswordAuthentication no`、`PermitRootLogin no`、`KbdInteractiveAuthentication no` 以及 `MaxAuthTries 3`（每个连接允许的认证尝试次数）。
Keyboard-interactive 是 sshd 请求密码的另一种途径，在最先读取的文件中将其设置为 `no` 意味着排序靠后的 drop-in 都无法将其重新启用。
使用 `sudo sshd -t` 进行验证，使用 `sudo systemctl reload ssh` 应用更改，并保持 ssh.service 处于 active 状态。

使用 `sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|kbdinteractiveauthentication|maxauthtries) ' > /home/learner/ops/sshd-effective` 记录结果（重定向以你的身份运行，这没有问题，因为 `/home/learner/ops` 归你所有）。
该文件必须严格按此顺序包含以下内容：

```text
maxauthtries 3
permitrootlogin no
passwordauthentication no
kbdinteractiveauthentication no
```

最后运行 `sudo systemctl start ops-ssh-check.service` 并执行 `cat /run/ops/ssh-check`，此时应显示 `Permission denied (publickey).`，接着是 `/etc/ssh/sshd_config.d/05-legacy.conf: unchanged`，最后是上述四行内容。
在你执行完最后一个命令之后，运行中的服务器必须持续保持返回该登录响应，而不仅仅是在你查看的那一刻。

### 解答

```bash
# 创建排序最靠前的 drop-in，使其设置先于 05-legacy.conf 被读取
sudo tee /etc/ssh/sshd_config.d/01-ops-hardening.conf <<'EOF'
PasswordAuthentication no
PermitRootLogin no
KbdInteractiveAuthentication no
MaxAuthTries 3
EOF

# 校验配置语法（无输出且退出码为 0 表示有效）
sudo sshd -t

# 让运行中的守护进程加载新配置，并确认服务仍为 active
sudo systemctl reload ssh
systemctl is-active ssh

# 记录生效值
sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|kbdinteractiveauthentication|maxauthtries) ' > /home/learner/ops/sshd-effective
cat /home/learner/ops/sshd-effective

# 重新运行检测并查看结果
sudo systemctl start ops-ssh-check.service
cat /run/ops/ssh-check
```
