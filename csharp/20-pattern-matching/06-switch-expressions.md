### Switch 表达式

Switch 表达式为 switch 语句提供了一种更简洁的语法，适用于需要根据条件返回值的场景。
它们使用 `=>`（表达式主体）语法，非常适合用于将输入映射到输出。

### 基本语法

```csharp
// 传统的 switch 语句
switch (value)
{
    case 1:
        return "One";
    case 2:
        return "Two";
    default:
        return "Other";
}

// 等价的 switch 表达式
return value switch
{
    1 => "One",
    2 => "Two",
    _ => "Other"
};
```

### 与 Switch 语句的主要区别

| 特性 | Switch 语句 | Switch 表达式 |
| --- | --- | --- |
| 关键字位置 | `switch (value)` | `value switch` |
| Case 语法 | `case 1:` | `1 =>` |
| 默认分支 | `default:` | `_`（弃元） |
| 分隔符 | 带有 `break`/`return` 的语句 | 分支之间用逗号分隔 |
| 返回方式 | 多个 return 语句 | 单个表达式结果 |

### 每个分支匹配多个值

```csharp
var result = grade switch
{
    'A' or 'B' => "Pass with distinction",
    'C' or 'D' => "Pass",
    'F' => "Fail",
    _ => "Invalid grade"
};
```

### 你的任务

将所提供的 switch 语句转换为 switch 表达式。
该方法接收一个天数编号 (1-7)，并应返回该天的描述。
在每个分支中使用 `=>` 语法，并使用弃元模式 `_` 处理无效输入。

### 方法签名

```csharp
public static string GetDayType(int dayNumber)
```

### 预期结果

```
GetDayType(1) -> "Monday - Start of work week"
GetDayType(5) -> "Friday - End of work week"
GetDayType(6) -> "Saturday - Weekend"
GetDayType(0) -> "Invalid day"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetDayType(int dayNumber)
    {
        // 使用 => 语法将 switch 语句转换为 switch 表达式
        return dayNumber switch
        {
            1 => "Monday - Start of work week",
            2 => "Tuesday - Early week",
            3 => "Wednesday - Midweek",
            4 => "Thursday - Late week",
            5 => "Friday - End of work week",
            6 => "Saturday - Weekend",
            7 => "Sunday - Weekend",
            _ => "Invalid day"
        };
    }
}
```
