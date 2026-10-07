### Console.Write 与 Console.WriteLine

在 C# 中，主要有两种输出文本的方式：`Console.WriteLine()` 会在文本后添加换行符，而 `Console.Write()` 则将光标保持在同一行。

### 基本用法

```csharp
// Console.WriteLine 会在输出后添加换行符
Console.WriteLine("Hello");
Console.WriteLine("World");
// 输出：
// Hello
// World

// Console.Write 保持在同一行
Console.Write("Hello");
Console.Write("World");
// 输出：HelloWorld
```

### 结合使用两种方法

```csharp
// 你可以混合使用 Write 和 WriteLine
Console.Write("Name: ");
Console.WriteLine("Alice");
// 输出：Name: Alice

Console.Write("Score: ");
Console.Write(100);
Console.WriteLine(" points");
// 输出：Score: 100 points
```

### 主要区别

| 方法 | 添加换行符 | 使用场景 |
| --- | --- | --- |
| `Console.WriteLine()` | 是 | 完整的单行输出 |
| `Console.Write()` | 否 | 逐段构建输出内容 |

### 你的任务

结合使用 `Console.Write` 和 `Console.WriteLine` 创建一条问候语。
首先，使用 `Console.Write` 打印 `Hello,` （包含空格），然后使用 `Console.WriteLine` 打印 `World!`。

### 方法签名

```csharp
public static void PrintGreeting()
```

### 预期输出

```
Hello, World!
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintGreeting()
    {
        // 使用 Console.Write 打印，不添加换行符
        Console.Write("Hello, ");
        // 然后使用 Console.WriteLine 补全这条消息
        Console.WriteLine("World!");
    }
}
```
