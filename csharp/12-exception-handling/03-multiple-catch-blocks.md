### 多个 Catch 块

当代码可能会抛出不同类型的异常时，你可以使用多个 catch 块分别处理每种类型。
这使你能够针对每种情况提供具体的错误消息和恢复逻辑。

### 基本语法

```csharp
try
{
    // 可能抛出不同异常的代码
}
catch (SpecificException1 ex)
{
    // 处理 SpecificException1
}
catch (SpecificException2 ex)
{
    // 处理 SpecificException2
}
```

### 顺序很重要

C# 从上到下依次检查 catch 块。
更具体的异常应该放在更通用的异常之前：

```csharp
try
{
    int x = int.Parse("abc");  // 抛出 FormatException
}
catch (FormatException)       // 捕获解析错误
{
    Console.WriteLine("Not a valid number");
}
catch (Exception)             // 捕获其他所有异常
{
    Console.WriteLine("Something went wrong");
}
```

### 常见异常类型

| 异常 | 抛出时机 |
| --- | --- |
| `FormatException` | 字符串无法解析为目标类型 |
| `DivideByZeroException` | 整数被零除 |
| `ArgumentNullException` | 在不允许的地方传递了 null |
| `IndexOutOfRangeException` | 数组索引无效 |

### 你的任务

创建一个接收两个表示数字的字符串输入的方法。
将它们解析为整数，用第一个数字除以第二个数字，并打印结果。
分别使用具体的错误消息来处理 `FormatException` 和 `DivideByZeroException`。

### 方法签名

```csharp
public static void ProcessInput(string numberText, string divisorText)
```

### 预期结果

```
ProcessInput("10", "2") -> prints "Result: 5"
ProcessInput("abc", "2") -> prints "Error: Invalid number format"
ProcessInput("10", "0") -> prints "Error: Cannot divide by zero"
```

### 解答

```csharp
using System;

public class Solution
{
    public static void ProcessInput(string numberText, string divisorText)
    {
        try
        {
            // 1. 将两个字符串解析为整数
            int number = int.Parse(numberText);
            int divisor = int.Parse(divisorText);
            // 2. 用第一个数字除以第二个数字
            int result = number / divisor;
            // 3. 打印结果
            Console.WriteLine($"Result: {result}");
        }
        // 4. 分别处理 FormatException 和 DivideByZeroException
        catch (FormatException)
        {
            Console.WriteLine("Error: Invalid number format");
        }
        catch (DivideByZeroException)
        {
            Console.WriteLine("Error: Cannot divide by zero");
        }
    }
}
```
