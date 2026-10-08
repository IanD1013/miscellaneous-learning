### Try-Catch 语句块

异常处理允许您的程序优雅地处理错误而不是直接崩溃。
`try-catch` 语句块是 C# 中捕获和处理异常的基本结构。

### 基本语法

```csharp
try
{
    // 可能抛出异常的代码
    int result = 10 / 0;  // 这里会抛出 DivideByZeroException
}
catch (DivideByZeroException ex)
{
    // 处理异常的代码
    Console.WriteLine("An error occurred!");
}
```

### 工作原理

1. `try` 块内的代码正常执行
2. 如果发生异常，执行流程会立即跳转到 `catch` 块
3. 如果没有发生异常，`catch` 块会被完全跳过

```csharp
// 成功执行的示例
try
{
    int result = 10 / 2;  // 没有异常
    Console.WriteLine(result);  // 输出：5
}
catch (DivideByZeroException)
{
    Console.WriteLine("This won't print");
}

// 发生异常的示例
try
{
    int result = 10 / 0;  // 抛出异常！
    Console.WriteLine(result);  // 这一行永远不会执行
}
catch (DivideByZeroException)
{
    Console.WriteLine("Caught it!");  // 输出：Caught it!
}
```

### 捕获特定异常

您可以捕获特定的异常类型来分别处理不同的错误：

| 异常类型 | 发生时机 |
| --- | --- |
| `DivideByZeroException` | 整数除以零 |
| `NullReferenceException` | 访问 null 对象的成员 |
| `IndexOutOfRangeException` | 数组索引越界 |
| `Exception` | 捕获任何异常（基类） |

### 你的任务

编写一个尝试将两个整数相除的方法。
如果除数为零，捕获 `DivideByZeroException` 并打印一条友好的错误消息。

### 方法签名

```csharp
public static void SafeDivide(int dividend, int divisor)
```

### 预期输出

```
SafeDivide(10, 2)  -> prints "Result: 5"
SafeDivide(20, 4)  -> prints "Result: 5"
SafeDivide(10, 0)  -> prints "Error: Cannot divide by zero!"
SafeDivide(0, 5)   -> prints "Result: 0"
```

### 解答

```csharp
using System;

public class Solution
{
    public static void SafeDivide(int dividend, int divisor)
    {
        try
        {
            // 尝试相除并打印结果
            int result = dividend / divisor;
            Console.WriteLine($"Result: {result}");
        }
        catch (DivideByZeroException)
        {
            // 除数为零时捕获异常并打印友好的错误消息
            Console.WriteLine("Error: Cannot divide by zero!");
        }
    }
}
```
