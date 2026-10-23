### 什么是 remote

remote 是仓库另一个副本的命名地址，通常位于服务器上。
在开始前需要说明的是：此环境中没有网络。
您在此处配置的 remote 是一个本地替代品，但正如接下来的课程所展示的那样，关于它的所有可观察行为都与实际情况完全一致。

1. `git remote`：目前还没有 remote。没有任何输出。
2. `git remote add origin https://example.com/store.git`：注册一个 remote。名称 origin 是代表“该代码存放的主位置”的惯用命名。
3. `git remote -v`：查看列表及对应地址。
4. Remote 本质上只是配置：`git remote remove origin` 会注销它。
5. 为了保险起见，把它重新添加回来：`git remote add origin https://example.com/store.git`。
