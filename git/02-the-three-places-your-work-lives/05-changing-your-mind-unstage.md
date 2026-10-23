### 改变主意：取消暂存 (unstage)

暂存了太多内容？
有两个命令可以撤回操作，而且它们都不会改动你的实际文件。

1. `git status -s`：有两个文件已暂存。
2. `git restore --staged report.txt`：现代写法。修改会移出暂存区 (index) 并显示为未暂存状态；磁盘上的文件未受任何影响。`-S` 是缩写参数。
3. `git reset chart.js`：经典写法，效果完全相同。注意看 "Unstaged changes after reset:" 这一行，这是真实 git 的确切提示信息。
4. `cat report.txt`：你的修改依然存在。取消暂存绝不会删除你的工作成果。
