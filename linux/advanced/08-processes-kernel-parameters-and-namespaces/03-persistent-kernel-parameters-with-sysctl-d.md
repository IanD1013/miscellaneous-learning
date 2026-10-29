`/proc/sys` 下的每个文件都是一个内核参数，其名称就是将路径中的斜杠替换为点号：
`/proc/sys/vm/swappiness` 就是 `vm.swappiness`。

读取该文件会显示运行时值（即内核当前使用的值），无需 `sudo` 使用 `cat` 即可读取。
以 root 权限写入会立即更改该值，但仅在内核内存中生效，因此下次启动时会再次从内核内置的默认值开始。
`sysctl` 命令通过点分名称读取和写入相同的值。
它位于 `/usr/sbin` 中，该路径不在 `learner` 的 PATH 中，因此即使仅读取也需要使用 `sudo` 运行：

```bash
sudo sysctl net.core.somaxconn
sudo sysctl -w vm.swappiness=10
```

### 在启动时应用参数

在启动时，`systemd-sysctl.service` 会应用四个目录下的 `*.conf` 文件：`/etc/sysctl.d`、`/run/sysctl.d`、`/usr/local/lib/sysctl.d` 和 `/usr/lib/sysctl.d`。

它并不是按顺序依次处理这些目录。
而是将所有四个目录中的文件名合并到一个列表中，按字典顺序对该列表进行排序并依次应用这些文件，因此对于两个文件都设置了的键，后应用的文件生效。
目录仅用于区分同名文件：
`/etc` 中的文件会替换其他三个目录中的同名文件。
这就是为什么这些文件以数字开头。
`/run` 在每次启动时都会被清空，因此必须持久保留的设置应放在 `/etc/sysctl.d` 中。

`sudo sysctl --system` 现在会按相同顺序应用这些文件并在执行时打印每个文件名，最后以 `/etc/sysctl.conf` 本身结束（systemd-sysctl 仅通过 `/etc/sysctl.d` 中指向它的 `99-sysctl.conf` 链接读取该文件）。
在这台机器上，`/etc/sysctl.conf` 仅包含注释，因此最后一步不会设置任何内容。
`sudo systemctl restart systemd-sysctl` 也会应用这些文件，但不会列出文件。

### 要求

`vm.swappiness` 设置内核将空闲进程内存换出到 swap 而不是丢弃文件缓存的倾向程度；数值越大意味着 swapping 越频繁。
`net.core.somaxconn` 限制监听套接字的 backlog，即等待程序 accept 的连接队列上限。
运行中的内核将它们分别设置为 60 和 4096；当前以及每次启动后，都需要将它们分别设置为 10 和 1024。
`/etc/sysctl.d/90-legacy.conf` 设置了 `vm.swappiness = 60` 以及平台团队负责的另外两个键，因此它必须保持完全不变。
每次更改都需要 `sudo`。


- 在 `/etc/sysctl.d` 中创建您自己的新 `.conf` 文件，将这两项设置分别写为一行 `key = value`，文件名应确保其值在启动时能够优先于 `90-legacy.conf` 生效。
- 使正在运行的内核使用 10 和 1024。
- 然后运行 `sudo systemctl start ops-sysctl-replay`。
  该 oneshot 服务会将这两个键重新设置为 60 和 4096，并对全新启动仍会找到的文件（即不包含 `/run/sysctl.d` 下的内容）运行 systemd-sysctl，从而使正在运行的内核显示启动后所获得的值。
  `/run/ops/sysctl-boot` 保存了这些文件在下次启动时提供的两个值，并且其最后一行指明 `90-legacy.conf` 是否仍是平台团队交付的文件。
  重放服务每次运行时都会重写该文件，因此在进行任何修复（包括对 `90-legacy.conf` 的更改）后，重新启动重放服务并读取该文件。
  其内容必须为：

```text
vm.swappiness = 10
net.core.somaxconn = 1024
/etc/sysctl.d/90-legacy.conf: unchanged
```


### 解答

```bash
# 查看各目录中是否还有文件设置这两个键
sudo grep -rn -e swappiness -e somaxconn /etc/sysctl.d /run/sysctl.d /usr/local/lib/sysctl.d /usr/lib/sysctl.d /etc/sysctl.conf
# 新建自己的配置文件，文件名按字典顺序排在 90-legacy.conf（以及其他所有文件）之后
printf 'vm.swappiness = 10\nnet.core.somaxconn = 1024\n' | sudo tee /etc/sysctl.d/99-zz-ops.conf
# 让正在运行的内核立即使用新值
sudo sysctl -p /etc/sysctl.d/99-zz-ops.conf
# 模拟启动并查看下次启动时得到的值
sudo systemctl start ops-sysctl-replay
cat /run/ops/sysctl-boot
```
