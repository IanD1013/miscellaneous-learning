### 书签：轻量标签

轻量标签（lightweight tag）只是一个指向特定 commit 的纯名称，就像一个永远不会移动的分支。
非常适合用作私有书签。

1. `git tag milestone`：在 HEAD 处创建一个标签。没有发生其他任何事情。
2. `git tag`：列出已有的标签。
3. 标签可以指向任何位置，而不仅限于 HEAD：`git tag first-cut HEAD~2` 可以为较早的 commit 添加书签。
4. `git log --oneline`：修饰信息（decorations）会显示各个标签所在的 commit。
5. 书签是可以随意丢弃的：`git tag -d first-cut` 会移除该名称。commit 仍然保留，不受任何影响。
