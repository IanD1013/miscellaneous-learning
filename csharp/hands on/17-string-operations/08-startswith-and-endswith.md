### StartsWith 和 EndsWith

这些字符串方法用于检查字符串是否以特定的字符序列开头或结尾。
它们返回一个布尔值，常用于验证输入、筛选文件以及检查 URL 协议。

### 基本用法

```csharp
string filename = "document.txt";
string url = "https://example.com";

// 检查字符串的结尾
bool isTxt = filename.EndsWith(".txt");    // True
bool isPdf = filename.EndsWith(".pdf");    // False

// 检查字符串的开头
bool isSecure = url.StartsWith("https://"); // True
bool isHttp = url.StartsWith("http");    // True (https 包含 http)
```

### 大小写敏感性

默认情况下，这两种方法都是区分大小写的。
你可以使用 StringComparison 使它们不区分大小写：

```csharp
string file = "README.TXT";

// 区分大小写（默认）
bool result1 = file.EndsWith(".txt");                                    // False

// 不区分大小写
bool result2 = file.EndsWith(".txt", StringComparison.OrdinalIgnoreCase); // True
```

### 常见用例

| 方法 | 用例 | 示例 |
| --- | --- | --- |
| EndsWith | 文件扩展名检查 | `file.EndsWith(".csv")` |
| EndsWith | 句子标点符号 | `text.EndsWith("?")` |
| StartsWith | 协议验证 | `url.StartsWith("https://")` |
| StartsWith | 前缀筛选 | `name.StartsWith("Dr.")` |

### 你的任务

实现以下两个方法：

1. `IsTextFile` - 检查文件名是否以 ".txt" 结尾
2. `IsHttpsUrl` - 检查 URL 是否以 "https://" 开头

### 方法签名

```csharp
public static bool IsTextFile(string filename)
public static bool IsHttpsUrl(string url)
```

### 预期结果

```
IsTextFile("notes.txt") -> True
IsTextFile("image.png") -> False
IsHttpsUrl("https://example.com") -> True
IsHttpsUrl("http://example.com") -> False
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool IsTextFile(string filename)
    {
        // 检查文件名是否以 ".txt" 结尾
        return filename.EndsWith(".txt");
    }
    
    public static bool IsHttpsUrl(string url)
    {
        // 检查 URL 是否以 "https://" 开头
        return url.StartsWith("https://");
    }
}
```
