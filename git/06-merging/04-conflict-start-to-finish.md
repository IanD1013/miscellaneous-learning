### 冲突，从头到尾

两个分支都重写了 `poem.txt` 的同一行。
Git 无法替你做决定，所以它停下来向你询问。
从容地完整走一遍整个生命周期。

1. `git merge feature`：CONFLICT（冲突）。没有任何东西损坏；git 只是在等待。
2. `cat poem.txt`：`<<<<<<<` / `=======` / `>>>>>>>` 标记是真实文件中的真实字节。分割线上方是你的内容，下方是他们的内容。
3. 通过自行写入最终版本来解决：`echo roses are red > poem.txt`，然后 `echo violets are violet, obviously >> poem.txt`。（编辑器也在标记处提供了采纳某一方的按钮；当其中完整的一方就是答案时，它们非常有用。在这里，需要将两行结合起来。）
4. 标记为已解决：`git add poem.txt`。暂存该文件就是你告诉 git 冲突已解决的方式。
5. 完成：`git commit -m "merge feature"`。一个真正的双父节点合并提交（two-parent merge commit）。
6. `git status`：再次恢复干净。在冲突过程中它会显示 "You have unmerged paths"；在执行 add 之后，会显示 "All conflicts fixed but you are still merging"。在你下一次遇到真正的冲突时运行它，观察它是如何叙述状态的。
