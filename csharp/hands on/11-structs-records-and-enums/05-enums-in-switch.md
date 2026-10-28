### Switch 语句中的枚举

Switch 语句与枚举是绝配。
编译器可以验证你是否处理了所有的枚举值，从而使你的代码更安全、更具可维护性。

### 基本枚举 Switch

```csharp
enum TrafficLight { Red, Yellow, Green }

string GetAction(TrafficLight light)
{
    switch (light)
    {
        case TrafficLight.Red:
            return "Stop";
        case TrafficLight.Yellow:
            return "Caution";
        case TrafficLight.Green:
            return "Go";
        default:
            return "Unknown";
    }
}
```

### 合并多个 Case

当多个枚举值应该产生相同的结果时，可以堆叠这些 case：

```csharp
enum Season { Spring, Summer, Fall, Winter }

string GetTemperature(Season season)
{
    switch (season)
    {
        case Season.Summer:
            return "Hot";
        case Season.Winter:
            return "Cold";
        case Season.Spring:
        case Season.Fall:
            return "Mild";  // Spring 和 Fall 都返回 "Mild"
        default:
            return "Unknown";
    }
}
```

### DayOfWeek 枚举

C# 在 `System` 命名空间中提供了内置的 `DayOfWeek` 枚举：

```csharp
// DayOfWeek 的值：
// Sunday = 0, Monday = 1, Tuesday = 2, Wednesday = 3,
// Thursday = 4, Friday = 5, Saturday = 6

DayOfWeek today = DayOfWeek.Monday;
```

### 你的任务

编写一个方法，接收一个 `DayOfWeek` 枚举值并返回：

- Saturday 和 Sunday 返回 `"Weekend"`
- Monday 至 Friday 返回 `"Weekday"`

### 方法签名

```csharp
public static string GetDayType(DayOfWeek day)
```

### 预期结果

```
GetDayType(DayOfWeek.Monday) -> "Weekday"
GetDayType(DayOfWeek.Saturday) -> "Weekend"
GetDayType(DayOfWeek.Friday) -> "Weekday"
GetDayType(DayOfWeek.Sunday) -> "Weekend"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetDayType(DayOfWeek day)
    {
        switch (day)
        {
            // 堆叠 case：Saturday 和 Sunday 都返回 "Weekend"
            case DayOfWeek.Saturday:
            case DayOfWeek.Sunday:
                return "Weekend";
            // 其余的 Monday 至 Friday 返回 "Weekday"
            default:
                return "Weekday";
        }
    }
}
```
