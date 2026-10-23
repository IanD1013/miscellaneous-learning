### rebase --skip 和 --abort

从暂停的 rebase 中退出的另外两种途径，分别适用于不同的情况。

首先是 `--skip`，用于在新基线上已经废弃过时的 commit。
你当前位于 feature 分支，正在变基到 main 分支。
feature 上的第一个 commit 设置了 demo 模式，而 main 分支随后将其覆盖为 production 模式，且你同意采用 main 的设置。

1. `git rebase main`：在 mode 冲突处暂停。
2. 这个 commit 不值得去解决冲突；丢弃它：`git rebase --skip`。demo 相关的 commit 随即消失，rebase 顺利重放 fixtures 相关的 commit。`config.txt` 中的内容为 mode=production，并且 `git log --oneline` 显示被跳过的 commit 已经不复存在。

其次是 `--abort`，用于整个 rebase 根本不可行的情况。

3. `git switch experiment`：第二个分支正在等待。
4. `git rebase main`：遇到另一个 mode 冲突。
5. 你今天完全不想处理这些：`git rebase --abort`。分支完全恢复到 rebase 开始前的状态。
