Bash 不会直接将未加引号的变量值原样传递给命令。
它首先会在每个空格、制表符和换行符处分割该值，这就是**单词分割**（word splitting）。
接着进行的是**文件名展开**（filename expansion）：每个包含通配符（例如 `*`）的生成词都会被替换为与其匹配的文件名（如果有匹配的话）。
一个文件名可能会变成两个参数，或者变成其他文件的列表。

`archive-upload.sh` 位于你 Shell 启动时的目录 `~/bash-lab` 中，它将一个文件从 `incoming/` 移动到 `archive/`。
在脚本内部，`$1` 是调用者传递的第一个参数，在此处即为文件名：

```bash
#!/bin/bash
cd incoming || exit 1
cp $1 ../archive/
rm $1
```

以下三个名称展示了当 `incoming/` 中有其他文件与目标文件并存时，未加引号的 `$1` 会产生什么后果：

- `monthly report.txt` 会被分割为 `monthly` 和 `report.txt`。cp 会将具有这两个名称的文件复制到 `archive/`，rm 会从 `incoming/` 中删除它们，而 `monthly report.txt` 本身完全没有被移动。
- `*.log` 会匹配所有以 `.log` 结尾的名称，因此 `app.log` 和 `db.log` 会与实际名为 `*.log` 的文件一起被移动。
- `-rf` 会被 cp 读取为选项 `-r` 和 `-f`。由于只剩下 `../archive/`，cp 会报错停止，而 rm 只收到了选项却没有收到文件名，因此什么也不会删除。脚本最终仍然以状态码 0 退出，而文件 `-rf` 留在 `incoming/` 中。

与命令注入不同，这里不会启动第二条命令：调用者的输入改变的是脚本自身 cp 和 rm 的参数。

在变量两边加上**双引号**，Bash 就会跳过对它的单词分割和文件名展开。
Bash 仍会将 `"$1"` 替换为其值，但会将其作为恰好一个参数传递给命令，包括其中的空格和 `*`。
以文件夹中名为 `q3 budget.csv` 的文件为例：

```text
$ name='q3 budget.csv'
$ cat $name
cat: q3: No such file or directory
cat: budget.csv: No such file or directory
$ cat "$name"
region,total
north,1200
```

单引号在这里不起作用。
Bash 不会展开单引号中的任何内容，因此 `'$1'` 只是字符 `$` 和 `1`，cp 会去查找具有该名称的文件。

加引号可以使 `-rf` 保持为一个参数，但 cp 和 rm 仍然会将以破折号开头的参数读取为选项。
输入变成命令本不应接收的选项，这种情况称为**参数注入**（argument injection）。
参数 `--` 标志着**选项的结束**：命令会将其后的每个参数都视为文件名，即使它是以破折号开头的。
`--` 应当位于任何真正的选项之后、文件名之前；如果把 `--` 放在文件名之后就太迟了，因为该名称已经被读取为选项了。
在这里，用于统计文件行数的 `wc -l` 接收了一个名为 `-n` 的文件：

```text
$ name='-n'
$ wc -l "$name"
wc: invalid option -- 'n'
Try 'wc --help' for more information.
$ wc -l -- "$name"
3 -n
```

### 修复 archive-upload.sh

修改 cp 和 rm 行，使它们各自都将 `$1` 视为恰好一个文件名。
完成后的脚本应将指定的文件从 `incoming/` 移动到 `archive/`，将 `incoming/` 中的其他所有文件保留在原处，并以状态码 0 退出。
它始终只接收恰好一个名称（对应 `incoming/` 中的一个文件），并且必须能够正确处理 `monthly report.txt`、`*.log` 和 `-rf`。
保持代码行 `cd incoming || exit 1` 不变：脚本是从 `~/bash-lab` 运行的，并从该路径查找这两个文件夹。
使用 `&&` 连接这两条命令也很有帮助，因为这样 rm 仅在复制成功后才会运行。

若要测试某个文件名，请使用 `incoming/` 前缀创建其测试文件，这样 touch 就不会把像 `-rf` 这样的名称读取为选项。
无论在创建测试文件还是在运行脚本时，都要对任何包含空格或 `*` 的名称加上引号，然后列出两个文件夹的内容：

```bash
touch 'incoming/monthly report.txt' incoming/monthly incoming/report.txt
bash archive-upload.sh 'monthly report.txt'
ls incoming archive
```

此时 `archive/` 中应该只有 `monthly report.txt`。
`ls` 会用引号打印包含空格或 `*` 的名称，这些引号并不是文件名的一部分。
