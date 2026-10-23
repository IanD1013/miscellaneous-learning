### 来自过去的文件

`story.md` 经历了三个版本，当前版本丢失了你喜欢的一些内容。
`git restore` 可以在不改动历史记录的情况下获取旧内容。

1. `git restore --source=HEAD~2 story.md`：仅将第一个版本提取到你的工作区（working tree）中。暂存区（index）仍保留着最终文本，因此 `git status` 会将其显示为未暂存的修改。
2. `git status`，然后运行 `git diff`：将这次时光穿梭视为普通的未暂存更改。
3. 改变主意了？`git restore story.md`：普通形式会从暂存区恢复，而暂存区从未离开过当前状态。你又回到了最终文本。

`--source` 接受任何指向 commit 的标识：`HEAD~2` 或复制的 id。
