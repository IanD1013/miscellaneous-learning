### 带有冲突的 rebase

将 commit 重新应用（replay）到已变动的基准上时，可能会像 merge 一样发生冲突。
暂停的 rebase 提供了三条出路：`--continue`、`--skip`、`--abort`。
这一次，我们选择第一条。

1. `git rebase main`：rebase 暂停了。双方都修改了页面标题。阅读 git 输出的提示信息；它列出了全部三条出路。
2. 结合双方意图来解决冲突：`echo '<title>Final, by Shop</title>' > page.html`，然后执行 `git add page.html`。
3. `git rebase --continue`：重新应用继续进行并顺利完成。你的 commit 已经建立在新的基准之上，提交信息保持完好，且包含了你的冲突解决方案。
4. `git log --oneline`：历史记录再次变成了一条直线。
