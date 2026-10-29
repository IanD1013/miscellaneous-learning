发票下载端点从查询字符串中读取 `fileName`，例如 `GET /invoices?fileName=2026-05.pdf`，并把它与 `/var/app/invoices`（存放发票 PDF 的文件夹）拼接起来。
请求在 `fileName` 中放什么，就决定了拼接后的路径最终指向哪里，包括该文件夹之外的位置：

```csharp
var path = Path.Combine("/var/app/invoices", fileName);
var bytes = File.ReadAllBytes(path);
```

`2026-05.pdf` 得到 `/var/app/invoices/2026-05.pdf`，带子文件夹的名称（例如 `2025/12.pdf`）也仍然在其内部。
代码打算从中读取的文件夹是**基准文件夹**（base folder）。
如果改为发送 `../../../etc/passwd`，端点就会返回 `/etc/passwd`，即列出这台机器用户账户的 Linux 文件。
这就是**路径遍历**（path traversal）：来自请求的文件名（与任何其他查询字符串值一样是不可信输入）把拼接后的路径带出了基准文件夹。
于是服务器会读取它从未打算提供的文件，而在这样的路径下保存文件的端点也会把文件写到该文件夹之外。
OWASP 将路径遍历列在 A01:2025 Broken Access Control 之下。
该端点的 Node.js 版本在使用 `path.join` 时有同样的缺陷。

### 路径如何爬出去

在路径中，`..` 表示上一级文件夹，所以每个 `../` 段会向上移动一个目录。
`Path.Combine` 把两个字符串拼接起来，但不会计算 `..` 段，并返回 `/var/app/invoices/../../../etc/passwd`。
只有当 `File.ReadAllBytes` 打开文件时，才会计算 `..` 段：向上到 `/var/app`，然后是 `/var`，然后是 `/`，即根目录。
从那里，`etc/passwd` 向下通向 `/etc/passwd`。

![文件夹树，根目录在顶部，其下是 etc 和 var，passwd 在 etc 下，app 在 var 下，invoices 在 app 下，2026-05.pdf 在 invoices 下。请求 `../../../etc/passwd` 从 invoices 经过 app 和 var 向上爬到根目录，然后经过 etc 向下到达 passwd。](images/path-climbing-out.png)

每个 `../` 都从 `/var/app/invoices` 向上移动一个文件夹，所以第三个到达根目录，然后 `etc/passwd` 向下通向基准文件夹之外的一个文件。

向上爬也可以在别处再向下回来。
在基准文件夹旁边，服务器把较旧的发票保存在 `/var/app/invoices-archive` 中，而 `../invoices-archive/2025-11.pdf` 会向上一级到达 `/var/app`，再向下进入那个同级文件夹。

绝对路径根本不需要 `..`。
当 `Path.Combine` 的第二个参数是有根的（rooted），即像 `/etc/passwd` 那样从根目录开始时，`Path.Combine` 会丢弃基准文件夹，并原样返回第二个参数。
它不会抛出异常：`Path.Combine("/var/app/invoices", "/etc/passwd")` 返回 `/etc/passwd`。

### 让路径保持在基准文件夹内

第一种修复尝试是在拼接之前从名称中删除 `../`。
只删除一次该序列，会留下删除操作所推到一起的内容。
在 `....//etc/passwd` 中，唯一的 `../` 从第三个字符开始。
删掉这三个字符后，前面的两个点就与后面的斜杠相遇了：`../etc/passwd`，它仍然会向上爬出基准文件夹一级。
真正有效的检查看的是路径最终落在哪里，所以名称的拼写对它们来说无关紧要。

检查拼接后的字符串是否以基准文件夹开头也会失败。
`/var/app/invoices/../../../etc/passwd` 与 `/var/app/invoices` 逐字符相同地开头，所以 `StartsWith("/var/app/invoices")` 会通过，而 `..` 段要到之后打开文件时才会爬出去。

`Path.GetFullPath` 会计算出一个路径通向哪里。
它返回**完整路径**（full path）：一个每个 `.` 和 `..` 段都已解析的绝对路径，所以 `/var/app/invoices/../../../etc/passwd` 变成 `/etc/passwd`。
它只计算路径。
它不知道基准文件夹，也不拒绝任何东西，所以比较仍然取决于你的代码。
在 Node.js 中，`path.resolve('/var/app/invoices', fileName)` 在一次调用中完成拼接和解析，而绝对的 `fileName` 在那里同样会替换基准文件夹。

比较还需要再加一个字符。
`/var/app/invoices-archive/2025-11.pdf` 也以字符 `/var/app/invoices` 开头，所以针对该字符串的检查会放过那个同级文件夹。
应当与基准文件夹加上**末尾分隔符**（trailing separator）`/var/app/invoices/` 进行比较。
归档路径在那个 `/` 所在的位置是 `-`，所以它不通过，而基准文件夹内的每个文件仍然能通过：

```csharp
var baseFolder = "/var/app/invoices/";
var full = Path.GetFullPath(Path.Combine(baseFolder, fileName));
if (!full.StartsWith(baseFolder, StringComparison.Ordinal))
    return NotFound();
return PhysicalFile(full, "application/pdf");
```

`StringComparison.Ordinal` 精确地比较字符，不应用语言规则。
先解析再与末尾分隔符比较，两者结合使检查可靠：`../../../etc/passwd` 解析为 `/etc/passwd`，`/etc/passwd` 保持不变，两者都会被拒绝。
Node.js 的检查形式相同，先 `path.resolve(baseFolder, fileName)`，然后 `startsWith(baseFolder)`，其中 `baseFolder` 带有末尾的 `/`。

### 不使用请求中的文件名

另一种可靠的方法是从不把请求中的文件名放进路径。
当应用程序写入发票 PDF 时，它自己为文件命名，使用**生成的名称**（generated name），例如 `7f3a9c2e41b8.pdf`，并把该名称存储在发票的数据库行中。
请求只携带发票的 ID，如 `GET /invoices/8812`，端点从 ID 为 8812 的行中读取存储的名称，并把它与基准文件夹拼接。
到达 `Path.Combine` 的每个名称都是由应用程序写入的，所以请求没有办法添加 `../` 或绝对路径。
