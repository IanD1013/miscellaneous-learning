### 保持最新状态：fetch 和 pull

这一次远程仓库领先于你：一位队友发布了更新日志。
有两个命令可以让你保持最新状态。

1. `git fetch`：下载队友的提交，但不会改动你的本地工作。观察传输摘要，以及分支图谱中 `origin/main` 的上移。
2. `git status`：“落后 'origin/main' 1 个提交，并且可以快进（fast-forwarded）”。在 fetch 之前，status 会认为你已经是最新的；这就是养成该习惯很重要的原因。
3. `git pull`：相当于 fetch 加上合并跟踪引用（tracking ref）。在这里这是一个干净的快进合并。运行 `ls` 可以看到 CHANGELOG.md 已经出现。
4. 回馈贡献：`echo v2 shipped >> README.md`，然后运行 `git commit -am "note the v2 ship"`。
5. `git push`：你的提交被推送到远端，`origin/main` 随即移动以保持一致。
6. `git status`：已是最新状态。你与远程仓库完全一致。
