### 日期运算

`DateTime` 提供了添加或减去时间段的方法，两个日期相减会得到一个表示时间差的 `TimeSpan`。

### 为日期增加时间

```csharp
DateTime today = new DateTime(2024, 1, 15);

// 增加天数
DateTime nextWeek = today.AddDays(7);      // 2024-01-22
DateTime lastWeek = today.AddDays(-7);     // 2024-01-08

// 增加月数
DateTime nextMonth = today.AddMonths(1);   // 2024-02-15
DateTime lastYear = today.AddMonths(-12);  // 2023-01-15

// 增加年数
DateTime fiveYearsLater = today.AddYears(5); // 2029-01-15
```

### 日期相减 (TimeSpan)

```csharp
DateTime start = new DateTime(2024, 1, 1);
DateTime end = new DateTime(2024, 1, 31);

// 日期相减返回一个 TimeSpan
TimeSpan difference = end - start;

int totalDays = (int)difference.TotalDays;    // 30
double totalHours = difference.TotalHours;    // 720
```

### 关键方法

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| `AddDays(n)` | 增加/减少天数 | `date.AddDays(30)` |
| `AddMonths(n)` | 增加/减少月数 | `date.AddMonths(-1)` |
| `AddYears(n)` | 增加/减少年数 | `date.AddYears(5)` |
| `date2 - date1` | 获取两者之间的 TimeSpan | `end - start` |

### 你的任务

实现四个方法：

1. `AddDaysToDate` - 为日期增加指定天数
2. `AddMonthsToDate` - 为日期增加指定月数
3. `AddYearsToDate` - 为日期增加指定年数
4. `GetDaysBetween` - 计算两个日期之间的天数

### 预期结果

```
AddDaysToDate(2024-01-01, 30) -> 2024-01-31
AddMonthsToDate(2024-01-15, 2) -> 2024-03-15
GetDaysBetween(2024-01-01, 2024-02-01) -> 31
```

### 解答

```csharp
using System;

public class Solution
{
    public static DateTime AddDaysToDate(DateTime date, int days)
    {
        // 为日期增加指定天数
        return date.AddDays(days);
    }
    
    public static DateTime AddMonthsToDate(DateTime date, int months)
    {
        // 为日期增加指定月数
        return date.AddMonths(months);
    }
    
    public static DateTime AddYearsToDate(DateTime date, int years)
    {
        // 为日期增加指定年数
        return date.AddYears(years);
    }
    
    public static int GetDaysBetween(DateTime start, DateTime end)
    {
        // 计算两个日期之间的天数
        TimeSpan difference = end - start;
        return (int)difference.TotalDays;
    }
}
```
