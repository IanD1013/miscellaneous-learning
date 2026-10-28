### 逐字字符串

逐字字符串（verbatim string）字面量以开头的双引号前的 `@` 开始。
它告诉 C# 按照书写的原样处理字符串，忽略诸如 `\n` 或 `\t` 之类的转义序列。
这对于 **Windows 文件路径** 特别有用，否则其中的每个反斜杠都需要写成双反斜杠。

### 为什么使用逐字字符串？

如果不使用逐字字符串，像 `C:\Users\Admin` 这样的路径必须写成 `"C:\\Users\\Admin"`，因为单个 `\` 会开始一个转义序列。
逐字字符串允许你按照实际显示的样子编写路径，从而保持代码整洁易读。

### 普通字符串 vs 逐字字符串

```csharp
// 普通字符串 - 反斜杠必须写成两个（转义）
string regular = "D:\\Projects\\Notes\\todo.md";

// 逐字字符串 - 反斜杠按原样生效
string verbatim = @"D:\Projects\Notes\todo.md";

// 两者都产生：D:\Projects\Notes\todo.md
```

### 更多示例

```csharp
// 注册表风格的键
string key = @"HKEY_LOCAL_MACHINE\Software\MyApp";
Console.WriteLine(key); // HKEY_LOCAL_MACHINE\Software\MyApp

// 网络共享路径
string share = @"\\Server01\Shared\Reports";
Console.WriteLine(share); // \\Server01\Shared\Reports
```

### 逐字字符串中的引号

要在逐字字符串内部包含引号，请将其写成两个双引号：

```csharp
string withQuote = @"She said ""Hello"" to me.";
// 输出：She said "Hello" to me.
```

### 何时不使用逐字字符串

- **当你需要转义序列时**：`\n`、`\t`、`\r` 在逐字字符串内会被视为字面文本。
- **简短简单的字符串**：`@"Hello"` 相比于 `"Hello"` 没有任何优势。

### 你的任务

编写一个方法，使用逐字字符串（`@"..."`）打印**两条 Windows 文件路径**，每条路径占一行：

1. `C:\Users\Admin\Documents\report.txt`
2. `D:\Mail\Inbox\2026\archive.pst`

对每个路径使用 `Console.WriteLine`，使它们显示在独立的行上。
因为每个路径都是单行文本，所以你不会遇到任何编辑器自动缩进的问题。

### 方法签名

```csharp
public static void PrintFilePaths()
```

### 预期输出

```
C:\Users\Admin\Documents\report.txt
D:\Mail\Inbox\2026\archive.pst
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintFilePaths()
    {
        // 使用逐字字符串打印 Windows 文件路径
        Console.WriteLine(@"C:\Users\Admin\Documents\report.txt");

        // 再使用逐字字符串打印邮件文件夹路径
        Console.WriteLine(@"D:\Mail\Inbox\2026\archive.pst");
    }
}
```
