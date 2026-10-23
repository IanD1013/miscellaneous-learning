### reset --hard 与 reflog 救援

最新的提交是一个错误。
将其清除，然后使用 reflog 恢复最近的 reset 操作。

1. `git reset --hard HEAD~1`：main 分支回退到要保留的提交，与其他 reset 模式不同的是，你的工作区（working tree）也会同步更新。现在运行 `git log` 显示的历史记录就像这个错误从未发生过一样。
2. 从 log 中消失并不代表彻底消失。`git reflog`：记录了 HEAD 曾经指向过的每一个位置，包括被清除的提交，按时间倒序排列（最新的在最前）。
3. 消除恐慌：从 reflog 中复制被清除提交的 id，并针对该 id 运行 `git reset --hard`。（初始环境也将该提交标记为了 `lifeline` 标签，因此 `git reset --hard lifeline` 也会达到相同的效果。）

`--hard` 是唯一会覆盖工作区（working tree）的 reset 模式。
最近的 hard reset 通常可以通过 reflog 恢复；reflog 条目会过期，且不可达的对象随后可能会被修剪（pruned）。
