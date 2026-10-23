### 一步完成创建与切换

创建分支并立即切换到该分支是非常常见的操作，因此 git 为此提供了一个专用参数。

1. `git switch -c feature`：一步完成创建与切换。这是现代写法。
2. `git checkout -b hotfix main`：经典写法，这里带有一个可选的起始点。无论你当前位于何处，新分支都会从 main 开始。
3. `git branch -v`：三个分支，并且你当前位于 hotfix。

两种写法都可以指定起始点；`git switch -c` 接受起始点的方式与此处的 `checkout -b` 完全相同。
