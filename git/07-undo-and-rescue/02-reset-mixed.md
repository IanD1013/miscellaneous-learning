### reset --mixed

默认的 reset 模式。
与 `--soft` 类似，它会使分支回退，但它还会重置暂存区（index）以匹配较早的提交：这些更改会保留在你的工作区中，处于未暂存状态，等待被重新选择。

1. `git reset HEAD~1`（mixed 是默认模式，无需添加标志）：分支向后回退，该提交的更改会显示为未暂存的修改。请阅读 "Unstaged changes after reset:" 这一行。
2. `git status`：已修改，未暂存。与 --soft 对比，在 --soft 下它们原本是处于已暂存状态的。
3. 深思熟虑后重新选择：`git add notes.md`。
4. 再来一个熟悉的操作：`git reset notes.md`。同一个词，不同的任务：指定路径时，reset 仅取消暂存该文件，不会移动分支。你在暂存章节中遇到过这个操作。

两种任务，同一个命令名称：指定提交（如 `HEAD~1`）的 `reset` 用于移动分支，指定路径（如 `notes.md`）的 `reset` 用于编辑暂存区。
