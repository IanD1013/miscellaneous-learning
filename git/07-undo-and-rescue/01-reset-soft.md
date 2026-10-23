### reset --soft

你用一条 "wip" 提交信息提交了半个功能。
与其在其上堆叠第二个提交，不如把第一个提交撤回到暂存区，然后交付一个整洁的提交。

1. `git reset --soft HEAD~1`：main 分支后退一个提交，且该提交包含的所有内容都会回到暂存区，处于已暂存且就绪的状态。你的工作区保持不变。
2. `git status -s`：完成一半的功能处于已暂存状态，就像你刚刚运行了 git add 一样。
3. 完成该功能并暂存完整的文件：`echo the rest of the feature >> feature.js`，然后 `git add feature.js`。
4. 将其重新合并为一个提交：`git commit -m "feature: complete and tidy"`。
5. `git log --oneline`：在原本 wip 提交的位置现在只有一个整洁的提交。

`--soft` 是最温和的 reset 模式：只有分支指针会移动。
