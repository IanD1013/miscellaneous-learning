`ProtectSystem=` 和 `ProtectHome=` 可以在不改变任何单个文件的情况下，改变服务能够写入和查看的内容。
当服务启动时，systemd 会为它提供专属的 mount namespace（挂载命名空间），即挂载表的一个私有副本，并在该副本内部将目录重新挂载为只读或将其隐藏。
Root 忽略权限位的特权无法突破只读挂载，因此以 root 身份运行的服务向其中写入时会收到 "Read-only file system" 错误。
你的 shell 以及所有其他进程仍保持正常的视图。

```ini
[Service]
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/spool/reports
```

- `ProtectSystem=` 接受一个级别参数。
  `yes` 会将 `/usr` 和 `/boot` 设为只读。
  `ProtectSystem=full` 会在此基础上增加 `/etc`，仅此而已，因此 `/srv`、`/var` 和 `/opt` 仍保持可写。
  `ProtectSystem=strict` 则除了内核的 API 文件系统 `/dev`、`/proc` 和 `/sys` 之外，将整个目录树都设为只读。
- `ReadWritePaths=` 在只读视图中重新开放某个路径及其子路径的写入权限。
  `ReadOnlyPaths=` 和 `InaccessiblePaths=` 则相反：前者将路径设为只读，后者将其从视图中移除。
  除非在路径前加上 `-` 前缀，否则列出的路径在服务启动时必须存在。
  unit 通过 `StateDirectory=` 获取的目录无需列出即可直接写入。
- `ProtectHome=yes` 会用一个权限模式为 000 的空目录覆盖 `/home`、`/root` 和 `/run/user`。
  像下文中的 `ops-export.service` 这样的 root 服务仍然可以列出 `/home` 并发现其为空；而在 `User=` 下运行的服务则完全无法打开它，并会收到 "Permission denied"。
  `ProtectHome=read-only` 会使它们保持可见但不可写入，而 `ProtectHome=tmpfs` 则会在其上挂载空的、可写的目录。

### 沙箱化 ops-export.service

`ops-export.service` 已安装但处于停止状态，并且它必须保持以 root 身份运行：它需要读取 `/etc/ops/export.key`，该文件属主为 root，权限模式为 0600。
每次启动时，它会尝试执行六项操作，并在 `/srv/ops/exports/probe.txt`（当前为 `pending`）中各写入一行：写入 `/etc/ops/probe`（`etc`）、`/usr/local/share/ops/probe`（`usr`）和 `/srv/ops/other/probe`（`srv`），列出 `/home/learner/ops`（`home`），读取密钥（`key`），以及写入 `/srv/ops/exports/report.csv`（`exports`）。
第七行 `protect` 则指明该进程运行时所采用的 `ProtectSystem=` 级别，该级别读取自其自身的挂载信息。
每次启动都会先删除旧的 `probe.txt`，因此该文件始终描述当前正在运行的进程。
仅 reload 而不 restart 不会对其产生任何改变；`systemctl show -p ProtectSystem ops-export.service` 会输出 systemd 为下一次启动所加载的级别。
按当前原样启动该服务，其他各行都会显示 `written`、`visible` 或 `readable`，且 `protect=no`。


使用 `sudo` 在 `/etc/systemd/system/ops-export.service.d/` 下添加一个 drop-in 配置，设置 `ProtectSystem=strict`、`ProtectHome=yes` 以及 `ReadWritePaths=/srv/ops/exports`。

重新加载 systemd（`systemctl edit` 会自动为你执行此操作），并重启该服务使其处于 active 状态。
这个可写路径也是允许该服务写入其报告的路径，因为 `probe.txt` 就保存在那里。
重启完成后，该文件的内容必须严格为：

```text
etc=denied
usr=denied
srv=denied
home=hidden
key=readable
exports=written
protect=strict
```

之后，从你自己的 shell 中，执行 `sudo touch /etc/ops/host-check` 和 `ls /home/learner/ops` 仍应正常工作。

### 解答

```bash
# 在 /etc 下写入 drop-in，服务仍以 root 运行，只改变其挂载视图
sudo mkdir -p /etc/systemd/system/ops-export.service.d
sudo tee /etc/systemd/system/ops-export.service.d/sandbox.conf > /dev/null <<'EOF'
[Service]
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/srv/ops/exports
EOF

# 重新加载 systemd 并重启服务
sudo systemctl daemon-reload
sudo systemctl restart ops-export.service
systemctl is-active ops-export.service
systemctl show -p ProtectSystem -p ProtectHome ops-export.service

# 验证服务写出的结果
cat /srv/ops/exports/probe.txt

# 验证自己的 shell 视图未受影响
sudo touch /etc/ops/host-check
ls /home/learner/ops
```
