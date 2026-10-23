### 认识终端

你将运行的每一个 git 命令都始于这里：终端。
在 git 登场之前，先来熟悉五个用于创建和读取文件的小命令。

1. `ls`：列出当前文件夹中的文件。已经有一个文件在等你了。
2. `cat guide.txt`：打印文件的内容。
3. 使用 `echo` 创建文件：`echo my first file > notes.txt`。`>` 箭头会将文本写入文件，并替换原有的任何内容。
4. 追加到末尾而不是替换：`echo a second line >> notes.txt`。双箭头表示追加。
5. `touch scratch.txt`：创建一个空文件。
6. 查看你的操作结果：`cat notes.txt`。

箭头前后无论是否有空格都可以正常运行：`echo hi > file.txt` 和 `echo hi >file.txt` 的效果相同。
