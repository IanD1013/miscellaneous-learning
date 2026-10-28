### 写入文本文件

`File.WriteAllText` 方法是在 C# 中将文本写入文件的最简单方式。
它在一个操作中创建新文件、写入指定的字符串并关闭文件。
程序通常需要向用户反馈执行情况，因此本练习将文件写入与控制台输出结合在一起。

### 工作原理

当你调用 `File.WriteAllText` 时，运行时会自动打开（或创建）文件、写入整个字符串并关闭句柄。
它本身不会报告进度，因此通常在写入之后调用 `Console.WriteLine` 来确认已写入的内容。
在本练习中，**被检查的是控制台输出**，你的方法必须打印两行内容。

### 基本用法

```csharp
// 将一个简单字符串写入文件
File.WriteAllText("output.txt", "Hello, World!");

// 写入多行（在字符串中使用 \n）
File.WriteAllText("notes.txt", "Line 1\nLine 2\nLine 3");

// 覆盖已有内容
File.WriteAllText("data.txt", "New content replaces old");
```

### 打印确认消息

`Console.WriteLine` 会打印一行文本并在末尾换行。
结合字符串插值（`$"..."` 语法），你可以直接嵌入变量值：

```csharp
string name = "report.csv";
Console.WriteLine($"Saved file: {name}");   // Saved file: report.csv
Console.WriteLine($"Bytes written: {42}");  // Bytes written: 42
```

### File.WriteAllText 的关键特性

- 如果文件不存在，**创建该文件**
- 如果文件已存在，**覆盖该文件**（没有任何警告！）
- 写入后自动**关闭文件**

### File 类方法

| 方法 | 描述 |
| --- | --- |
| `File.WriteAllText(path, text)` | 将字符串写入文件 |
| `File.WriteAllLines(path, lines)` | 写入字符串数组，每行一个 |
| `File.AppendAllText(path, text)` | 将文本追加到文件末尾 |

### 你的任务

编写一个方法，按顺序执行以下三项操作：

1. 使用 `File.WriteAllText` 将提供的内容写入给定的文件路径。
2. 打印一行确认信息，格式必须完全一致：`Successfully wrote to {filePath}`
3. 在下一行打印内容，格式必须完全一致：`Content: {content}`

**注意：** 本练习通过控制台输出来进行验证。
两个 `Console.WriteLine` 行都是必需的，并且必须完全匹配（包括空格）才能通过验证。

### 方法签名

```csharp
public static void WriteToFile(string filePath, string content)
```

### 预期输出

```vbnet
WriteToFile("test.txt", "Hello") prints:
Successfully wrote to test.txt
Content: Hello
```

### 解答

```csharp
using System;
using System.IO;

public class Solution
{
    public static void WriteToFile(string filePath, string content)
    {
        // 第 1 步：将内容写入指定路径的文件
        File.WriteAllText(filePath, content);

        // 第 2 步：打印确认信息
        Console.WriteLine($"Successfully wrote to {filePath}");

        // 第 3 步：在下一行打印内容
        Console.WriteLine($"Content: {content}");
    }
}
```
