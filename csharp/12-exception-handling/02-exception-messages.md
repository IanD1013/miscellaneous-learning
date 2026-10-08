### 异常信息

当抛出异常时，它会携带有关出错原因的信息。
`Message` 属性包含人类可读的错误描述。

### 访问 Message 属性

```csharp
try
{
    // 可能抛出异常的代码
}
catch (Exception ex)
{
    Console.WriteLine(ex.Message);  // 打印错误消息
}
```

### 具名异常变量

要访问异常属性，必须使用变量为捕获的异常命名：

```csharp
// 不带变量 - 无法访问属性
catch (Exception)
{
    // 这里无法访问 Message
}

// 带变量 - 可以访问属性
catch (Exception ex)
{
    Console.WriteLine(ex.Message);  // 现在可以访问了！
    Console.WriteLine(ex.StackTrace);  // 其他属性也可以使用
}
```

### 常见的异常属性

| 属性 | 描述 | 示例 |
| --- | --- | --- |
| Message | 错误描述 | "Input string was not in a correct format." |
| StackTrace | 抛出时的调用堆栈 | 方法名称和行号 |
| Source | 应用程序名称 | "MyApp" |

### 你的任务

编写一个方法，尝试使用 `int.Parse()` 将字符串解析为整数。
如果解析成功，打印 `Parsed: {number}`。
如果解析失败（抛出 `FormatException`），捕获该异常并打印其 `Message` 属性。

### 方法签名

```csharp
public static void PrintExceptionMessage(string input)
```

### 预期结果

```
PrintExceptionMessage("42") -> Prints: Parsed: 42
PrintExceptionMessage("abc") -> Prints: The input string 'abc' was not in a correct format.
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintExceptionMessage(string input)
    {
        try
        {
            // 尝试将输入解析为整数
            int number = int.Parse(input);
            Console.WriteLine($"Parsed: {number}");
        }
        catch (FormatException ex)
        {
            // 解析失败时捕获异常并打印其 Message 属性
            Console.WriteLine(ex.Message);
        }
    }
}
```
