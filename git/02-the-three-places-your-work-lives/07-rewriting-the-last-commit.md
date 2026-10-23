### 重写最后一次提交

`--amend` 会替换最后一次提交，而不是添加一个新提交。
可以用它来解决两种常见的疏忽：写错了提交信息和遗漏了文件。

1. `git log --oneline`：最新的提交显示为 "add losing screen"。这不是你的本意。修正该信息：`git commit --amend -m "add loading screen"`。
2. 你还遗漏了配置文件。创建并暂存它：`echo fullscreen=true > settings.ini`，然后执行 `git add settings.ini`。
3. 将暂存的文件合并到最新提交中，保持一个整洁的提交：`git commit --amend -m "add loading screen and settings"`。
4. 有时你需要一个完全没有变更的提交作为标记。在没有暂存任何内容时，普通的 `git commit -m` 会被拒绝；明确覆盖该行为的方式是 `git commit --allow-empty -m "nothing to see here"`。
5. `git log --oneline`：历史依然很短。这两次 amend 都替换了最新提交；它从未堆叠新的提交。

后续需要注意的一点：amend 会重写历史。
对于尚未共享的工作，这完全没有问题。
