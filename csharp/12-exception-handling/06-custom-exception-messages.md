### 自定义异常

内置异常类型（如 `ArgumentException`、`InvalidOperationException` 等）描述的是*通用*问题。
**自定义异常**是你自己定义的类，用于描述应用程序特有的问题，这样调用者就可以精确地捕获该故障并做出响应。
它还可以携带有关出错原因的额外数据，而不是将所有信息隐藏在文本消息中。

自定义异常在实际代码中的典型应用场景：

| 场景 | 自定义异常 | 作用 |
| --- | --- | --- |
| 调用 HTTP API | `ApiUnavailableException` (包含 `StatusCode`) | 调用者可以在 503 错误时重试，而在 400 错误时不重试 |
| 从数据库读取数据 | `RecordNotFoundException` (包含 `Id`) | 调用者可以返回 404 而不是 500 |
| 支付 / 领域规则 | `InsufficientFundsException` (包含 `Shortfall`) | UI 可以显示缺少多少金额 |

### 工作原理

自定义异常只是一个继承自 `Exception`（或更具体的异常类型）的类。
因为它继承自 `Exception`，所以可以使用 `throw` 抛出，它带有 `Message` 属性，并且可以被 `catch (MyException ex)` 捕获，如果调用者想要捕获所有异常，也可以使用 `catch (Exception ex)`。

你可以为想要保留的额外上下文添加构造函数参数，将它们存储在只读属性中，并将人类可读的文本传递给基类构造函数，使其成为 `Message`。

### 语法

```csharp
public class MyException : Exception
{
    public string ExtraData { get; }

    public MyException(string message, string extraData)
        : base(message)      // 设置 Message 属性
    {
        ExtraData = extraData;
    }
}

// 抛出异常
throw new MyException("Something specific went wrong", "context");
```

### 示例

```csharp
// 钱包的领域特定异常
public class InsufficientFundsException : Exception
{
    public decimal Shortfall { get; }

    public InsufficientFundsException(string message, decimal shortfall)
        : base(message)
    {
        Shortfall = shortfall;
    }
}

public static void Withdraw(decimal balance, decimal amount)
{
    if (amount > balance)
    {
        decimal missing = amount - balance;
        throw new InsufficientFundsException(
            $"Cannot withdraw {amount:0.00}. Balance is {balance:0.00}", missing);
    }
}

// 仅捕获你关心的故障
try
{
    Withdraw(50m, 80m);
}
catch (InsufficientFundsException ex)
{
    Console.WriteLine(ex.Message);      // "Cannot withdraw 80.00. Balance is 50.00"
    Console.WriteLine(ex.Shortfall);    // 30
}
```

### 编写消息

消息是开发人员在凌晨 3 点查看日志时阅读的内容，因此请务必具体并包含出错的值：

```csharp
// 模糊不清
throw new ArgumentException("Invalid value");

// 具体明确，包含实际值
throw new ArgumentException($"Quantity must be positive. Received: {quantity}");
```

### 任务

`InvalidAgeException.cs`（只读）已经定义了一个带有 `Message` 和 `ProvidedAge` 属性的自定义异常。
请实现 `ValidateAge`，要求如下：

- 接受 **0 到 150（含）** 之间的年龄，且不抛出任何异常。
- 年龄为负数时，抛出 `InvalidAgeException`，其消息为 `Age cannot be negative. Received: <age>`。
- 年龄超过 150 时，抛出 `InvalidAgeException`，其消息为 `Age cannot exceed 150. Received: <age>`。
- 在上述两种失败情况下，异常都必须在 `ProvidedAge` 中携带出错的年龄。

`Main.cs` 中的 `Describe` 方法是一个提供的测试工具：当没有抛出异常时，它返回 `"Valid"`；当你的异常被捕获时，它返回 `"<message> (ProvidedAge: <age>)"`。
测试会调用 `Describe`，所以请保持其原样。

### 方法签名

```csharp
public static void ValidateAge(int age)
```

### 预期结果

```
Describe(30)  -> Valid
Describe(-5)  -> Age cannot be negative. Received: -5 (ProvidedAge: -5)
Describe(200) -> Age cannot exceed 150. Received: 200 (ProvidedAge: 200)
```

### 解答

```csharp
using System;

public class Solution
{
    // 验证年龄。
    // 有效范围：0 到 150（含）。
    // 无效值必须抛出 InvalidAgeException（见 InvalidAgeException.cs），
    // 并携带描述性的消息以及出错的年龄。
    public static void ValidateAge(int age)
    {
        if (age < 0)
        {
            throw new InvalidAgeException($"Age cannot be negative. Received: {age}", age);
        }
        if (age > 150)
        {
            throw new InvalidAgeException($"Age cannot exceed 150. Received: {age}", age);
        }
    }

    // 测试使用的工具方法 - 请勿修改。
    // 它调用你的 ValidateAge，并将结果转换为字符串。
    public static string Describe(int age)
    {
        try
        {
            ValidateAge(age);
            return "Valid";
        }
        catch (InvalidAgeException ex)
        {
            return $"{ex.Message} (ProvidedAge: {ex.ProvidedAge})";
        }
    }
}
```
