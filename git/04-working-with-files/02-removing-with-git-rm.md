### 使用 git rm 进行删除

删除一个已跟踪的文件包含两个部分：从磁盘中移除以及告知 git。
`git rm` 可以一步完成这两件事，并且它非常注重你的数据安全。

1. 首先是繁琐的方式。`rm notes.txt`（普通 shell 命令）仅从磁盘删除文件。`git status` 会显示一个未暂存的删除：git 注意到了，但尚未暂存任何更改。
2. 在继续之前将其恢复：`git restore notes.txt`。你之前见识过 restore 的 `--staged` 形式用于取消暂存；而普通形式则是从暂存区恢复工作区，因此撤销未暂存的删除与撤销未暂存的编辑操作是一样的。
3. git 的方式：`git rm old-config.txt`。一步操作即可从磁盘移除并且已暂存该删除操作。
4. 安全机制：`git rm draft.txt` 会被拒绝，因为该文件包含可能会丢失的本地修改。查看拒绝信息，然后做出最终决定：`git rm -f draft.txt`。
5. 第三种模式：`git rm --cached secrets.txt` 会暂存删除操作，但将文件保留在磁盘上。这非常适合“这个文件本就不该被跟踪”的情况。
6. 记录所有更改：`git commit -m "clean house"`。
7. `git status`：secrets.txt 显示为未跟踪。文件仍在磁盘上，但不再由 git 管理。
