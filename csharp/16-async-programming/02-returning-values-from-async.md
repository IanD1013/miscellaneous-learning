### 使用 Task<T> 进行异步文件 I/O

异步读取文件时，请使用返回 `Task<string>` 的 `File.ReadAllTextAsync()`。
这使得应用程序在等待磁盘操作时能够保持响应。

### 为什么使用异步文件 I/O？

```csharp
// 同步 - 在文件读取完成前阻塞线程
string content = File.ReadAllText("data.txt");

// 异步 - 在等待 I/O 期间释放线程
string content = await File.ReadAllTextAsync("data.txt");
```

文件操作涉及磁盘 I/O，与 CPU 操作相比速度较慢。
使用异步方法可以防止应用程序在等待任务完成时出现冻结/未响应。

### 异步文件读取方法

`System.IO.File` 类提供了几种用于读取文件的异步方法：

```csharp
// 将整个文件读取为单个字符串
string text = await File.ReadAllTextAsync("document.txt");

// 将文件读取为行数组
string[] lines = await File.ReadAllLinesAsync("log.txt");

// 将文件读取为原始字节
byte[] bytes = await File.ReadAllBytesAsync("image.png");
```

### 异步文件读取参考

| 方法 | 返回值 | 描述 |
| --- | --- | --- |
| `File.ReadAllTextAsync(path)` | `Task<string>` | 将整个文件作为单个字符串读取 |
| `File.ReadAllLinesAsync(path)` | `Task<string[]>` | 将文件读取为行数组（按换行符拆分） |
| `File.ReadAllBytesAsync(path)` | `Task<byte[]>` | 将文件读取为原始字节数组（用于二进制文件） |

### 选择合适的方法

```csharp
// 对需要整体处理的文本内容使用 ReadAllTextAsync
string json = await File.ReadAllTextAsync("config.json");

// 需要逐行处理时使用 ReadAllLinesAsync
string[] logEntries = await File.ReadAllLinesAsync("app.log");
foreach (string entry in logEntries)
{
    Console.WriteLine(entry);
}

// 对二进制文件（图片、PDF 等）使用 ReadAllBytesAsync
byte[] imageData = await File.ReadAllBytesAsync("photo.jpg");
```

### 深入了解 File.ReadAllTextAsync

```csharp
// 签名：public static Task<string> ReadAllTextAsync(string path)

// 用法：
public static async Task<string> GetFileContentAsync(string path)
{
    // await 会解包 Task<string>，得到实际的字符串
    string text = await File.ReadAllTextAsync(path);
    return text;
}
```

### 你的任务

创建一个异步方法，该方法读取文件并返回前缀为 "Content: " 的文件内容。
这模拟了从文件中异步获取数据的实际应用场景。

### 方法签名

```csharp
public static async Task<string> ReadFileAsync(string filePath)
```

### 预期结果

```
ReadFileAsync("greeting.txt") -> "Content: Hello, World!"
ReadFileAsync("data.txt") -> "Content: Important data here"
```

### 解答

```csharp
using System;
using System.IO;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> ReadFileAsync(string filePath)
    {
        // 异步读取整个文件内容
        string content = await File.ReadAllTextAsync(filePath);
        return "Content: " + content;
    }
}
```
