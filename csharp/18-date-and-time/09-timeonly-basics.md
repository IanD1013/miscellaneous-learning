### TimeOnly 基础

`TimeOnly` 表示一天中的某个时间，不包含日期部分，非常适合用于日程安排、营业时间或任何只需要关注时间的场景。

### 创建 TimeOnly 值

```csharp
// 通过小时和分钟创建
var morning = new TimeOnly(9, 30);        // 09:30:00

// 通过小时、分钟和秒创建
var precise = new TimeOnly(14, 30, 45);   // 14:30:45

// 通过 TimeSpan 创建
var fromSpan = TimeOnly.FromTimeSpan(TimeSpan.FromHours(8.5)); // 08:30:00

// 当前时间
var now = TimeOnly.FromDateTime(DateTime.Now);
```

### TimeOnly 与 DateTime

| 方面 | TimeOnly | DateTime |
| --- | --- | --- |
| 表示内容 | 仅时间 | 日期和时间 |
| 范围 | 00:00:00 至 23:59:59.9999999 | 完整日历范围 |
| 使用场景 | 日程安排、营业时间 | 事件、时间戳 |

### 格式化 TimeOnly

```csharp
var time = new TimeOnly(14, 30, 15);

time.ToString("HH:mm:ss");  // "14:30:15"（24 小时制）
time.ToString("hh:mm tt"); // "02:30 PM"（带 AM/PM 的 12 小时制）
time.ToString("HH:mm");    // "14:30"（不含秒）
```

### 比较时间

```csharp
var early = new TimeOnly(8, 0);
var late = new TimeOnly(17, 0);
var current = new TimeOnly(12, 0);

bool isOpen = current >= early && current < late; // true
bool isAfterClose = current > late;               // false
```

### 时间运算

```csharp
var start = new TimeOnly(9, 0);
var end = new TimeOnly(17, 30);

TimeSpan duration = end - start;  // 08:30:00

var later = start.AddHours(2);    // 11:00
var earlier = end.AddMinutes(-30); // 17:00
```

### 你的任务

实现以下三个方法：

1. **FormatTime**：从小时（hour）、分钟（minute）、秒（second）创建 `TimeOnly` 并格式化为 "HH:mm:ss"
2. **GetMinutesUntil**：计算从当前时间到目标时间的分钟数（如果目标时间更早，则假定为第二天）
3. **IsBusinessHours**：检查时间是否在 09:00-17:00 之间（包含开始时间，不包含结束时间）

### 预期结果

```
FormatTime(14, 30, 0) -> "14:30:00"
FormatTime(9, 5, 30) -> "09:05:30"
GetMinutesUntil(9, 0, 10, 30) -> 90
GetMinutesUntil(23, 0, 1, 0) -> 120
IsBusinessHours(9, 0) -> true
IsBusinessHours(17, 0) -> false
```

### 解答

```csharp
using System;

public class Solution
{
    public static string FormatTime(int hour, int minute, int second)
    {
        // 创建 TimeOnly 并按 HH:mm:ss 格式返回
        var time = new TimeOnly(hour, minute, second);
        return time.ToString("HH:mm:ss");
    }
    
    public static int GetMinutesUntil(int currentHour, int currentMinute, int targetHour, int targetMinute)
    {
        // 计算两个时间之间的分钟数（target - current）
        // 如果目标时间更早，表示是第二天 - 返回正的分钟数
        var current = new TimeOnly(currentHour, currentMinute);
        var target = new TimeOnly(targetHour, targetMinute);

        // TimeOnly 相减会在午夜处回绕，结果总是非负的 TimeSpan
        TimeSpan duration = target - current;
        return (int)duration.TotalMinutes;
    }
    
    public static bool IsBusinessHours(int hour, int minute)
    {
        // 如果时间在 09:00 到 17:00 之间（包含开始时间，不包含结束时间）则返回 true
        var time = new TimeOnly(hour, minute);
        var open = new TimeOnly(9, 0);
        var close = new TimeOnly(17, 0);
        return time >= open && time < close;
    }
}
```
