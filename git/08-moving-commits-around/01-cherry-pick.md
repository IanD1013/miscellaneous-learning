### cherry-pick

hotfix 分支只包含一个 commit，即崩溃修复补丁。
你希望将该 commit 应用到 main，而不是合并整个分支。
`git cherry-pick` 可以将单个 commit 复制到任何地方。

1. `git log --oneline --all`：查看位于其独立分支上的补丁。
2. `git cherry-pick hotfix`：补丁的副本落入 main 分支。相同的变更，相同的 message，全新的 id。
3. `git log --oneline`：该副本成为你当前的 tip。原始 commit 仍然原封不动地留在 hotfix 上；cherry-pick 只会复制，从不移动。
