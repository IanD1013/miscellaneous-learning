### 让 git 视而不见：.gitignore

某些文件属于你的文件夹，但绝不应该进入版本历史：日志、构建输出、临时草稿文件。
如果放任不管，它们会扰乱每次 `git status` 的输出，并会被 `git add .` 一并卷入。
一个名为 `.gitignore` 的文件可以列出它们，随后 git 便不再提及它们。

1. `git status`：有三个未跟踪的文件，但只有 `notes.txt` 值得保留。`debug.log` 和 `scratch.tmp` 都是干扰项。
2. 创建忽略文件：`echo debug.log > .gitignore`。再次运行 `git status`：debug.log 已从列表中消失。文件并未被删除，只是不再归 git 管辖。
3. 模式匹配可以覆盖整个文件类别：`echo '*.tmp' >> .gitignore`。再执行一次 `git status`：scratch.tmp 也被隐藏了，连同该项目未来可能产生的所有 .tmp 文件一并被忽略。
4. `.gitignore` 本身也是一个普通的、应当纳入版本历史的文件，这样团队成员就能继承相同的规则。将它与要保留的文件一起提交：`git add .`，然后运行 `git commit -m "add the ignore rules"`。注意 `add .` 暂存了哪些内容：notes.txt 和 .gitignore，没有任何被忽略的文件。

需要记住的一个界限：忽略规则仅对未跟踪（untracked）的文件生效。
只要文件已经被提交过，无论 .gitignore 中写了什么，它都依然会保持被跟踪状态。
