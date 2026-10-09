### DateTime 基础

C# 中的 `DateTime` 结构体用于表示日期和时间。
它是 .NET 应用程序中处理时间数据的基础。

### 获取当前日期和时间

```csharp
// 获取当前日期和时间
DateTime now = DateTime.Now;  // 例如：2024-03-15 14:30:45

// 获取今天的日期（时间为 00:00:00）
DateTime today = DateTime.Today;  // 例如：2024-03-15 00:00:00
```

### DateTime.Now 与 DateTime.Today

| 属性 | 返回值 | 时间部分 |
| --- | --- | --- |
| DateTime.Now | 当前日期和时间 | 实际的当前时间 |
| DateTime.Today | 仅当前日期 | 午夜（00:00:00） |

### 访问各个组成部分

每个 `DateTime` 值都有用于访问其各部分的属性：

```csharp
DateTime now = DateTime.Now;

int year = now.Year;      // 例如：2024
int month = now.Month;    // 1-12
int day = now.Day;        // 1-31
int hour = now.Hour;      // 0-23
int minute = now.Minute;  // 0-59
int second = now.Second;  // 0-59
```

### 使用字符串拼接构建输出

```csharp
// 使用字符串拼接组合各个值
Console.WriteLine(year + "-" + month + "-" + day);
// 输出：2024-3-15
```

### 你的任务

编写一个方法，按以下格式打印：

1. 今天的日期，格式为：`Year-Month-Day`
2. 当前的时间，格式为：`Hour:Minute:Second`

每个值都应该单独打印在一行上。

### 方法签名

```csharp
public static void PrintDateAndTime()
```

### 预期输出格式

```
2024-3-15
14:30:45
```

注意：实际值将取决于代码运行的时间。
日期行使用 `DateTime.Today`，时间行使用 `DateTime.Now`。

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintDateAndTime()
    {
        // 获取当前日期和时间
        DateTime today = DateTime.Today;
        DateTime now = DateTime.Now;

        // 按 Year-Month-Day 格式打印今天的日期
        Console.WriteLine(today.Year + "-" + today.Month + "-" + today.Day);

        // 按 Hour:Minute:Second 格式打印当前时间
        Console.WriteLine(now.Hour + ":" + now.Minute + ":" + now.Second);
    }
}
```
