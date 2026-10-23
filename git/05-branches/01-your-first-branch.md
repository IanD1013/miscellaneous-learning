### 你的第一个分支

分支不过是一个指向提交（commit）的可移动名称。
创建分支不会复制任何内容，也不会产生任何开销；它只是立起了一个路标。

1. `git branch idea`：一个新的名称，指向 main 所指向的同一个提交。没有发生其他任何事情。
2. `git branch`：列出它们。`*` 标记了 HEAD 所在的分支，仍然是 main。
3. `git branch -v`：同样的列表，附带每个分支的提交，证明 idea 和 main 当前指向同一个位置。
4. `git switch idea`：现在 HEAD 附加到了 idea 上。新的提交将移动 idea，而把 main 留在原地。
