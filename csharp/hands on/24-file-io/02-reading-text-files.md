### 读取文本文件

`File.ReadAllText` 是在 C# 中将整个文本文件读取为字符串的最简单方法。
它会打开文件、读取全部内容、关闭文件，并返回文本。

### 基本用法

```csharp
// 将整个文件读取为一个字符串
string content = File.ReadAllText("myfile.txt");

// 使用指定的编码读取
string content = File.ReadAllText("myfile.txt", Encoding.UTF8);
```

### 读取与写入

| 方法 | 用途 | 返回值 |
| --- | --- | --- |
| `File.ReadAllText(path)` | 读取整个文件 | `string` |
| `File.WriteAllText(path, text)` | 将文本写入文件 | `void` |
| `File.ReadAllLines(path)` | 按行读取文件 | `string[]` |

### File 类方法

```csharp
// 读取前先检查文件是否存在
if (File.Exists(filePath))
{
    string text = File.ReadAllText(filePath);
}

// ReadAllText 会自动处理文件的打开和关闭
```

### 你的任务

编写一个方法，读取文本文件的内容并将其打印到控制台。
文件路径作为参数提供。

**重要提示：** 请使用 `Console.Write`（而不是 `Console.WriteLine`）完全按照文件中的原始内容进行打印。

### 方法签名

```csharp
public static void ReadAndPrintFile(string filePath)
```

### 预期结果

```scss
ReadAndPrintFile("greeting.txt")  // 文件内容: "Hello, World!"
// 打印: Hello, World!

ReadAndPrintFile("numbers.txt")   // 文件内容: "1\n2\n3"
// 打印:
// 1
// 2
// 3
```

### 解答

```csharp
using System;
using System.IO;

public class Solution
{
    public static void ReadAndPrintFile(string filePath)
    {
        // 读取整个文件，并按原样打印（不额外添加换行）
        string content = File.ReadAllText(filePath);
        Console.Write(content);
    }
}
```
