### 读取 git status

你的工作内容存在于三个地方：工作区（working tree，文件当前的实际状态）、暂存区（index，下一次提交将包含的内容，也称为 staging）以及 HEAD（最后记录的快照）。
`git status` 会读取这三者的状态。

1. `git status`：分为三个部分。`notes.txt` 有已暂存待提交的更改，`app.js` 有尚未暂存的更改，而 `sketch.txt` 是未跟踪的文件。
2. `git status -s`：以两列形式展示相同的信息。左列：暂存区（index）。右列：工作区（working tree）。`M ` 表示已暂存，` M` 表示未暂存，`??` 表示未跟踪。
3. 暂存未跟踪的文件：`git add sketch.txt`。
4. 再次运行 `git status -s`：`??` 变成了 `A `，表示已暂存的新增文件。
