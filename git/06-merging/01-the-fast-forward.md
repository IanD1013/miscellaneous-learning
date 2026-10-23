### 快进合并（fast-forward）

当你要合并的分支严格领先于当前分支时，无需进行任何内容合并。
Git 只是直接将你的分支指针向前推进。
这就是快进合并（fast-forward），并且完全不会产生 merge commit。

1. `git log --oneline --all`：feature 正好领先 main 一个 commit，呈一条直线。
2. `git merge feature`：查看输出内容。包含 "Fast-forward" 以及指针移动前后的两个 id。
3. `git log --oneline`：main 和 feature 现在指向同一个 commit，历史记录仍然是一条直线。没有创建 merge commit，因为并不需要。
