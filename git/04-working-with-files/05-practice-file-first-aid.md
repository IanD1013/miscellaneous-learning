### 练习：文件急救

三个文件问题，一个仓库。
全部修复它们，然后一次性全部提交。

1. `widnow.js` 是 `window.js` 的拼写错误。正确重命名它：`git mv widnow.js window.js`。
2. `debug.log` 本就不该被提交。彻底删除它：`git rm debug.log`。
3. 两个提交之前的样式表更好。提取该版本：`git restore --source=HEAD~2 style.css`。
4. 一行代码提交所有内容：`git commit -am "file first aid"`。`-a` 会将未暂存的样式表更改与已暂存的重命名及删除操作一同提交。
5. `git status`：状态完全健康，工作区干净。
