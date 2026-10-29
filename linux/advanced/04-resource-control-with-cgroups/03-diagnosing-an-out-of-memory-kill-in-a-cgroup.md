`ops-index.service` 显示为 `active (running)`，但它的缩略图批处理任务始终无法完成，并且 `/srv/ops/index/thumbs.done` 从未出现。
在此虚拟机上每次读取 journal 都需要 `sudo`，因为 `learner` 不在 `adm` 或 `systemd-journal` 组中。
`sudo journalctl -u ops-index.service` 每隔几秒就会显示相同的失败信息：

```text
systemd[1]: ops-index.service: A process of this unit has been killed by the OOM killer.
index-batch[158]:        174 Killed                  | "/usr/local/lib/ops/$helper" -c "$window" > /dev/null
index-batch[158]: batch 2: a stage exited with status 137, retrying in 5 s
```

状态码 137 是 128 加上 9：
即 SIGKILL，发送给了批处理作为子进程运行的某个阶段程序。
宿主机大约有 180 MB 空闲内存。
该服务的 cgroup 内存要少得多，因为该 unit 设置了 `MemoryMax=32M`。


### 单个 cgroup 内部的 OOM killer

当 cgroup 的使用量达到 `memory.max` 且内核无法回收足够的页面使其降回限制之下时，**OOM killer** 会仅针对该 cgroup 运行。
它会在该 cgroup 自身的进程中挑选一个受害者（通常是使用内存最多的进程），并向其发送 SIGKILL。
`memory.events` 记录了各个阶段的计数：

```bash
cat /sys/fs/cgroup/system.slice/ops-index.service/memory.events
```

`max` 统计使用量触及限制的次数，`oom` 统计随后内存回收失败的次数，而 `oom_kill` 统计该 cgroup 中有多少进程被终止。
仅凭 `oom_kill` 也可能统计到因宿主机全局内存不足而丢失的进程；但若旁边的 `oom` 为非零值，则表明是该 cgroup 自身的限制触发了 kill。
这两个计数器都无法指出是谁被杀死了，unit 的日志也无法指出：
bash 在记录作业日志时未对 `$helper` 进行展开。
内核日志指明了受害者的名称：

```bash
sudo journalctl -k --no-pager | grep -i "out of memory"
```

每次 kill 都会打印 `Memory cgroup out of memory: Killed process N (name) ...`，其中 name 是被杀程序的文件名，绝不会是 unit 的名称。

该 unit 保持 active 状态是因为其 unit 文件设置了 `OOMPolicy=continue`，这指示 systemd 在 OOM killer 终止其子进程时保持该 unit 继续运行。
在这里，受害者是一个子进程，因此作为主进程的 bash 循环幸存下来并无休止地重试，这就是为什么 `systemctl status` 看起来一切正常。
如果主进程是被杀死的受害者，那么无论策略如何设置，该 unit 都会失败。

### 根据测得的峰值调整大小

移除限制可以让批处理完成，但在下次占用增长时也会让服务耗尽整台宿主机的资源。
凭猜测设置一个较大的数值可能仍然偏小。
`memory.peak` 保存了该 cgroup 自创建以来达到的最高使用量（以字节为单位），而在存在限制的情况下，它的读数绝不会高于该限制。
因此，解除正在运行的 unit 的上限，等待 `thumbs.done` 出现，然后读取峰值：

```bash
sudo systemctl set-property ops-index.service MemoryMax=infinity
cat /sys/fs/cgroup/system.slice/ops-index.service/memory.peak
```

该数值就是批处理的工作集大小。
将其除以 1048576 即可转换为 `M` 后缀所代表的 MiB，然后将 `MemoryMax=` 设置为其 1.2 到 1.5 倍，向上取整为整数 MiB。
下限保留了缓冲空间，以确保下次批处理稍大时不会被杀死；上限则使限制足够接近实际使用量，从而依然能够保护宿主机。
`set-property` 本身不输出任何内容，但你接下来运行的 `systemctl status` 或 `systemctl restart` 会发出警告，提示该 unit 的 drop-in 文件在磁盘上发生了更改。
新值已经应用于正在运行的 unit，因此该警告无需任何操作。

### 任务

- 将内核日志在括号中为被杀死进程打印的名称写入 `/home/learner/ops/oom-victim`。
- 将解除限制且批处理完成后测得的 `memory.peak` 读数保存到 `/home/learner/ops/index-peak`，必须是其打印的精确数值，不能是四舍五入或估算的数字。
- 通过 systemd 为 `ops-index.service` 设置为该峰值 1.2 到 1.5 倍的 `MemoryMax=`，并持久化保存以使其在重启后仍然有效，同时保持服务处于 active 状态。
  手动写入 `memory.max` 的数值只会更改正在运行的 cgroup：systemd 仍然保留 32M，并在下一次 `daemon-reload` 或重启时将其恢复。
- 在该限制下，`/srv/ops/index/thumbs.done` 必须存在。
  每当服务启动时，批处理都会删除该文件，并在所有三个阶段都成功后写入它，因此在重启后请等待它重新出现。

### 解答

```bash
# 确认是 cgroup 自身限制触发的 OOM（oom 和 oom_kill 均非零）
cat /sys/fs/cgroup/system.slice/ops-index.service/memory.events

# 从内核日志中找到被杀进程的名称，并写入括号中的名称
sudo journalctl -k --no-pager | grep -i "out of memory"
sudo journalctl -k --no-pager | grep -o 'Killed process [0-9]* ([^)]*)' | tail -n 1 \
  | sed 's/.*(\(.*\))/\1/' > /home/learner/ops/oom-victim
cat /home/learner/ops/oom-victim

# 解除正在运行的 unit 的上限，等待批处理完成
sudo systemctl set-property ops-index.service MemoryMax=infinity
while [ ! -e /srv/ops/index/thumbs.done ]; do sleep 2; done

# 保存精确的峰值读数
cat /sys/fs/cgroup/system.slice/ops-index.service/memory.peak > /home/learner/ops/index-peak
cat /home/learner/ops/index-peak

# 计算峰值的 1.3 倍并向上取整为整数 MiB（落在 1.2 到 1.5 倍之间）
peak=$(cat /home/learner/ops/index-peak)
mib=$(( (peak * 13 / 10 + 1048575) / 1048576 ))
echo "MemoryMax=${mib}M"

# 通过 systemd 设置并持久化新的限制（不带 --runtime）
sudo systemctl set-property ops-index.service MemoryMax=${mib}M

# 确认重新加载后仍是新值（没有其他 drop-in 覆盖它）
sudo systemctl daemon-reload
systemctl show -p MemoryMax ops-index.service
cat /sys/fs/cgroup/system.slice/ops-index.service/memory.max

# 重启后在新限制下等待 thumbs.done 重新出现
sudo systemctl restart ops-index.service
while [ ! -e /srv/ops/index/thumbs.done ]; do sleep 2; done
ls -l /srv/ops/index/thumbs.done
systemctl is-active ops-index.service
```
