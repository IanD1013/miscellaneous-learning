### 转义序列

转义序列是特殊的字符组合，用于表示无法直接在字符串中输入的字符，例如换行符、制表符或引号。

### 常用转义序列

| 转义序列 | 描述 | 示例输出 |
| --- | --- | --- |
| `\n` | 换行 | Line 1↵Line 2 |
| `\t` | 制表符（缩进） | Hello→World |
| `\\` | 反斜杠 | C:\Users |
| `\"` | 双引号 | He said "Hi" |

### 使用转义序列

```csharp
// 换行 - 创建多行
Console.WriteLine("Line 1\nLine 2");
// 输出：
// Line 1
// Line 2

// 制表符 - 添加水平间距
Console.WriteLine("Name:\tJohn");
// 输出：Name:    John

// 反斜杠 - 用于文件路径
Console.WriteLine("C:\\Program Files\\App");
// 输出：C:\Program Files\App

// 字符串中的引号
Console.WriteLine("She said \"Hello!\"");
// 输出：She said "Hello!"
```

### 组合转义序列

```csharp
Console.WriteLine("\"Quote\"\n\tIndented line");
// 输出：
// "Quote"
//     Indented line
```

### 你的任务

打印一条恰好包含 4 行的格式化消息：

1. `"Welcome to C#!"`（包含可见的双引号）
2. 一个空行
3. `Path: C:\Users\Documents`（包含单个反斜杠）
4. `Indented with a tab`（以制表符开头）

### 方法签名

```csharp
public static void PrintFormattedMessage()
```

### 预期输出

```
"Welcome to C#!"

Path: C:\Users\Documents
	Indented with a tab
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintFormattedMessage()
    {
        // 第 1 行：用 \" 输出双引号
        // 第 2 行：用 \n\n 产生一个空行
        // 第 3 行：用 \\ 输出单个反斜杠
        // 第 4 行：用 \t 以制表符开头
        Console.WriteLine("\"Welcome to C#!\"\n\nPath: C:\\Users\\Documents\n\tIndented with a tab");
    }
}
```
