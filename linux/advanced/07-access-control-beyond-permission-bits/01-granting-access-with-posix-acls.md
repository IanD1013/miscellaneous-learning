POSIX 访问 ACL 允许文件在所有者（owner）、所属组（owning group）和其他人（other）这三组权限基础之上，为特定账户授予权限。
每个额外的授权项可以是一个具名用户条目（`u:NAME:PERMS`）或具名用户组条目（`g:NAME:PERMS`）。
`setfacl -m ENTRY FILE` 用于添加或修改条目，并将其合并到文件现有的 ACL 中；`setfacl -x u:NAME FILE` 用于删除条目；`getfacl FILE` 用于打印完整列表。
默认的 `getfacl` 会以三行注释开头，分别注明文件名、所有者和所属组；`getfacl -c` 则会省略这些注释，只打印权限条目。
在此处，一个由 `opsfin` 拥有且权限模式为 0600 的临时文件仅向 `opsguest` 授予了读取权限（`install` 使用指定的所有者和权限模式创建该空文件）：

```console
$ sudo install -m 0600 -o opsfin -g opsfin /dev/null /srv/ops/ledger/scratch.csv
$ sudo setfacl -m u:opsguest:r /srv/ops/ledger/scratch.csv
$ getfacl -c /srv/ops/ledger/scratch.csv
getfacl: Removing leading '/' from absolute path names
user::rw-
user:opsguest:r--
group::---
mask::r--
other::---
```

第一行仅是 stderr 上的提示信息。
`user::`、`group::` 和 `other::` 是权限模式（mode）的三元组，保持原样；对于包含具名条目的文件，`ls -l` 会在其权限模式后加上一个 `+`。

这些文件位于 `/srv/ops/ledger`，这是为本节课程挂载的一个小型 tmpfs，因为该虚拟机的主根文件系统无法存储 ACL。

### mask（掩码）

`mask::` 条目是任何具名条目或所属组所能拥有的最大权限上限。
一旦文件包含具名条目，`ls -l` 和 `stat` 打印的组权限位实际上表示的是掩码（mask），而不是所属组本身的权限。
除非传递 `-n`，否则 `setfacl -m` 会重新计算掩码以覆盖所有条目，而 `chmod` 则会将其组权限位写入掩码中。
因此，`ls -l` 现在显示为 `-rw-r-----+`，如果使用 `chmod g-r` 试图阻止该组访问，反而会削减具名条目的权限，并且 `getfacl` 会使用 `#effective` 注释标出这一权限丢失：

```console
$ sudo chmod g-r /srv/ops/ledger/scratch.csv
$ getfacl -c /srv/ops/ledger/scratch.csv
getfacl: Removing leading '/' from absolute path names
user::rw-
user:opsguest:r--               #effective:---
group::---
mask::---
other::---
```

该条目虽然仍显示为 `r--`，但 `opsguest` 已无法再进行读取。
`m::PERMS` 将掩码作为独立的条目来指定，因此 `sudo setfacl -m m::rw /srv/ops/ledger/scratch.csv` 可以在不改变 `group::---` 的情况下提高掩码权限。
随后 `getfacl -c` 将列出 `user:opsguest:r--`，在 `mask::rw-` 旁边不会有 `#effective` 注释：掩码仅起上限限制作用，因此其包含的 `w` 不会向 `opsguest` 授予该条目尚未拥有的权限。

尝试以各个账户的身份进行读取，以观察条目生效情况。
`sudo runuser -u NAME -- COMMAND` 可以作为另一个账户运行单条命令，这也是稍后快速以 `auditor` 身份测试读取 ledger 文件的便捷方式。
然后删除该临时文件，使 ledger 目录恢复为仅包含两个任务文件：

```console
$ sudo runuser -u opsclerk -- cat /srv/ops/ledger/scratch.csv
cat: /srv/ops/ledger/scratch.csv: Permission denied
$ sudo runuser -u opsguest -- cat /srv/ops/ledger/scratch.csv
$ sudo rm -- /srv/ops/ledger/scratch.csv
```

尽管 `opsclerk` 属于 `opsfin`，但由于 `group::---` 从未更改，因此它的访问被拒绝。
属于组外的 `opsguest` 则通过其自身的条目读取了该空文件，因此 `cat` 没有输出任何内容，也没有报错。

这两个 ledger 文件中，有一个已经包含了被掩码所取消的 `auditor` 条目；对每个文件执行 `getfacl` 可以查看是哪一个。

将 `auditor` 添加到 `opsfin` 组中并不是替代方案。
所属组的条目是 `---`，提高该权限以允许 `auditor` 访问也会同时允许该组的所有其他成员访问。

### 要求

两个文件的所有权均为 `opsfin:opsfin`（uid 和 gid 均为 2001），权限模式为 0600。
`opsclerk` 是 `opsfin` 的成员；`opsguest` 不属于任何相关组。
`getfacl` 无需 `sudo` 即可运行，而 `setfacl` 则需要。

- `auditor` 可以读取 `/srv/ops/ledger/q3.csv` 和 `/srv/ops/ledger/q4.csv`，且不能向两者中的任何一个写入数据。
- `opsclerk` 和 `opsguest` 均无法读取这两个文件。
- 其他任何人均不能获得额外权限：`group::` 和 `other::` 保持为 `---`，且这两个文件上针对用户或组的任何其他具名条目均不授予任何权限。
- 两个文件均保持为由 `opsfin:opsfin` 拥有的常规文件。
- 不修改账户配置：`auditor` 保留其自身的 uid 且不加入 `opsfin`，而 `opsclerk` 仍留在 `opsfin` 中。

### 解答

```bash
# 先查看两个文件现有的 ACL（其中一个已有被掩码取消的 auditor 条目，可能还有其他具名条目）
getfacl /srv/ops/ledger/q3.csv /srv/ops/ledger/q4.csv

# 删除所有具名条目和掩码，只保留 user::rw- group::--- other::---（所有者和模式不变）
sudo setfacl -b /srv/ops/ledger/q3.csv /srv/ops/ledger/q4.csv

# 只给 auditor 添加只读条目，setfacl 会把掩码重新计算为 r--
sudo setfacl -m u:auditor:r /srv/ops/ledger/q3.csv /srv/ops/ledger/q4.csv

# 验证 ACL：只应有 user::rw-、user:auditor:r--、group::---、mask::r--、other::---
getfacl -c /srv/ops/ledger/q3.csv /srv/ops/ledger/q4.csv
ls -l /srv/ops/ledger

# 验证读取：auditor 成功，opsclerk 和 opsguest 被拒绝
sudo runuser -u auditor -- cat /srv/ops/ledger/q3.csv /srv/ops/ledger/q4.csv
sudo runuser -u opsclerk -- cat /srv/ops/ledger/q3.csv
sudo runuser -u opsguest -- cat /srv/ops/ledger/q4.csv
```
