### 处理文件中的行

虽然 `File.ReadAllText` 会将整个文件读取为一个字符串，但 `File.ReadAllLines` 会读取文件并将每一行作为字符串数组中的单独元素返回。
当你需要逐行处理文件时，这非常理想。

### ReadAllLines 对比 ReadAllText

```csharp
// ReadAllText - 返回一个包含换行符的字符串
string content = File.ReadAllText("data.txt");
// content = "Apple\nBanana\nCherry"

// ReadAllLines - 返回字符串数组
string[] lines = File.ReadAllLines("data.txt");
// lines[0] = "Apple"
// lines[1] = "Banana"
// lines[2] = "Cherry"
```

### WriteAllLines - 对应的写入方法

```csharp
// 将字符串数组按行分别写入
string[] fruits = { "Apple", "Banana", "Cherry" };
File.WriteAllLines("output.txt", fruits);
// 创建的文件中每种水果各占一行
```

### 常见用例

| 方法 | 适用场景 |
| --- | --- |
| `ReadAllLines` | 处理 CSV 文件、日志文件、配置文件 |
| `WriteAllLines` | 保存列表、导出数据、生成报告 |

### 你的任务

实现一个方法，读取文本文件并将其内容作为字符串数组返回，其中每个元素代表文件中的一行。

### 方法签名

```csharp
public static string[] ReadFileLines(string filePath)
```

### 预期结果

```scss
ReadFileLines("fruits.txt") -> ["Apple", "Banana", "Cherry"]
ReadFileLines("numbers.txt") -> ["1", "2", "3", "4", "5"]
ReadFileLines("empty.txt") -> []
```

### 解答

```csharp
using System;
using System.IO;

public class Solution
{
    public static string[] ReadFileLines(string filePath)
    {
        // 读取文件，每一行作为数组中的一个元素返回
        return File.ReadAllLines(filePath);
    }
}
```
