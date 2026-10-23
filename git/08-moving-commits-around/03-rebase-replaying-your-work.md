### rebase：重放你的工作

你的特性分支是在 main 进行日志提交之前分叉出来的。
merge 会将两条路线合并；而 rebase 则会将你的提交逐个在新的 main 之上重新重放（replay），从而使历史记录保持为一条直线。

1. `git log --graph --all --oneline`：变基前的状态，呈现两条路线。
2. `git rebase main`：你的两个搜索相关的提交将作为全新的 commit 重放在 main 的最新提交之上。相同的更改内容，新的 commit id，新的基准。
3. `git log --graph --all --oneline`：变基后的状态，一条笔直的单线，你的工作位于最顶部。

说明提示：本环境采用线性变基。
此处不支持交互式 rebase（interactive rebase）；重新排序和 squash 属于在本地计算机上使用完整 Git 时的进阶内容。
