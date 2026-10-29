一个仅访问自身文件的服务，以 root 身份运行并不会带来任何好处，而且其中的每个 bug 都会变成 root 级别的安全隐患。
为其分配一个**系统账户**，即一个专为程序而非个人存在的用户：

```bash
sudo useradd --system --shell /usr/sbin/nologin --no-create-home --user-group opsfeed
getent passwd opsfeed
```

```text
opsfeed:x:999:997::/home/opsfeed:/usr/sbin/nologin
```

- `--system` 从 1000 以下的范围分配 UID，从 `SYS_UID_MAX` 开始向下计数。
  在本机上，`/etc/login.defs` 将该设置保持为注释状态，因此使用内置的 999。
  如果不加该标志，`useradd` 会从 1000 开始向上分配下一个 UID，这是 `learner` 和其他所有普通个人用户所在的范围。
- `--user-group` 添加同名的 `opsfeed` 组，这里的 GID 为 997，同样来自于系统范围。
  `--no-create-home` 会跳过创建家目录，不过 passwd 字段仍会显示 `/home/opsfeed`。
- 将 `/usr/sbin/nologin` 作为 shell 会拒绝登录：
  `sudo su - opsfeed` 将输出 "This account is currently not available."。
  进程仍可以该账户身份运行。
  `sudo -u opsfeed id` 可以正常工作，并且 systemd 会直接启动服务的程序，无需经过 shell。
- 未设置密码，因此该账户在 `/etc/shadow` 中的对应字段为 `!`，即**锁定密码**，任何键入的内容都无法与之匹配。

`useradd` 位于 `/usr/sbin` 中，不在你的 PATH 环境变量内，因此请通过 `sudo` 来调用它。

随后该 unit 切换身份：

```ini
[Service]
User=opsfeed
Group=opsfeed
StateDirectory=opsfeed
```

`User=` 和 `Group=` 设置了服务进程运行时的凭据，因此它写入的每个路径都必须对该账户可写。
`StateDirectory=opsfeed` 让 systemd 在 `/var/lib/opsfeed` 不存在时创建它，并在每次启动前检查其所有者。
当该目录尚不属于该服务的用户和组时，systemd 会将其及其中的所有文件移交给它们。
如果已经是该用户和组所有，systemd 则不会触动内部内容，因此 root 稍后添加的文件仍将属于 root。
它还会通过 `STATE_DIRECTORY` 环境变量将该路径传递给服务的进程，systemd 仅会为带有 `StateDirectory=` 的 unit 设置该环境变量。
所有权随 unit 自动维护，无需在每次更改后都重复执行一次性的 `chown`。

`RuntimeDirectory=` 在 `/run` 下执行相同的操作，并在服务停止时删除该目录。

### 将 ops-feed.service 移出 root 运行

每次启动时，`ops-feed.service` 都会将 `id -un` 的输出写入 `/var/lib/opsfeed/whoami`，将 `$STATE_DIRECTORY` 写入 `/var/lib/opsfeed/state-dir`（当 systemd 未设置它时内容为单词 `unset`），并向 `/var/lib/opsfeed/feed.db` 追加一行内容。
当前它以 root 身份运行且未配置状态目录，因此 `whoami` 读取为 `root`，`state-dir` 读取为 `unset`，且所有这三个文件均属于 root。

使用 `sudo` 将 `opsfeed` 创建为系统账户（UID 小于 1000，shell 为 `/usr/sbin/nologin`，锁定密码），并带有 GID 同样小于 1000 的 `opsfeed` 组。
将上述三个指令放入 `/etc/systemd/system/ops-feed.service.d/` 下的 drop-in 文件中，使其在重启后仍然生效（在 `/run` 下的文件，即 `systemctl edit --runtime` 写入的文件，会在下次启动时丢失），重新加载 systemd，并重启该服务以使其处于 active 状态。
完成后，`/var/lib/opsfeed/whoami` 的内容必须为 `opsfeed`，`/var/lib/opsfeed/state-dir` 的内容必须为 `/var/lib/opsfeed`。


### 解答

```bash
# 创建系统账户 opsfeed 及同名系统组（UID/GID 小于 1000，shell 为 nologin，不创建家目录，密码保持锁定）
sudo useradd --system --shell /usr/sbin/nologin --no-create-home --user-group opsfeed
getent passwd opsfeed
getent group opsfeed
sudo grep '^opsfeed:' /etc/shadow

# 在 /etc 下写入持久的 drop-in
sudo mkdir -p /etc/systemd/system/ops-feed.service.d
sudo tee /etc/systemd/system/ops-feed.service.d/opsfeed.conf > /dev/null <<'EOF'
[Service]
User=opsfeed
Group=opsfeed
StateDirectory=opsfeed
EOF

# 重新加载 systemd 并重启服务
sudo systemctl daemon-reload
sudo systemctl restart ops-feed.service
systemctl is-active ops-feed.service

# 验证：应分别输出 opsfeed 和 /var/lib/opsfeed，且文件属于 opsfeed
cat /var/lib/opsfeed/whoami
cat /var/lib/opsfeed/state-dir
ls -l /var/lib/opsfeed
```
