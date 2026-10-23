### 开放沙盒

这个终端是一个真实的 git 仓库，里面预置了你学过处理的所有内容：两个分支、一个 tag、一个未提交修改的文件（dirty file）、一个未跟踪的残留文件、一个旧的 stash，以及一个固定的 remote。
它是完全属于你的。
这里只有一个检查点，就在最后。

一些尝试的思路，按进阶程度排列：

- 到处看看：`git status`、`git log --graph --all --oneline`、`git branch -a`、`git remote -v`、`git stash list`、`git reflog`、`cat app.js`。
- 触发安全防护机制：在有未提交修改的情况下合并、在文件被修改时执行 `git rm app.js`、执行空的 `git commit -m`，以及执行 `git stash drop stash@{9}`，这些操作都会被礼貌地拒绝且不改变任何内容。取消设置你的身份信息（`git config --unset user.email`），下一次 commit 就会被拒绝，直到你重新设置为止。
- 开展实际工作：stash 暂存或 commit 提交未保存的修改、合并 `experiment` 并解决冲突（或 `--abort`）、cherry-pick、rebase、pop 弹出旧的 stash、`git push`、hard-reset 以及使用 reflog 来拯救自己。
- 编辑器面板操作的也是这同一个仓库。点击界面操作同样有效。

当你觉得练习得差不多了，插上旗帜通关：`git tag done`。
