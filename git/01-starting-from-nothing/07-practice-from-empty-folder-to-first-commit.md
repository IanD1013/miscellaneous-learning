### 练习：从空文件夹到第一次提交

这次没有任何预设内容。
请亲自走完整个流程，从空文件夹到记录版本历史。

1. `git init`
2. 身份配置：`git config user.name "Ada Lovelace"` 以及 `git config user.email ada@example.com`。
3. 创建一个值得保存的文件：`echo tomato soup > recipe.txt`。
4. `git add recipe.txt`
5. `git commit -m "add the first recipe"`
6. `git log --oneline`：一行显示一条提交记录及你的提交信息。
