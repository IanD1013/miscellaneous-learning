粘贴到 SQL 查询中的输入会成为查询的一部分。
以文本形式构建的操作系统命令也有同样的弱点。
当该文本通过 shell 运行时，输入中的字符可以启动应用程序从未打算运行的命令。
这就是**命令注入**（command injection），是 OWASP 列在 A05:2025 Injection 之下的攻击之一。

网络工具端点通过使用请求中的主机名运行 `ping` 来检查主机是否可达。
Node.js 版本把命令构建为一个字符串，并用 `exec` 运行它：

```js
const { exec } = require('node:child_process');
exec('ping -c 1 ' + host);
```

`exec` 把整个字符串传递给 **shell**（`/bin/sh`），即解释你在终端中输入内容的程序。
shell 不会把该字符串当作一个命令及其参数来读取。
它首先处理的是 **shell 元字符**（shell metacharacters），即除自身文本外还带有其他含义的字符：

- `;` 结束一个命令并开始下一个。
- `&&` 仅当第一个命令成功时才运行下一个。
- `|` 把一个命令的输出送入另一个命令。
- `$( )` 运行括号内的命令，并把其输出放在原位。这是命令替换（command substitution），而在命令两边加反引号（`` `id` ``）是一种较老的写法。

所以当 `host` 是 `example.com; cat /etc/passwd` 时，shell 会读到由 `;` 分隔的两个命令，并同时运行它们。
第二个命令以与应用程序进程相同的权限运行。
点和斜杠不是元字符，所以像 `sub.example.com` 这样的普通主机名不会添加命令，`example.com/status`（一个主机名后跟一个路径）也不会。

这种攻击并不取决于 `ping` 做什么。
`ping` 只发送网络探测，但输入追加的命令可以是任何东西，无论 `ping` 是什么，shell 都会以应用程序的权限运行它。
在浏览器中验证主机也无法阻止它，因为攻击者会把请求直接发送给服务器，而从不加载页面。

在命令字符串内给值加引号并不是修复方法。
使用 `exec('ping -c 1 "' + host + '"')` 时，shell 仍然会读取引号之间的文本，所以值中的 `$( )` 仍会作为命令运行，而输入中的 `"` 字符会提前关闭引号，让其余部分作为命令运行。
单引号也好不到哪里去：`$( )` 在单引号内不会运行，但输入中的 `'` 会以同样的方式关闭它们。
转义 shell 特殊对待的每一个字符是可能的，但很容易出错，而漏掉一个字符就会重新打开漏洞。

### 以列表形式传递参数

直接启动程序，并把它的参数放在列表中，这样就不会运行 shell，也就没有什么需要转义的。
在 Node.js 中，`execFile` 做的就是这件事：

```js
const { execFile } = require('node:child_process');
execFile('ping', ['-c', '1', host]);
```

数组中的每一项都恰好作为一个参数到达 `ping`。
没有任何东西会拆分或重新解释它，所以 `host` 中的 `;`、`|`、`&&` 和 `$( )` 都只是主机名中的字符。
整个恶意值作为单个主机名到达，`ping` 无法解析它，所以它会失败，而不是启动第二个命令。
**参数列表**（argument list）不会验证值，也不会从中移除字符；它只是防止 shell 读取它。

C# 也有同样的选择。
用 `-c` 和构建好的命令行启动 `/bin/sh`，会遇到与 `exec` 同样的问题，无论是在 C# 中还是通过 `execFile`：启动的程序是 shell，而它会读取整行。
修复方法是使用 `ProcessStartInfo`，其 `FileName` 是程序本身，其参数逐个放入 `ArgumentList`，不使用 `/bin/sh`：

```csharp
var psi = new ProcessStartInfo { FileName = "ping" };
psi.ArgumentList.Add("-c");
psi.ArgumentList.Add("1");
psi.ArgumentList.Add(host);
using var process = Process.Start(psi);
```

运行时在没有 shell 的情况下把列表传递给程序。
对于同一次调用，`ArgumentList` 和较老的单字符串 `Arguments` 不能同时设置。

最强的修复方法是根本不调用外部命令。
图像端点会对上传的文件名运行一个缩放程序，它可以改为在应用程序内部使用图像库来缩放图片，这样就没有命令行，也没有 shell 可供文件名突破。
