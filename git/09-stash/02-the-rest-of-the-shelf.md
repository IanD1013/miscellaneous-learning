### 储藏架的其他操作

储藏架可以容纳多个条目，并且 `pop` 也不是唯一的用法。
堆叠两个 stash，然后体验整个工具箱的功能。

1. 暂存当前的修改：`git stash push -m "first idea"`。
2. 创建并暂存第二个：`echo second idea >> notes.txt`，然后执行 `git stash push -m "second idea"`。
3. `git stash list`：显示两个条目。`stash@{0}` 是最新的（second idea），`stash@{1}` 是较旧的一个。`stash@{n}` 这种语法可以在任何 stash 命令中指定特定的条目。
4. `git stash apply`：恢复 `stash@{0}`，但与 pop 不同的是，它会将其保留在储藏架上。当你想在多个地方尝试这些修改时非常有用。
5. 刚刚应用的副本现在可以移除了：`git stash drop stash@{0}`。
6. 一键清空储藏架：`git stash clear`。全部清空。

过程中可以尝试一个无效地址，例如 `git stash drop stash@{9}`：其拒绝提示与真实的 git 完全一致。
