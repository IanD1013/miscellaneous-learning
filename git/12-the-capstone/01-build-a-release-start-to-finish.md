### 构建发布版本，从头到尾

一个完整的故事，用到所有工具箱。
披萨店的网站已经初始化并发布；规范地发布宣传标语的 1.0 版本。

1. 在分支上工作：`git switch -c launch`。
2. 编写上线宣传标语并提交：`echo fresh pasta, made daily > tagline.txt`，然后执行 `git commit -am "launch: the pasta tagline"`。
3. 与此同时店主有了新想法。切回 main 分支：`git switch main`。
4. 他们的版本：`echo pizza worth the wait > tagline.txt`，然后执行 `git commit -am "main: the pizza tagline"`。
5. 将分支合并回来：`git merge launch`。当然会出现冲突（CONFLICT）；双方都重写了标语。
6. 巧妙地化解冲突：`echo pizza and pasta, worth the wait > tagline.txt`，然后执行 `git add tagline.txt`。
7. 完成合并：`git commit -m "merge the launch tagline"`。
8. 标记发布版本：`git tag -a v1.0 -m "launch day"`。
9. 发布分支：`git push`。本课的模拟远程仓库会将附注标签 `v1.0` 保留在本地。在完整的 Git 环境中，可使用 `git push origin v1.0` 单独发布该标签。
10. 欣赏成果：`git log --graph --oneline`。分支、冲突、合并、本地发布标签、分支推送。泳道图中完整展现了整个过程。
