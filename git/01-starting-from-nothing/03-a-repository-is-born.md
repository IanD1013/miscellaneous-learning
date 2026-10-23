### 仓库的诞生

当您运行 `git init` 的那一刻，一个文件夹就变成了一个 git 仓库。
您的文件不会发生改变；git 只是启动了一个隐藏的数据库，随时准备在您要求时记录历史。

1. `git init`：阅读返回的信息。该文件夹现在已经是一个仓库了。
2. `git status`：git 的真实摘要。它会显示 "No commits yet"，并将 `idea.txt` 列为未跟踪（untracked）：git 可以看到该文件，但尚未记录它。
3. 再创建一个文件：`echo remember to write tests > todo.txt`。
4. 再次运行 `git status`：有两个未跟踪的文件。未跟踪（Untracked）意味着“git 能看到它，但尚未管理它”。接下来就是进行记录。
