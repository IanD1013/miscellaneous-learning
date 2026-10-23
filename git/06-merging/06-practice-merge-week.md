### 练习：合并周

有三个分支正在等待合并，每种类型各一个。
将它们全部合并到 main 中。

1. `git merge quickfix`：严格领先，因此这次会进行 fast-forward（快进合并）。
2. `git merge --no-ff -m "merge docs" docs`：docs 也严格领先，但这次记录很重要，因此强制生成 merge commit。
3. `git merge rewrite`：这个会产生冲突，两边都重写了 rose 那一行。
4. 偏向 rewrite 来解决冲突：`echo roses are scarlet > poem.txt`，然后运行 `git add poem.txt`。
5. 结束合并：`git commit -m "merge rewrite"`。
6. `git log --graph --oneline`：一周的合并操作，在分支泳道中呈现出三种不同的形态。
