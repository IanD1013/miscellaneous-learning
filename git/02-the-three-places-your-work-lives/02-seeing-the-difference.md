### 查看差异

`git status` 会列出发生更改的文件；`git diff` 则显示具体的行。
之所以存在两种 diff，是因为有两处差异空间：index 与 HEAD 之间（staged）以及 working tree 与 index 之间（unstaged）。

1. `git diff --staged`：已经暂存的更改，即 basil 那一行。`--cached` 是同一个标志的另一个名称。
2. `git diff`：当前为空。working tree 中的所有内容都与 index 匹配。
3. 进行一次新的编辑：`echo maybe some chili >> recipe.txt`。
4. `git diff`：显示 chili 那一行。这就是未暂存的差异。
5. 使用 `git diff recipe.txt` 将范围限定于单个文件，在修改了许多文件时非常有用。
6. `git add recipe.txt`：将其暂存。
7. `git diff --staged`：两次编辑现在都位于暂存差异中，而单纯的 `git diff` 再次变为空。
