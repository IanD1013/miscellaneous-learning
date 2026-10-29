`ops-api.service` 运行了 `ExecStartPre=/usr/bin/test -f /run/ops/cache.ready`，因此在该文件存在之前它会拒绝启动。
`ops-cache.service` 负责创建该文件：
该 unit 是一个 oneshot 服务，其脚本会休眠三秒然后 touch 该文件，并且其 `RemainAfterExit=yes` 会在脚本退出后保持其处于 `active` 状态。
目前这两个 unit 均未启动，且 `/etc/systemd/system/ops-api.service` 中没有任何内容提及 cache。
现在启动 API，只会运行 API，因此其检查失败：

```console
$ sudo systemctl start ops-api.service
Job for ops-api.service failed because the control process exited with error code.
```

API 对 cache 有两个独立的需求：与它一起启动，以及让它先完成。
systemd 将它们表示为两种依赖关系，且二者互不蕴含。

### 需求依赖：Wants= 与 Requires=

一个 `systemctl start` 请求会变成一个事务（transaction），即 systemd 在运行任何 job 之前计算出的一组 job。
在 API 的 `[Unit]` 部分中添加 `Wants=ops-cache.service`，会在启动 API 的每个事务中为 cache 添加一个启动 job，且即便 cache 失败，API 仍会运行。
`Requires=ops-cache.service` 会添加相同的 job 并将这两个 unit 绑定在一起：
停止或重启 cache 会停止或重启 API，并且如果 cache 的启动 job 失败且 API 顺序在其之后，API 将不会被启动。
这两个设置都接受以空格分隔的 unit 列表。

二者都没有指定哪个 job 先运行。
仅配置 `Requires=` 时，两个启动 job 会同时运行，API 的测试会在 cache 脚本仍处于休眠状态时执行，你将得到相同的错误，此时 `systemctl is-active ops-cache.service` 会输出 `activating`。


### 顺序依赖：After= 与 Before=

`After=ops-cache.service` 会让 API 的启动 job 等待，直到 cache 的启动 job 完成。
oneshot 服务的启动 job 在其 `ExecStart=` 退出时完成，在这里即为文件写入之后。
`Type=simple` 服务的启动 job 在其进程被 fork 后就会立即完成，因此排在其之后永远不会等待它准备就绪。
`Before=` 是在另一个 unit 文件中书写的相同关系。
排序仅对事务中已有的 job 进行排列：
仅有 `After=` 时，启动 API 绝不会启动 cache，当 API 失败时 cache 仍然保持 `inactive`。

因此这两行需要搭配使用：

```ini
[Unit]
Requires=ops-cache.service
After=ops-cache.service
```

它们可以放在 `/etc/systemd/system/ops-api.service` 中，或者放在 `/etc/systemd/system/ops-api.service.d/override.conf` 的 drop-in 文件中。
执行 `sudo systemctl daemon-reload` 后，`systemctl --no-pager list-dependencies ops-api.service` 会打印 API 的依赖需求树，此时 `ops-cache.service` 应该直接出现在 API 下方，在运行前标记为 `○`。

该依赖树遵循需求关系，而非顺序关系；添加 `--after` 可以列出 API 排在哪些服务之后。

### 任务

- API 必须在 cache 停止时随之停止，因此在上述任一文件中为 `ops-api.service` 添加一行 `Requires=` 和一行 `After=`，两者均指定 `ops-cache.service`。
  写入这些文件需要 `sudo` 权限。
- 重新加载 systemd，并仅通过 `sudo systemctl start ops-api.service` 启动 API。
  最终 `ops-api.service` 和 `ops-cache.service` 都必须处于 active 状态。

### 解答

```bash
# 用 drop-in 为 API 添加需求依赖和顺序依赖
sudo mkdir -p /etc/systemd/system/ops-api.service.d
sudo tee /etc/systemd/system/ops-api.service.d/override.conf >/dev/null <<'CONF'
[Unit]
Requires=ops-cache.service
After=ops-cache.service
CONF
sudo systemctl daemon-reload
sudo systemctl start ops-api.service

# 检查
systemctl --no-pager list-dependencies ops-api.service
systemctl is-active ops-api.service ops-cache.service
```
