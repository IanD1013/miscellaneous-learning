### 保留记录：--no-ff

feature 严格领先于 main，因此普通的 merge 会执行快进合并（fast-forward），历史记录中将不会留下该分支曾经存在过的任何痕迹。
团队通常希望保留这一痕迹。

1. `git merge --no-ff -m "merge branch feature" feature`：即使可以进行快进合并，也强制生成一个真正的双父提交 merge commit。
2. `git log --oneline --graph`：菱形结构。该分支的存在被永久记录下来，这是主动选择的结果。

`--no-ff` 是一种规范策略上的决定，而非技术上的决定：无论哪种方式，最终内容都完全相同，但在 log 中呈现的历史脉络却有所不同。
