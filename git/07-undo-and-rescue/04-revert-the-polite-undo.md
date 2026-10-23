### revert：礼貌的撤销

Reset 会重写历史，这对已经看到过该历史的人来说很不友好。
`git revert` 通过添加一个包含相反变更的新 commit 来撤销某个 commit。
历史记录得以保持真实完整。

1. `git revert HEAD`：出现了一个新的 commit，标题为 Revert "add telemetry pings"。这里没有编辑器，因此引擎会自动写入该标准提交信息。
2. `git log --oneline`：共有三次 commit。ping commit 依然存在，紧随其后的是对其正式的撤销记录。没有任何内容被抹去。
3. `cat app.js`：代码中的 ping 那一行已被移除。

经验法则：对于私有错误使用 reset，对于他人可能已经看到的任何内容使用 revert。
