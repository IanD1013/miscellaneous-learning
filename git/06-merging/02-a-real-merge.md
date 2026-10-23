### 一次真正的合并

这一次两个分支都有了新的推进：main 分支接入了 analytics，而 feature 分支构建了搜索框，且修改位于不同的文件中。
合并需要真正的结合，git 会将其记录为一个拥有两个父提交（parent）的 commit。

1. `git log --oneline --all --graph`：查看这两条路线。
2. `git merge feature`：没有冲突，因为分支修改了不同的文件。Git 会自行写入合并 commit："Merge made by the 'ort' strategy."
3. 认识 `^2`：`git show HEAD^2` 会显示该合并的第二个父提交，即 feature 的最新提交（tip）。`^1` 是你当时所在的分支。在这里，脱字符（caret）后面的数字终于发挥了作用。
4. `git log --graph --oneline`：菱形结构，两条路线汇合到了一起。
