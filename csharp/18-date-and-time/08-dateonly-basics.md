### DateOnly 基础

`DateOnly` 表示不包含任何时间部分的日期，非常适合生日、节日或任何不需要时间的场景。

### 创建 DateOnly 值

```csharp
// 使用构造函数
DateOnly christmas = new DateOnly(2024, 12, 25);

// 从现有的 DateTime 创建
DateTime now = DateTime.Now;
DateOnly today = DateOnly.FromDateTime(now);

// 从字符串解析
DateOnly parsed = DateOnly.Parse("2024-07-04");
```

### 访问属性

```csharp
DateOnly date = new DateOnly(2024, 3, 15);

int year = date.Year;        // 2024
int month = date.Month;      // 3
int day = date.Day;          // 15
DayOfWeek dow = date.DayOfWeek;  // Friday
```

### DateOnly 与 DateTime

| 方面 | DateOnly | DateTime |
| --- | --- | --- |
| 时间部分 | 否 | 是 |
| 内存大小 | 4 字节 | 8 字节 |
| 使用场景 | 仅日期 | 日期 + 时间 |

### 在类型之间转换

```csharp
// DateOnly 转 DateTime（需要时间部分）
DateOnly date = new DateOnly(2024, 6, 15);
DateTime dateTime = date.ToDateTime(TimeOnly.MinValue);

// DateTime 转 DateOnly
DateTime now = DateTime.Now;
DateOnly today = DateOnly.FromDateTime(now);
```

### 你的任务

创建一个方法，该方法接收年、月、日作为整数，使用它们创建一个 `DateOnly`，并将星期几作为字符串返回。

### 方法签名

```csharp
public static string GetDayOfWeek(int year, int month, int day)
```

### 预期结果

```
GetDayOfWeek(2024, 1, 1) -> "Monday"
GetDayOfWeek(2024, 12, 25) -> "Wednesday"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetDayOfWeek(int year, int month, int day)
    {
        // 用参数创建 DateOnly，并以字符串形式返回星期几
        DateOnly date = new DateOnly(year, month, day);
        return date.DayOfWeek.ToString();
    }
}
```
