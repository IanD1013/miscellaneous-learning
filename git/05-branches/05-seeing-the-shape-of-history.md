### 查看历史的形态

当前存在两个分支，且它们都即将增长。
通过你自己的提交让它们产生分叉，然后观察你所创建的历史形态。

1. 你当前位于 main 分支。扩展它：`echo main grows >> notes.txt`，然后执行 `git commit -am "main: extend the notes"`。
2. `git switch river`：切换到另一个分支，该分支仍然始于共同的起点。
3. 给 river 一个属于它自己的方向：`echo a different direction > river.txt`，`git add river.txt`，`git commit -m "river: a different direction"`。
4. 全貌呈现：`git log --graph --all --oneline`。两条轨道从一个提交分出：`--all` 会包含除当前分支之外的其他分支，`--graph` 会绘制出轨道，且分支名称在此处始终会带有装饰显示。
