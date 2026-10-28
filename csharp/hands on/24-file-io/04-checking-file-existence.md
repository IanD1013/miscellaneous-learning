### 检查文件是否存在

`File.Exists` 会在你尝试读取或写入文件之前，检查指定路径下是否存在该文件。
这可以防止在处理可能存在或不存在的文件时发生运行时异常。

### 为什么要先检查？

尝试读取一个不存在的文件会抛出 `FileNotFoundException` 异常。
先检查文件是否存在可以让你妥善处理文件缺失的情况。

```csharp
// 不检查 - 文件缺失时会抛出异常
string content = File.ReadAllText("missing.txt"); // BOOM!

// 先检查 - 安全的做法
if (File.Exists("data.txt"))
{
    string content = File.ReadAllText("data.txt");
}
else
{
    Console.WriteLine("File not found!");
}
```

### File.Exists 返回布尔值

```csharp
bool exists = File.Exists("config.txt");  // true 或 false

// 在条件中使用
if (File.Exists(path))
{
    // 可以安全读取
}
```

### 常见模式

```csharp
// 模式 1：文件缺失时使用默认值
string GetConfig(string path)
{
    if (File.Exists(path))
        return File.ReadAllText(path);
    return "default settings";
}

// 模式 2：文件缺失时创建它
if (!File.Exists("log.txt"))
{
    File.WriteAllText("log.txt", "Log started");
}
```

### 你的任务

编写一个安全读取文件的方法。
如果文件存在，返回其内容。
如果文件不存在，返回字符串 `"File not found"` 而不是抛出异常。

### 方法签名

```csharp
public static string SafeReadFile(string filePath)
```

### 预期结果

```rust
SafeReadFile("existing.txt") -> 文件的内容
SafeReadFile("missing.txt") -> "File not found"
```

### 解答

```csharp
using System;
using System.IO;

public class Solution
{
    public static string SafeReadFile(string filePath)
    {
        // 文件存在时返回其内容
        if (File.Exists(filePath))
        {
            return File.ReadAllText(filePath);
        }

        // 文件不存在时返回提示信息，而不是抛出异常
        return "File not found";
    }
}
```
