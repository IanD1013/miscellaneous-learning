`authorized_keys` 中的一行可以在公钥前附带选项，这些选项决定了使用该公钥登录后可以执行哪些操作。
下面这行配置让该公钥只能执行一项特定的操作：

```text
restrict,command="/usr/local/bin/ops-report-push",from="127.0.0.1" ssh-ed25519 AAAA... learner@dometrain-linux
```

选项之间用逗号分隔，其间不能有空格，可以按任意顺序排列，并在公钥类型之前的空格处结束。
`command="..."` 将其设为强制命令：
无论客户端请求执行什么，sshd 在每次使用该公钥登录时都会运行 `/usr/local/bin/ops-report-push`，并通过环境变量 `SSH_ORIGINAL_COMMAND` 将客户端的请求传递给它。
客户端即使请求 `uname -a` 也只会触发该推送脚本，而绝不会执行 `uname`。

`from="..."` 仅在连接来自指定地址时才接受该公钥。
`restrict` 则可以通过一个关键字直接禁用端口转发、agent 转发、X11 转发以及终端分配。
它不会影响强制命令的执行，该命令依然会运行，只是没有终端支持：
运行 `ssh -tt` 会收到 `PTY allocation request failed on channel 0`。


该行的其余部分是由 `ssh-keygen` 生成的密钥对中的公钥部分。
私钥保留在客户端；`.pub` 文件包含以 `ssh-ed25519` 开头的一行内容，该行需放置在选项之后。

sshd 不会随随便便读取任意 `authorized_keys`。

在默认启用的 `StrictModes` 下，除非该文件、`.ssh` 目录以及用户主目录归该账户或 root 所有，且同组用户或其他用户均无写权限，否则 sshd 会忽略该文件。
权限为 0666 的文件会被直接跳过，登录过程会顺延至下一个认证方式。
通常的权限设置（也是本练习所要求的）是：
`.ssh` 目录为 0700，文件为 0600，且两者均归该账户所有。

### 为 opsreport 安装公钥

`opsreport`（uid 2300）是一个已被锁定的服务账户，目前尚无 `.ssh` 目录。
已安装的 `/usr/local/bin/ops-report-push` 会将 `ran by <user> original=<request>` 追加到 `/srv/ops/report-push.log` 中，且不输出任何内容。
操作 `/home/opsreport` 下的任何内容都需要 `sudo`。


- 使用空密码短语生成密钥对，因为无人会在现场手动输入密码：`ssh-keygen -t ed25519 -N '' -f /home/learner/ops/keys/report_ed25519`。
- 创建 `/home/opsreport/.ssh`，所有者为 `opsreport`，权限模式为 0700。
- 将上述整行内容写入 `/home/opsreport/.ssh/authorized_keys`，用 `report_ed25519.pub` 的内容替换 `ssh-ed25519 AAAA...`，并将该文件的所有者设置为 `opsreport`，权限模式设为 0600。
  可以用单引号包裹整个选项列表，以防 shell 解析并剥离其中的双引号，并让 `"$(cat /home/learner/ops/keys/report_ed25519.pub)"` 在其后提供公钥：
  `echo` 会将两者以空格连接输出，以便通过管道传给 `sudo tee`。
  `tee` 可以写入你无权直接写入的文件，但在 `sudo` 下创建的文件归 root 所有且权限为 0644，因此之后需要修改所有者和权限。
- 使用该私钥登录，并请求执行 `uname -a`：

```bash
ssh -i /home/learner/ops/keys/report_ed25519 -o StrictHostKeyChecking=accept-new opsreport@127.0.0.1 uname -a
```

`-i` 用于指定私钥，`accept-new` 会在首次连接时自动记录主机公钥而无需确认。
如果登录成功，第一次会打印 known-hosts 警告信息，之后则不会有任何输出。
该服务器仍允许密码认证，因此如果密钥被拒绝，最终会停留在密码提示符处（而该账户并没有密码）：
按 Ctrl-C，或者在 `opsreport@127.0.0.1` 之前加上 `-o BatchMode=yes` 以便立即报错退出。
`/srv/ops/report-push.log` 的最后一行必须显示为 `ran by opsreport original=uname -a`，因此请确保这是你的最后一次登录。

### 解答

```bash
# 生成无密码短语的密钥对
mkdir -p /home/learner/ops/keys
ssh-keygen -t ed25519 -N '' -f /home/learner/ops/keys/report_ed25519

# 创建 .ssh 目录：所有者 opsreport，权限 0700
sudo mkdir /home/opsreport/.ssh
sudo chown opsreport /home/opsreport/.ssh
sudo chmod 0700 /home/opsreport/.ssh

# 写入带选项的公钥行（单引号保留选项中的双引号）
echo 'restrict,command="/usr/local/bin/ops-report-push",from="127.0.0.1"' "$(cat /home/learner/ops/keys/report_ed25519.pub)" | sudo tee /home/opsreport/.ssh/authorized_keys >/dev/null

# tee 创建的文件归 root 且为 0644，改为 opsreport 所有、0600
sudo chown opsreport /home/opsreport/.ssh/authorized_keys
sudo chmod 0600 /home/opsreport/.ssh/authorized_keys

# 用该私钥登录并请求 uname -a（这必须是最后一次登录）
ssh -i /home/learner/ops/keys/report_ed25519 -o StrictHostKeyChecking=accept-new opsreport@127.0.0.1 uname -a

# 确认日志最后一行为 ran by opsreport original=uname -a
sudo tail -n 1 /srv/ops/report-push.log
```
