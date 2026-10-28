### 抛出异常

当代码检测到错误情况时，`throw` 关键字会引发异常。
这使你能够向调用方代码发出问题信号，而不是返回无效的结果。

### 基本语法

```csharp
// 抛出一个新的异常
throw new Exception("Something went wrong");

// 抛出特定类型的异常
throw new ArgumentException("Invalid argument");
throw new InvalidOperationException("Cannot perform this action");
```

### ArgumentException

当方法接收到无效参数时，会抛出 `ArgumentException`。
它能清晰地传达调用方提供了错误输入的信息。

```csharp
public static void SetAge(int age)
{
    if (age < 0)
    {
        throw new ArgumentException("Age cannot be negative");
    }
    // 使用有效的年龄继续执行...
}
```

### 卫语句模式（Guard Clauses Pattern）

在方法开头检查参数被称为“卫语句”（guard clause），它可以保护后续代码免受无效输入的影响。

```csharp
public static string Greet(string name)
{
    if (string.IsNullOrEmpty(name))
    {
        throw new ArgumentException("Name cannot be empty");
    }
    return $"Hello, {name}!";
}
```

### 你的任务

创建一个计算数字的整数平方根的方法。
由于负数没有实数平方根（在实数范围内未定义），当输入为负数时，抛出一个带有消息 `"Number cannot be negative"` 的 `ArgumentException`。

对于有效输入，返回平方根的整数部分。

### 方法签名

```csharp
public static int CalculateSquareRoot(int number)
```

### 预期结果

```
CalculateSquareRoot(16) -> 4
CalculateSquareRoot(25) -> 5
CalculateSquareRoot(0) -> 0
CalculateSquareRoot(-1) -> throws ArgumentException
```

### 解答

```csharp
using System;

public class Solution
{
    public static int CalculateSquareRoot(int number)
    {
        // 数字为负数时抛出 ArgumentException
        if (number < 0)
        {
            throw new ArgumentException("Number cannot be negative");
        }
        // 对有效数字返回平方根的整数部分
        return (int)Math.Sqrt(number);
    }
}
```
