### 练习：撤销操作分类处理

三个工单，一个仓库，三种不同的撤销工具。
为每个工单选择合适的操作。

1. 工单一：一个临时 hack 即将被发布。首先复现它：`echo temp hack >> config.js`，然后执行 `git add config.js`。
2. 取消暂存它：`git reset config.js`。
3. 决定彻底放弃这些更改：`git restore config.js`。
4. 工单二：最新的 commit 说明为 "fix the loign bug"。原地修改该信息：`git commit --amend -m "fix the login bug"`。
5. 工单三："log passwords to console" 这个 commit 必须被公开撤销。它位于最新 commit 的前一个位置：`git revert HEAD~1`。
6. `git log --oneline`：确认获得干净的最新 commit 信息，以及一条清晰记录在案的 revert。
