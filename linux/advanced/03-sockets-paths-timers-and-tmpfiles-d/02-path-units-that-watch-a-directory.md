`/srv/ops/inbox` 中已经存放了 `pending-07.csv`，而 `ops-intake.service` 是一个现有的 oneshot 服务，它会将其中所有等待处理的 `*.csv` 移动到 `/srv/ops/processed`，并将每个文件名追加到 `/srv/ops/processed/manifest` 中。
目前还没有任何机制来启动它。
而 path unit 可以做到：
每当其在文件系统上的条件满足时，`ops-intake.path` 就会启动同名的 service（或由 `Unit=` 指定的 service）。
systemd 并不会对此进行轮询。
它会请求内核的 **inotify** 接口报告被监视路径的变更，并在收到变更通知时再次检查该条件。

### 状态条件还是事件条件

你选择的指令决定了 `pending-07.csv` 何时被移动。

- `PathChanged=` 对事件作出反应。
  它在监控启动后路径中发生更改时触发，因此原本就已存在的等待文件会一直留在原处，直到下一个文件的到来触发运行，届时它才会与新文件一起被处理清理。
- `DirectoryNotEmpty=` 对状态作出反应。
  只要目录中存在条目，它在监控启动时就会立即触发；并且每次服务执行完毕后，systemd 都会再次检查，只要目录中仍有残留文件，就会再次启动该服务。

这第二次检查正是服务必须清空目录的原因。
如果服务残留了文件，它就会被反复启动，直到 systemd 拒绝启动。
path unit 自身带有 **trigger limit**（在此 systemd 上为 2 秒内激活 200 次），并且对于运行迅速的 oneshot 服务，通常会先达到 service 的启动限制（10 秒内启动 5 次）。
无论触发哪种限制，监控最终都会变为 `failed` 状态并停止处理任何内容。

### 任务

unit 目录和 inbox 均属于 root，因此以下每项更改都需要 `sudo`。


- 创建 `/etc/systemd/system/ops-intake.path`，并在其中包含带有 `DirectoryNotEmpty=/srv/ops/inbox` 的 `[Path]` 小节。
  带有描述的 `[Unit]` 小节是可选的。
- 运行 `sudo systemctl daemon-reload`，然后运行 `sudo systemctl start ops-intake.path`，并使用 `ls` 检查 `pending-07.csv` 是否已自动移出 inbox。
- 将 `/home/learner/ops/samples/batch-41.csv` 复制到 `/srv/ops/inbox/` 中，并观察它到达 `/srv/ops/processed`。

保持 `ops-intake.path` 处于 active 状态，两个文件都应位于 `/srv/ops/processed` 中且 inbox 中均无残留。
请让 service 来移动这两个文件，这样每个文件名都会记录在 `/srv/ops/processed/manifest` 中；手动移动的文件绝不会出现在清单中。
systemd 运行的是它最后加载的 unit 版本，而不是文件当前的最新内容，因此 `systemctl show -p Paths ops-intake.path` 必须输出 `Paths=/srv/ops/inbox (DirectoryNotEmpty)`。


### 解答

```bash
# 创建 path unit：只要 inbox 非空就启动同名的 ops-intake.service
sudo tee /etc/systemd/system/ops-intake.path <<'EOF'
[Unit]
Description=Watch /srv/ops/inbox for pending CSV files

[Path]
DirectoryNotEmpty=/srv/ops/inbox
EOF

# 重新加载并启动监控
sudo systemctl daemon-reload
sudo systemctl start ops-intake.path

# pending-07.csv 应已被自动移出 inbox
ls /srv/ops/inbox /srv/ops/processed

# 放入新文件，由 service 自动处理
sudo cp /home/learner/ops/samples/batch-41.csv /srv/ops/inbox/
sleep 2
ls /srv/ops/inbox /srv/ops/processed
cat /srv/ops/processed/manifest

# 确认监控处于 active 状态且加载的是 DirectoryNotEmpty 条件
systemctl is-active ops-intake.path
systemctl show -p Paths ops-intake.path
```
