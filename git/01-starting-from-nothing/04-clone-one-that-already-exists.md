### 克隆一个已存在的仓库

当项目在你的计算机上从零开始时，你会使用 `git init`。
但通常情况下，项目已经存在于其他地方。
在这种情况下，你不需要初始化一个空仓库，而是克隆现有的仓库。

本课程使用的是预先准备好的课程远程仓库，而不是公共互联网。
其操作方式与你使用 GitHub、GitLab、Azure Repos 或任何其他托管 Git 服务器时的形式完全相同。

1. 首先在这里运行 `git status`。你现在还没有进入仓库中。
2. 使用 `git clone lesson://github/starter-site.git` 克隆准备好的项目。
3. 运行 `ls`。克隆操作生成了一个新的 `starter-site` 文件夹。
4. 使用 `cd starter-site` 进入该文件夹。
5. 使用 `git status`、`git remote -v` 和 `git log --oneline` 查看克隆为你提供了什么：一个分支、一个 `origin` 远程仓库以及已有的历史记录。
