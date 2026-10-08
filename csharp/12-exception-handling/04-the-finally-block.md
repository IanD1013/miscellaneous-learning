### Finally 块

`finally` 块包含在 try-catch 之后**始终执行**的代码，无论是否发生异常。
它用于清理操作和确保执行的操作。

### 基本结构

```csharp
try
{
    // 可能抛出异常的代码
}
catch (Exception ex)
{
    // 处理异常
}
finally
{
    // 这里始终会执行 - 无论是否发生异常
}
```

### Finally 何时执行

```csharp
// 场景 1：没有异常
try
{
    Console.WriteLine("Success");
}
finally
{
    Console.WriteLine("Cleanup"); // 在 "Success" 之后执行
}

// 场景 2：异常被捕获
try
{
    throw new Exception("Oops");
}
catch (Exception)
{
    Console.WriteLine("Error handled");
}
finally
{
    Console.WriteLine("Cleanup"); // 在 "Error handled" 之后执行
}
```

### 常见用例

| 用例 | 示例 |
| --- | --- |
| 关闭文件 | `file.Close()` |
| 释放资源 | `connection.Dispose()` |
| 记录完成日志 | `Console.WriteLine("Done")` |
| 重置状态 | `isProcessing = false` |

### 你的任务

编写一个方法，尝试将字符串解析为整数并将其翻倍：

1. 如果解析成功，打印翻倍后的值
2. 如果解析失败（抛出 `FormatException`），打印 `Invalid input`
3. **始终**在最后使用 `finally` 块打印 `Done`

### 方法签名

```csharp
public static void ProcessNumber(string input)
```

### 预期结果

```
ProcessNumber("5") -> prints "10" then "Done"
ProcessNumber("abc") -> prints "Invalid input" then "Done"
ProcessNumber("0") -> prints "0" then "Done"
```

### 解答

```csharp
using System;

public class Solution
{
    public static void ProcessNumber(string input)
    {
        try
        {
            // 1. 尝试将输入解析为整数
            int number = int.Parse(input);
            // 2. 解析成功时打印翻倍后的值
            Console.WriteLine(number * 2);
        }
        catch (FormatException)
        {
            // 3. 解析失败时打印 "Invalid input"
            Console.WriteLine("Invalid input");
        }
        finally
        {
            // 4. 使用 finally 始终在最后打印 "Done"
            Console.WriteLine("Done");
        }
    }
}
```
