### 练习：历史侦探

有人将主题从 light 改为了 midnight。
仅使用只读工具，查出具体是哪一次 commit 进行了该更改。

1. `git log --oneline`：列出嫌疑提交。
2. 进行排查：`git show` 加上 log 中的短 id 可以打印出某一次 commit 更改的内容；`git diff` 加上两个 id（较旧的在前）可以比较两个节点。相对名称同样有效：`git show HEAD~2`。其 diff 将 `theme=light` 变为 `theme=midnight` 的 commit 就是你要找的“元凶”。
3. 得出结论：使用 echo 和 `>` 操作符将该有罪 commit 的 message 写入 `answer.txt`。
