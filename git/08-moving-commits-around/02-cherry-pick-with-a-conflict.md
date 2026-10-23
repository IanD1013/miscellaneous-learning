### 遇到冲突时的 cherry-pick

cherry-pick 会将更改重新应用到新的基础上，但有时基础已经发生了变化：在此处，双方都修改了同一行 retries。
cherry-pick 会像 merge 一样暂停下来。

1. `git cherry-pick tuning`：CONFLICT（冲突）。`git status` 会显示未合并的路径，并且文件中包含实际的冲突标记。如果你想退出，`git cherry-pick --abort` 可以恢复到 pick 之前的状态；不过这次请继续保留在当前流程中。
2. 采用 pick 的更改来解决冲突：`echo retries=5 > config.txt`，然后执行 `git add config.txt`。
3. 完成操作：`git cherry-pick --continue`。复制的 commit 将带着它原始的提交信息被应用。
