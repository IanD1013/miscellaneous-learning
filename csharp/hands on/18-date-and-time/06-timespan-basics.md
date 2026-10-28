### TimeSpan 基础

`TimeSpan` 表示时间间隔，即两个时间点之间的差值或一个固定的时间区间。

### 创建 TimeSpan 值

```csharp
// 使用构造函数
TimeSpan ts1 = new TimeSpan(1, 30, 0);        // 1 小时 30 分钟 0 秒
TimeSpan ts2 = new TimeSpan(2, 12, 30, 45);   // 2 天 12 小时 30 分钟 45 秒

// 使用静态工厂方法（推荐）
TimeSpan oneDay = TimeSpan.FromDays(1);
TimeSpan twoHours = TimeSpan.FromHours(2);
TimeSpan thirtyMinutes = TimeSpan.FromMinutes(30);
TimeSpan tenSeconds = TimeSpan.FromSeconds(10);
```

### 通过日期相减获取 TimeSpan

```csharp
DateTime start = new DateTime(2024, 1, 1);
DateTime end = new DateTime(2024, 1, 15);

TimeSpan difference = end - start;  // 14 天
```

### Total 与 Component 属性对比

`TimeSpan` 具有两组属性 - 分量值（component values）和总量值（total values）：

| 属性 | 说明 | 示例（1 天 6 小时） |
| --- | --- | --- |
| Days | 完整天数分量 | 1 |
| Hours | 小时分量 (0-23) | 6 |
| TotalDays | 包含小数的总天数 | 1.25 |
| TotalHours | 包含小数的总小时数 | 30.0 |
| TotalMinutes | 包含小数的总分钟数 | 1800.0 |

```csharp
TimeSpan span = new TimeSpan(1, 6, 30, 0);  // 1 天 6 小时 30 分钟

int days = span.Days;           // 1（分量）
int hours = span.Hours;         // 6（分量）
double totalDays = span.TotalDays;     // 1.270833...
double totalHours = span.TotalHours;   // 30.5
```

### 你的任务

编写一个方法，计算两个日期之间的**完整天数**。
无论哪个日期在前，结果都应始终为正数。

### 方法签名

```csharp
public static int GetDaysBetween(DateTime startDate, DateTime endDate)
```

### 预期结果

```
GetDaysBetween(2024-01-01, 2024-01-15) -> 14
GetDaysBetween(2024-01-15, 2024-01-01) -> 14
GetDaysBetween(2024-01-01, 2024-01-01) -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetDaysBetween(DateTime startDate, DateTime endDate)
    {
        // 计算两个日期之间的完整天数
        // 无论日期顺序如何都返回正数
        TimeSpan difference = endDate - startDate;
        return Math.Abs(difference.Days);
    }
}
```
