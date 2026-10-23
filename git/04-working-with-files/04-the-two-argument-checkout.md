### 带有两个参数的 checkout

`restore --source` 的前辈是带有提交和路径的 `git checkout`，例如这里的 `git checkout HEAD~2 -- story.md`。
它的影响范围更大：它会将旧内容同时写入暂存区（index）和工作区（working tree）。

1. `git checkout HEAD~2 -- story.md`：初稿恢复了，并且 `git status -s` 显示该更改已暂存，随时可以提交。将此与保留暂存区不变的 `restore --source` 进行对比。
2. `git status -s`：确认已暂存状态。
3. 分两步将其全部撤销：`git restore --staged story.md`（将暂存区恢复到当前状态），然后执行 `git restore story.md`（将工作区恢复到当前状态）。

相同的目标文件，不同的影响范围。
通过询问自己来做出选择：我是否希望它已经被暂存？
