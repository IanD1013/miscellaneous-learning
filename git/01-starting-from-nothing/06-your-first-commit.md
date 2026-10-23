### 你的第一次提交

提交（commit）是带有说明信息的永久快照。
两个操作构成一次提交：`git add` 选择要包含的内容，`git commit` 记录它。
这个仓库刚刚完成初始化，你的日志正等待处理。

1. 如上一课所示设置你的身份信息：`git config user.name "Ada Lovelace"`，然后运行 `git config user.email ada@example.com`。
2. `git add journal.md`：文件状态从未跟踪（untracked）变为已暂存（staged）。已暂存意味着“将包含在下一次提交中”。
3. `git commit -m "my first commit"`：快照已被记录，同时附带你的提交说明。
4. `git log`：查看你的提交及其 Author 行。这就是你所配置的身份信息。
