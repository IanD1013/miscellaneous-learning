### 发布：push 与 -u

你的 main 比远程已知的内容领先一个 commit。
发布它。
记住诚实规则：这里不会真正发送网络数据包，但可观察到的行为、移动的 `origin/main` 引用以及状态计数，与真实的 git 完全一致。

1. `git status`：“ahead of 'origin/main' by 1 commit”。该计数比较了你的分支与远程跟踪引用。
2. `git push`：查看 old..new 这一行。`origin/main` 移动到了你的最新 commit（tip），此时 `git status` 显示 up to date（最新）。
3. 全新的分支还没有对应的远程分支，因此首次推送需要自我介绍：`git switch -c release`，然后 `git push -u origin release`。`-u`（长参数形式 `--set-upstream`）将二者关联起来，以便后续普通的 push 和 pull 知道目标分支在哪里。
4. `git branch -a`：本地分支加上你现在拥有的远程跟踪引用。
