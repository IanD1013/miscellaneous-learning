`systemd-analyze verify` 会像 systemd 那样读取 unit 文件，打印其中的问题，但不会启动任何服务。
它可以直接作为 `learner` 运行，无需 `sudo`：

```bash
systemd-analyze verify /etc/systemd/system/ops-batch.service
```

无任何问题的 unit 不会输出任何内容，并返回退出状态 0。
该检查的存在是因为 systemd 在加载 unit 时较为宽松。
它无法识别的 section 或键名只会在 journal 中记录一行并跳过，unit 在没有该设置的情况下依然会加载，因此拼错的键永远不会导致 `systemctl start` 失败；服务只是在没有该配置的情况下运行。
verify 会将该行作为 **unknown key** 警告输出到屏幕上。
它还会捕获启动时会遇到的两个问题：`ExecStart=` 对应的程序缺失或不可执行，以及 `Requires=` 指向了一个不存在的 unit。
这些属于错误，会将退出状态设为 1。
单单一个 unknown key 只是警告，输出时的退出状态仍为 0，因此请仔细阅读输出内容，而不要完全依赖 `$?`。

忽略任何与 `ops-batch` 或 `ops-spooler` 无关的 unit 提示行。

### 任务

`/etc/systemd/system/ops-batch.service` 存在四个缺陷。
它的脚本 `/usr/local/sbin/ops-batch` 会将其启动时所在的目录以 `workdir=` 开头的形式写入 `/run/ops/batch.done`。

编辑该 unit 或脚本需要使用 `sudo`。


- 修复该 unit，直到 verify 不再输出与其相关的任何内容。
  批处理必须在 `/srv/ops/batch` 中运行，因此 `/run/ops/batch.done` 的内容应为 `workdir=/srv/ops/batch`。
- `Requires=` 必须指向实际存在的 unit `ops-spooler.service`，这样在启动 batch 时也会启动 spooler。
  请修正名称而不是删除该行，并在其旁边添加 `After=ops-spooler.service`，两者都应放在 `[Unit]` 下：
  单独的 `Requires=` 不会规定两者的启动顺序，而在 `[Service]` 下这两行都会被视作未知键（unknown key）而被 systemd 忽略。
- 为该脚本赋予 `0755` 权限模式。
- 在完成最后的编辑后运行 `sudo systemctl daemon-reload`，启动 `ops-batch.service`，并保持两个 unit 均处于 active 状态。
  最终生效的启动必须是在加载了修正后的 `Requires=` 的前提下执行的，因此如果 batch 在修复前运行过且仍处于 active 状态，请重启它。
  这两个 unit 都是配置了 `RemainAfterExit=yes` 的 oneshot unit，因此在其命令退出后它们仍会保持 active 状态。

在修改任何内容之前先运行 verify。
它只报告了一个缺陷，而不是四个：

```text
/etc/systemd/system/ops-batch.service:5: Unknown section 'Serivce'. Ignoring.
ops-batch.service: Service has no ExecStart=, ExecStop=, or SuccessAction=. Refusing.
Unit ops-batch.service has a bad unit file setting.
```

第 5 行是拼错的 `[Service]` 标头。
systemd 会忽略它不认识的 section 下的每一行，因此 `WorkingDirectoy=` 和 `ExecStart=` 根本没有被读取，导致该 unit 完全没有 `ExecStart=`。

拼写错误的 `Requires=` 位于 `[Unit]` 下且已被读取，但是加载失败的 unit 根本不会进一步检查其依赖项，而且脚本的权限模式也不是文件中的某一行。
verify 运行只能报告 systemd 已经执行到了检查步骤的问题。
修复该标头并再次运行 verify：
其余三个缺陷将在第二次运行时显示，每一项都会指明其行号、文件或无法找到的 unit。
继续修复并重新运行，直到不再输出任何内容。

### 解答

```bash
# 先运行 verify 查看第一个缺陷
systemd-analyze verify /etc/systemd/system/ops-batch.service

# 修正 section 标头、WorkingDirectory= 键名，以及 Requires= 指向的 unit 名称，并在其后添加 After=
sudo sed -i \
  -e 's/^\[Serivce\]/[Service]/' \
  -e 's|^WorkingDirectoy=.*|WorkingDirectory=/srv/ops/batch|' \
  -e 's/^Requires=.*/Requires=ops-spooler.service\nAfter=ops-spooler.service/' \
  /etc/systemd/system/ops-batch.service
# 为脚本赋予 0755 权限模式
sudo chmod 0755 /usr/local/sbin/ops-batch

# 再次运行 verify，直到不再输出与 ops-batch 相关的内容
systemd-analyze verify /etc/systemd/system/ops-batch.service
sudo systemctl --no-pager cat ops-batch.service

sudo systemctl daemon-reload
# restart 会在已加载修正后的 Requires= 的前提下重新启动 batch，并拉起 spooler
sudo systemctl restart ops-batch.service

# 检查
systemctl is-active ops-batch.service ops-spooler.service
cat /run/ops/batch.done
```
