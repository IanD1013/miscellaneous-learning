两个额外的权限位（mode bits）可以将一个组可写的目录转变为可用的团队中转目录（drop）。
目录上的 setgid 位会使每个新文件和子目录继承该目录的所属组，而不是创建者的主组，并且新子目录也会获得该标志位。
粘滞位（sticky bit）增加了限制删除功能，类似于 `/tmp`：任何在目录中具有写权限的人仍然可以在其中创建文件，但只有文件的所有者、目录的所有者和 root 才能删除或重命名该文件。

这里的中转目录是 `/srv/ops/drop`，是为本课程挂载的一个小型 tmpfs，因为该虚拟机的主根文件系统无法存储 ACL。
它的初始状态为 `root:root`，权限模式为 0755。
组 `opsteam`（gid 2100）包含成员 `ana` 和 `ben`；账户 `reviewer` 在该组之外。
每次更改都需要 `sudo`。


如果没有 setgid，`ana` 创建的文件会归属于她的主组（名称同样为 `ana`）；有了 setgid，无论谁创建该文件，继承的组都是 `opsteam`。

并且对目录的写权限允许用户删除或重命名其中的任何条目，而不管该条目的所有者是谁，因此在模式 2770 下，`ben` 可以删除 `ana` 的文件。

这两个标志位位于通常的三位数字之前的一位：2 代表 setgid，1 代表 sticky，如果两个都需要则相加为 3。
`chmod g+s DIR` 和 `chmod o+t DIR` 分别设置其中一个位。
在更改中转目录本身之前，可以在其中的临时测试目录上尝试这些操作；组 `users` 和账户 `backup` 在本任务中不起任何作用：

```console
$ sudo mkdir /srv/ops/drop/scratch
$ sudo chgrp users /srv/ops/drop/scratch
$ sudo chmod 2770 /srv/ops/drop/scratch
$ ls -ld /srv/ops/drop/scratch
drwxrws--- 2 root users 40 Oct  8 01:35 /srv/ops/drop/scratch
$ sudo chmod o+t /srv/ops/drop/scratch
$ stat -c '%a %A' /srv/ops/drop/scratch
3770 drwxrws--T
```

`s` 表示在组执行权限之上设置了 setgid。
当 others 拥有执行权限时，粘滞位显示为 `t`；当没有执行权限时（如此处所示），显示为 `T`，并且 `stat` 会显示这两个标志位对应的首位数字 3。

### 默认 ACL

目录上的访问 ACL 条目（access ACL entry）仅对该目录生效；稍后在其中创建的文件绝不会看到它。
新文件复制的是默认 ACL（default ACL）。
在创建时，每个新文件和子目录都会将默认 ACL 作为自己的访问 ACL，新子目录还会保留它作为自己的默认 ACL，因此继承关系会沿目录树向下传递。
复制的权限受创建程序所请求模式的限制：其所有者、掩码（mask）和 other 条目仅保留该模式允许的位。
Shell 的 `>` 和 `touch` 对新文件请求的模式是 0666，而 `mkdir` 请求的是 0777，因此新文件的掩码最多为 `rw-`，其继承的 `x` 永远不会生效。
已存在的文件不会发生改变；要修改这些文件需要使用 `setfacl -R -m`。


`setfacl -d -m u:NAME:PERMS DIR` 添加一条默认条目。
在单个 `-m` 列表中，`d:` 前缀将单个条目标记为默认条目，因此 `setfacl -m u:NAME:PERMS,d:u:NAME:PERMS DIR` 可以在一条命令中同时设置访问条目和默认条目。
大写的 `X` 仅在目标是目录或已经具有执行位时才添加执行权限，因此在目录上它存储的内容与 `x` 完全相同。
在这里，`backup` 获得了对临时目录以及稍后在其中创建的所有内容的完全访问权限：

```console
$ sudo setfacl -m u:backup:rwx,d:u:backup:rwX /srv/ops/drop/scratch
$ getfacl -c /srv/ops/drop/scratch
getfacl: Removing leading '/' from absolute path names
user::rwx
user:backup:rwx
group::rwx
mask::rwx
other::---
default:user::rwx
default:user:backup:rwx
default:group::rwx
default:mask::rwx
default:other::---
$ ls -ld /srv/ops/drop/scratch
drwxrws--T+ 2 root users 40 Oct  8 01:35 /srv/ops/drop/scratch
```

`getfacl` 会给默认条目加上 `default:` 前缀。
第一个 `setfacl` 还填充了默认的所有者、组、other 和掩码条目，而 `ls` 在组权限位中显示的掩码仍为 `rwx`，因此模式仍然显示为 3770。
现在以 root 身份创建一个文件，并以 `backup` 身份创建一个文件（`sudo runuser -u NAME -- COMMAND` 会以该账户身份运行一条命令）：

```console
$ sudo touch /srv/ops/drop/scratch/root.txt
$ sudo runuser -u backup -- touch /srv/ops/drop/scratch/backup.txt
$ sudo ls -l /srv/ops/drop/scratch
total 0
-rw-rw----+ 1 backup users 0 Oct  8 01:35 backup.txt
-rw-rw----+ 1 root   users 0 Oct  8 01:35 root.txt
$ sudo getfacl -c /srv/ops/drop/scratch/backup.txt
getfacl: Removing leading '/' from absolute path names
user::rw-
user:backup:rwx                 #effective:rw-
group::rwx                      #effective:rw-
mask::rw-
other::---
```

`backup` 的主组是 `backup`，但它的文件却属于 `users`：这就是 setgid 的作用。
其 `user:backup` 这一行来自默认 ACL，而 `touch` 请求的 0666 让掩码保持为 `rw-`，因此 `#effective` 剥离了 `x`。

接下来测试粘滞位并删除临时目录，以便在开始操作中转目录前保持其为空：

```console
$ sudo runuser -u backup -- rm /srv/ops/drop/scratch/root.txt
rm: cannot remove '/srv/ops/drop/scratch/root.txt': Operation not permitted
$ sudo runuser -u backup -- rm /srv/ops/drop/scratch/backup.txt
$ sudo rm -r -- /srv/ops/drop/scratch
```

`backup` 可以在目录中写入，但粘滞位限制了它只能删除自己的文件。

仅凭默认条目并不能让所属组之外的账户读取目录中的新文件。
当目录的 other 位为 `---` 时，该账户还需要通过其自有的访问条目获得对目录本身的搜索权限（`x`），否则它无法访问内部的任何路径。

在首次执行 `setfacl` 之前，请先设置中转目录的组和模式。
当 `setfacl` 添加首批条目时，它会从目录当时的模式中复制所有者、组和 other 条目，因此在初始提供的 0755 目录上，访问 ACL 将获得 `group::r-x`，默认 ACL 将获得 `default:group::r-x` 和 `default:other::r-x`，而不是模式 3770 对应的 `rwx` 和 `---`。

之后再使用 `chmod` 也无法修复它们：一旦目录存在 ACL，chmod 的组权限数字设置的就是掩码，因此 `ls -ld` 显示为 `drwxrws--T+`，而 `getfacl` 仍列出 `group::r-x`，导致 `ana` 无法创建文件。
如需重新开始，可使用 `sudo setfacl -b /srv/ops/drop` 删除所有访问和默认 ACL 条目，并将 `group::r-x` 条目恢复到组权限位（模式 3750）；然后按顺序先设置模式，再重新添加条目。

### 需求

- `/srv/ops/drop` 保持所有者为 `root`，所属组为 `opsteam`，模式为 3770。
- `reviewer` 可以访问中转目录中的文件，并通过从目录默认 ACL 继承的专属命名条目读取每个新文件，而不是通过所属组或 other 读取。
  它不能更改这些文件，不在 `opsteam` 组中，也不能在中转目录中创建文件。
- 其他任何人不能从中转目录的默认 ACL 中获得任何权限：其中的任何其他命名条目要么属于 `opsteam` 或其成员之一，要么不授予任何权限，并且其 `other` 条目不授予任何权限。
- `sudo ops-drop-check` 用于运行中转检查并打印其记录：在 `dir=` 行上显示中转目录的 `stat -c '%a %u %g'`（模式、所有者 uid、所属组 gid），接着显示以 `ana` 身份创建文件、以 `reviewer` 身份读取、写入及创建文件、以及以 `ben` 身份删除 `ana` 文件的结果。
  `others=` 行通过数字 id 列出新文件继承的属于 `opsteam` 之外的账户或其他组的任何命名条目（例如 `user:65534:r--`），以及在授予任何权限时中转目录的默认 `other` 条目（例如 `other::r--`）。
  本练习在每次评分时都会运行相同的检查，因此在每次修复后再次运行该命令以查看当前进度。
  记录最终必须显示为：

```text
dir=3770 0 2100
group=opsteam
ben-delete=denied
reviewer-read=read
reviewer-write=denied
reviewer-create=denied
others=none
```

### 解答

```bash
# 先设置所属组和模式（setgid + sticky + rwxrwx---），再添加 ACL，
# 这样 setfacl 复制的 group:: 为 rwx，default:other:: 为 ---
sudo chgrp opsteam /srv/ops/drop
sudo chmod 3770 /srv/ops/drop

# reviewer：对目录本身只有搜索权限 x（不能创建文件），
# 默认条目 r 让每个新文件都继承只读的专属命名条目
sudo setfacl -m u:reviewer:x,d:u:reviewer:r /srv/ops/drop

# 验证目录的模式、所有者和 ACL
stat -c '%a %U %G' /srv/ops/drop
getfacl -c /srv/ops/drop

# 运行中转检查
sudo ops-drop-check
```
