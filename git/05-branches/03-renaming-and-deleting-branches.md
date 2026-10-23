### 重命名和删除分支

创建分支的成本很低，因此仓库中往往会积累很多分支。
日常整理有三个招式。

1. 重命名：`git branch -m wip-stuff cleanup`。相同的 commit，更好的名称。
2. 删除已合并的分支：`git branch -d cleanup`。它指向一个 main 已经包含的 commit，因此不会丢失任何内容，git 会静默允许该操作。
3. 删除未合并的工作：先尝试 `git branch -d spike`。Git 会拒绝，因为 spike 包含其他任何分支都没有的 commit。如果你确实想彻底删除它：`git branch -D spike`。
4. `git branch`：只剩下 main。
