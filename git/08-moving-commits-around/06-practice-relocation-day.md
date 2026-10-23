### 练习：迁移之日

在一个稍大的仓库上，接连执行本章学到的两个操作。

1. hotfix 上的舍入修复今天需要随 main 一起发布：`git cherry-pick hotfix`。
2. 礼品包装相关的工作应该置于最新的 main 之上。`git switch feature`，然后执行 `git rebase main`。两个 feature 提交都会顺利重放；它们的文件从未与 main 发生冲突。
3. `git log --graph --all --oneline`：main 包含了挑拣过来的修复，feature 则呈直线位于 main 之上。
