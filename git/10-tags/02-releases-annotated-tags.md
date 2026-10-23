### 发布版本：附注标签

附注标签（annotated tag）是一个独立的对象，拥有自己的作者、日期和附注信息。
这正是发布版本（release）所需要的。

1. `git tag -a v1.0 -m "first stable release"`。好奇如果不加 message 会发生什么吗？先试试 `git tag -a oops`：操作会被拒绝，因为当前环境没有可供调用的编辑器来提示你输入。
2. `git show v1.0`：查看标签头部信息、Tagger、Date、附注信息，接着是它所指向的 commit。只有附注标签才会显示该头部信息。
3. 作为对比，创建一个轻量标签：`git tag draft`。
4. `git show draft`：直接显示 commit 内容，没有头部信息，因为并没有创建标签对象。
5. 给错误的 commit 打了标签？`-f` 可以移动标签：`git tag -f draft HEAD~1`。
6. 用完之后清理该书签：`git tag -d draft`。
