### 练习：玩转分支

将本章学到的所有内容连贯地实践一遍。

1. `git switch -c feature-a`：创建新分支并切换过去。
2. 提交一些内容：`echo alpha > a.txt`，`git add a.txt`，`git commit -m "feature-a: first cut"`。
3. `git switch -c feature-b main`：创建第二个分支，特意从 main 开始，而不是从当前位置。
4. 同样在该分支上提交：`echo beta > b.txt`，`git add b.txt`，`git commit -m "feature-b: first cut"`。
5. feature-a 获得了一个正式名称：`git branch -m feature-a payments`。
6. 预置的 stale-experiment 分支早已过时：`git branch -d stale-experiment`。
7. `git log --graph --all --oneline`：两条新的分支轨迹，一条已重命名，废弃的分支已删除。
