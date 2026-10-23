### 使用 git mv 重命名

手动重命名意味着删除一个路径并创建另一个路径，然后将这两项变动都告知 git。
`git mv` 则一步完成重命名并将整个变更暂存。

1. `git mv draft.txt chapter1.txt`：文件在磁盘上完成重命名，并且该变更已经暂存。
2. `git status -s`：查看状态。原生 Git 通常会将完全一致的移动操作精简显示为 `R draft.txt -> chapter1.txt`。本课程终端则将这一相同的底层变更展示为暂存的添加和删除（`A chapter1.txt` 加上 `D draft.txt`）。
3. 记录变更：`git commit -m "rename the draft"`。

如果目标名称已存在，`git mv` 会拒绝执行；`git mv -f` 则会强制覆盖。
