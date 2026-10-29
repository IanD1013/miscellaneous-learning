drop-in 是一个用于在不直接编辑单元文件的情况下修改 unit 的 `.conf` 文件。
systemd 会在以完整 unit 名称加上 `.d` 命名的目录中查找 drop-in，例如 `/etc/systemd/system/ops-web.service.d/`。

它会首先读取主文件，然后按照文件名顺序将该目录下的所有 `*.conf` 合并覆盖到其上。
软件包自带的 unit 文件位于 `/usr/lib/systemd/system` 下，下次软件包升级时会将其重写，但升级绝不会改动您在 `/etc` 中的 drop-in。
请务必在目录名中保留 `.service` 后缀：
systemd 会静默忽略 `ops-web.d/`。


`sudo systemctl edit ops-web.service` 是捷径。
它会创建该目录并在 Debian 的默认编辑器 nano 中打开 `override.conf`，当前 unit 的内容会作为注释行显示在下方。
您在 `### Anything between here...` 注释与 `### Lines below this comment will be discarded` 之间输入的任何内容都会写入该文件，当您保存并退出时，systemctl 会自动为您执行 `daemon-reload`。

使用 `sudo mkdir -p` 和 `sudo tee` 自行编写文件同样可行，但此时执行 `sudo systemctl daemon-reload` 就是您的职责了：
如果不重新加载就重启，服务仍会按照 systemd 已经加载的定义启动。

包含单个值的配置项（例如 `Description=`）会被 drop-in 直接替换。
而列表配置项（例如 `ExecStart=`、`ExecStartPre=` 或 `Environment=`）则会被追加。
对于 `Environment=`，这正符合预期，因为 drop-in 中的 `WEB_LOG=debug` 出现在厂商自带的 `WEB_LOG=info` 之后，针对同一变量的后续赋值会生效。
但对于 `ExecStart=`，追加意味着两条命令，而 systemd 仅对 `Type=oneshot` 服务接受多条命令，因此它会拒绝合并后的 ops-web unit。
空赋值（即 `=` 后面不带任何内容的配置项）可以清空列表，随后的下一行将成为唯一的命令：

```ini
[Service]
ExecStart=
ExecStart=/usr/local/sbin/ops-web --port 8090
```

`systemctl cat` 会输出主文件以及每个 drop-in，每个 drop-in 上方都有一行以 `#` 开头指明其路径的注释，这就是 systemd 合并后的内容。
它会在当前终端中打开分页器，因此请使用 `systemctl --no-pager cat ops-web.service`。

第一个标题显示为 `/lib/systemd/system/ops-web.service`；在这里 `/lib` 是指向 `/usr/lib` 的软链接，因此它就是软件包自带的文件。

### 将 ops-web 迁移到端口 8090

`ops-web.service` 当前正在基于软件包自带的 unit 运行，其配置为 `Environment=WEB_LOG=info` 和 `ExecStart=/usr/local/sbin/ops-web --port 8080`。

每次启动时，`/usr/local/sbin/ops-web` 首先会将 `systemctl show -p FragmentPath -p DropInPaths ops-web.service` 报告的内容（即 systemd 加载的 unit 文件以及它合并的 drop-in）保存到 `/run/ops/web.unit`。

接着，它会将自己的参数以及 `WEB_LOG` 写入 `/run/ops/web.args`，当前该文件内容为 `args=--port 8080` 和 `WEB_LOG=info`。


- 保持 `/usr/lib/systemd/system/ops-web.service` 原样不动，切勿在其位置或 `/etc/systemd/system`、`/run/systemd/system` 中放置该 unit 的完整副本。
- 使用 `sudo` 或 `systemctl edit` 将新的命令行 `/usr/local/sbin/ops-web --port 8090` 和 `WEB_LOG=debug` 写入 `/etc/systemd/system/ops-web.service.d/override.conf`。
  修改 ops-web 的每个 drop-in 都应放在同一目录下；放在 `/run` 下的文件在下次开机后就会丢失。
- 当 systemd 加载 drop-in 后，运行 `sudo systemctl restart ops-web.service` 并保持服务处于运行状态。

完成后，`/run/ops/web.args` 的内容必须为 `args=--port 8090` 和 `WEB_LOG=debug`，且 `/run/ops/web.unit` 必须显示软件包自带文件为 `FragmentPath`，并将您的 `override.conf` 显示在 `DropInPaths` 中。
重启命令返回时工作进程可能尚未完成这两个文件的重写，因此查看前请等待一两秒。

### 解答

```bash
# 写入 drop-in：清空 ExecStart= 后设置新命令，并追加 WEB_LOG=debug
sudo mkdir -p /etc/systemd/system/ops-web.service.d
sudo tee /etc/systemd/system/ops-web.service.d/override.conf >/dev/null <<'CONF'
[Service]
Environment=WEB_LOG=debug
ExecStart=
ExecStart=/usr/local/sbin/ops-web --port 8090
CONF
sudo systemctl daemon-reload
sudo systemctl restart ops-web.service

# 等待一两秒后检查
sleep 2
cat /run/ops/web.args /run/ops/web.unit
systemctl --no-pager cat ops-web.service
```
