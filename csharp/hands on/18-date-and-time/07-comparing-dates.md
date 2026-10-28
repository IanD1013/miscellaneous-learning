### 比较日期

可以使用标准比较运算符来比较 `DateTime` 值，从而轻松确定时间先后顺序或检查日期是否落在特定时期内。

### 比较运算符

```csharp
DateTime date1 = new DateTime(2024, 1, 15);
DateTime date2 = new DateTime(2024, 6, 20);

bool isBefore = date1 < date2;   // True - date1 更早
bool isAfter = date1 > date2;    // False - date1 不是更晚
bool isEqual = date1 == date2;   // False - 日期不同
bool notEqual = date1 != date2;  // True - 日期不相同
```

### 检查过去和未来

```csharp
DateTime appointment = new DateTime(2025, 3, 15);
DateTime now = DateTime.Now;

bool isInPast = appointment < now;    // 该日期是否早于现在？
bool isInFuture = appointment > now;  // 该日期是否晚于现在？
bool isToday = appointment.Date == now.Date;  // 是否为同一个日历日？
```

### DateTime.Now 与 DateTime.Today

| 属性 | 返回值 | 示例 |
| --- | --- | --- |
| DateTime.Now | 当前日期和时间 | 2024-03-15 14:30:45 |
| DateTime.Today | 当前日期的午夜零点 | 2024-03-15 00:00:00 |

### CompareTo 方法

```csharp
int result = date1.CompareTo(date2);
// 返回：如果 date1 < date2 返回 -1
//       如果 date1 == date2 返回 0
//       如果 date1 > date2 返回 1
```

### 你的任务

编写一个方法，检查给定的 `DateTime` 是否在未来（晚于当前时刻）。

### 方法签名

```csharp
public static bool IsInFuture(DateTime date)
```

### 预期结果

```
IsInFuture(DateTime.Now.AddDays(1)) -> True
IsInFuture(DateTime.Now.AddDays(-1)) -> False
IsInFuture(DateTime.Now.AddYears(10)) -> True
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool IsInFuture(DateTime date)
    {
        // 检查该日期是否在未来
        return date > DateTime.Now;
    }
}
```
