### 比较两个提交

`git diff` 不仅可用于未提交的工作。
传入两个提交，它就会显示两者之间的所有变更。

1. `git log --oneline`：了解当前状态并复制几个 ID。
2. `git diff HEAD~1 HEAD`：最新提交所做的更改。顺序很重要：从哪个提交（from），到哪个提交（to）。
3. `git diff HEAD~3 HEAD`：在一个视图中查看三个提交的变更量。
4. `git diff <a> <b>` 使用两个复制的 ID：按名称进行相同的比较。
