### C# 中的 Enum

枚举（enum，即 enumeration）是一种值类型，它定义了一组具名常量，与直接使用原始整数或字符串相比，能让你的代码更具可读性和类型安全性。

### 声明 Enum

```csharp
// 基本枚举 - 默认从 0 开始
public enum Color
{
    Red,    // 0
    Green,  // 1
    Blue    // 2
}

// 显式指定值的枚举
public enum HttpStatus
{
    OK = 200,
    NotFound = 404,
    ServerError = 500
}
```

### 使用 Enum

```csharp
Color myColor = Color.Red;

// 比较枚举值
if (myColor == Color.Red)
{
    Console.WriteLine("It's red!");
}

// 对枚举值使用 switch
switch (myColor)
{
    case Color.Red:
        Console.WriteLine("Stop");
        break;
    case Color.Green:
        Console.WriteLine("Go");
        break;
}
```

### 为什么使用 Enum 而不是整数？

```csharp
// 不使用枚举 - 1 代表什么？
int status = 1; // 令人困惑！

// 使用枚举 - 代码即文档
OrderStatus status = OrderStatus.Shipped; // 清晰明了！
```

### 你的任务

1. 定义一个包含所有七天的 `DayOfWeek` 枚举：Sunday (0)、Monday (1)、Tuesday (2)、Wednesday (3)、Thursday (4)、Friday (5)、Saturday (6)
2. 实现 `GetDayType`，对于 Saturday 和 Sunday 返回 `"Weekend"`，其他所有天返回 `"Weekday"`

### 方法签名

```csharp
public static string GetDayType(DayOfWeek day)
```

### 预期结果

```
GetDayType(DayOfWeek.Monday) -> "Weekday"
GetDayType(DayOfWeek.Saturday) -> "Weekend"
GetDayType(DayOfWeek.Sunday) -> "Weekend"
```

### 解答

```csharp
using System;

// 定义包含所有七天的 DayOfWeek 枚举
// Sunday 为 0，Monday 为 1，依此类推
public enum DayOfWeek
{
    Sunday,     // 0
    Monday,     // 1
    Tuesday,    // 2
    Wednesday,  // 3
    Thursday,   // 4
    Friday,     // 5
    Saturday    // 6
}

public class Solution
{
    public static string GetDayType(DayOfWeek day)
    {
        // Saturday 和 Sunday 返回 "Weekend"
        if (day == DayOfWeek.Saturday || day == DayOfWeek.Sunday)
        {
            return "Weekend";
        }
        // Monday 至 Friday 返回 "Weekday"
        return "Weekday";
    }
}
```
