### Switch 表达式

Switch 表达式是 switch 语句的一种简洁的、基于表达式的替代方案。
它们直接返回一个值，并使用 `=>` 箭头语法。

### 基本语法

```csharp
// Switch 表达式语法
var result = value switch
{
    pattern1 => result1,
    pattern2 => result2,
    _ => defaultResult  // 弃元模式 (default)
};
```

### Switch 语句与 Switch 表达式对比

```csharp
// 传统的 switch 语句 (冗长)
string GetGrade(int score)
{
    switch (score)
    {
        case 10:
            return "A+";
        case 9:
            return "A";
        default:
            return "B";
    }
}

// Switch 表达式 (简洁)
string GetDayName(int score) => score switch
{
    10 => "A+",
    9 => "A",
    _ => "B"
};
```

### 主要区别

| 特性 | Switch 语句 | Switch 表达式 |
| --- | --- | --- |
| 返回值 | 通过 `return` | 直接返回 |
| 使用 `case:` | 是 | 否，使用 `=>` |
| 使用 `break` | 是 | 否 |
| 默认情况 | `default:` | `_` (弃元) |
| 未匹配的值 | 不执行任何操作，继续执行 switch 后的代码 | 编译器警告 (CS8509) 并在运行时抛出 `SwitchExpressionException`。添加 `_` 分支来覆盖它 |

### 弃元模式 `_`

下划线 `_` 是弃元模式，它匹配任何未被之前模式匹配的内容。
它等同于 switch 语句中的 `default`。

### 任务

创建一个方法，使用 **switch 表达式** 将天数编号 (1-7) 转换为对应的星期名称。

- 1 = "Monday"
- 2 = "Tuesday"
- 3 = "Wednesday"
- 4 = "Thursday"
- 5 = "Friday"
- 6 = "Saturday"
- 7 = "Sunday"
- 其他任何数字 = "Invalid day"

### 方法签名

```csharp
public static string GetDayName(int dayNumber)
```

### 预期结果

```
GetDayName(1) -> "Monday"
GetDayName(5) -> "Friday"
GetDayName(7) -> "Sunday"
GetDayName(0) -> "Invalid day"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetDayName(int dayNumber)
    {
        // 使用 switch 表达式直接返回结果，_ 匹配其他所有数字
        return dayNumber switch
        {
            1 => "Monday",
            2 => "Tuesday",
            3 => "Wednesday",
            4 => "Thursday",
            5 => "Friday",
            6 => "Saturday",
            7 => "Sunday",
            _ => "Invalid day"
        };
    }
}
```
