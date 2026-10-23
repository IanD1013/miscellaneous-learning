### 相对命名：~ 和 ^

你很少会想要整天复制 id。
Git 允许你根据提交与你当前所在位置的关系来指代它们。

1. `git show HEAD~1`：HEAD 的父提交。
2. `git show HEAD^`：脱字符是同一个父提交的另一种写法。（`^2` 表示“第二个父提交”，且仅存在于合并提交中；这些将在后面的章节中介绍。）
3. `git show HEAD~2`：往上两级。只要历史记录足够长，就可以一直链式追溯下去。
4. `git rev-parse HEAD~2`：查看某个名称具体解析为哪个 id。
5. `git rev-parse --abbrev-ref HEAD`：反向操作，查看 HEAD 当前代表哪个分支名称。
6. 证明你可以进行导航：HEAD 上方两级的提交有一条提交信息。将其写入文件：`echo style the header > answer.txt`。
