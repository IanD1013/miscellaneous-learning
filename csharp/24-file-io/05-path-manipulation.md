### 路径操作

`Path` 类提供了在不同操作系统之间安全处理文件和目录路径的方法。

### Path.Combine - 安全构建路径

切勿使用字符串拼接（`+`）来连接路径。
请改用 `Path.Combine`：

```csharp
// 错误 - 在不同操作系统或边界情况下会出问题
string bad = directory + "\\" + fileName;

// 正确 - 自动处理分隔符
string good = Path.Combine(directory, fileName);
string multi = Path.Combine("C:\\", "Users", "Documents", "file.txt");
```

`Path.Combine` 会自动处理尾部/前导斜杠，因此这些都会产生相同的结果：

```csharp
Path.Combine("C:\\folder", "file.txt")     // C:\folder\file.txt
Path.Combine("C:\\folder\\", "file.txt")    // C:\folder\file.txt
Path.Combine("C:\\folder", "\\file.txt")    // C:\folder\file.txt
```

### 提取路径组件

```csharp
string fullPath = "C:\\Documents\\report.pdf";

Path.GetFileName(fullPath)      // "report.pdf"
Path.GetExtension(fullPath)     // ".pdf"
Path.GetFileNameWithoutExtension(fullPath)  // "report"
Path.GetDirectoryName(fullPath) // "C:\\Documents"
```

### 实用的 Path 方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `Path.Combine(a, b)` | 安全地连接路径 | `Path.Combine("dir", "file.txt")` → `"dir\\file.txt"` |
| `Path.GetFileName(p)` | 获取带有扩展名的文件名 | `Path.GetFileName("dir\\file.txt")` → `"file.txt"` |
| `Path.GetExtension(p)` | 获取带有句点的扩展名 | `Path.GetExtension("file.txt")` → `".txt"` |
| `Path.GetDirectoryName(p)` | 获取目录部分 | `Path.GetDirectoryName("dir\\file.txt")` → `"dir"` |

### 你的任务

实现三个方法：

1. `BuildFilePath` - 使用 `Path.Combine` 安全地合并目录和文件名
2. `GetFileNameFromPath` - 从完整路径中仅提取文件名
3. `GetFileExtension` - 提取文件扩展名（包括句点）

### 方法签名

```csharp
public static string BuildFilePath(string directory, string fileName)
public static string GetFileNameFromPath(string filePath)
public static string GetFileExtension(string filePath)
```

### 预期结果

```swift
BuildFilePath("C:\\Users", "data.txt") -> "C:\\Users\\data.txt"
GetFileNameFromPath("C:\\Documents\\report.pdf") -> "report.pdf"
GetFileExtension("image.png") -> ".png"
```

### 解答

```csharp
using System;
using System.IO;

public class Solution
{
    public static string BuildFilePath(string directory, string fileName)
    {
        // 使用 Path.Combine 合并目录和文件名
        return Path.Combine(directory, fileName);
    }
    
    public static string GetFileNameFromPath(string filePath)
    {
        // 从完整路径中仅提取文件名
        return Path.GetFileName(filePath);
    }
    
    public static string GetFileExtension(string filePath)
    {
        // 提取文件扩展名（包括句点），没有扩展名时返回空字符串
        return Path.GetExtension(filePath);
    }
}
```
