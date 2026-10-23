### 从容应对 Detached HEAD

通常 HEAD 指向一个分支。
如果直接将其指向某个 commit，Git 就会提示进入了“detached HEAD”（头指针分离）状态。
这听起来像受了重伤，但实际上它只是只读的“观光模式”，外加一条规则。

1. `git log --oneline`：查看历史记录。分支 `first-release` 仍标记在较早的 commit 上。
2. 回到过去：`git switch --detach first-release`。（从日志中复制 commit ID 并运行带有该 ID 的 `git checkout` 也会到达相同的位置。）仔细阅读 Git 输出的信息。
3. `cat app.js`：查看旧代码，完全是当时的样子。
4. 结束观光：`git switch main`。重新关联分支，回到分支顶端。
5. 唯一的一条规则：在分离状态下进行的工作不属于任何分支。让我们来实操一下：再次使用 `git switch --detach first-release` 进入分离状态。
6. 进行实验：`echo experimental idea > lab.txt`、`git add lab.txt`、`git commit -m "a detached experiment"`。这个 commit 处于任何分支都无法看到的位置。
7. 离开前抢救它：`git switch -c rescue`。现在该 commit 已经有了归属的分支。
