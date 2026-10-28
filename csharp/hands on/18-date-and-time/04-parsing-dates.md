### 解析日期字符串

`DateTime.Parse` 和 `DateTime.TryParse` 用于将文本转换为 `DateTime` 值。
当你确信输入有效时使用 `Parse`，需要安全解析且不抛出异常时使用 `TryParse`。

### DateTime.Parse

将字符串转换为 `DateTime`，如果字符串无效则抛出 `FormatException`。

```csharp
DateTime date1 = DateTime.Parse("2024-03-15");
DateTime date2 = DateTime.Parse("March 15, 2024");
DateTime date3 = DateTime.Parse("15/03/2024 14:30");
```

### DateTime.TryParse

如果解析成功返回 `true`，否则返回 `false`。
对于无效输入绝不会抛出异常。

```csharp
bool success = DateTime.TryParse("2024-03-15", out DateTime result);
// success = true, result = 2024 年 3 月 15 日

bool failed = DateTime.TryParse("not a date", out DateTime invalid);
// failed = false, invalid = DateTime.MinValue
```

### 丢弃 out 参数

当你只需要检查有效性时，可以使用弃元模式（discard）`out _`：

```csharp
if (DateTime.TryParse(userInput, out _))
{
    Console.WriteLine("Valid date!");
}
```

### 可识别的格式

| 格式 | 示例 |
| --- | --- |
| ISO 8601 | "2024-03-15" |
| 长日期 | "March 15, 2024" |
| 短日期 | "3/15/2024" |
| 带时间 | "2024-03-15 14:30:00" |

### 你的任务

实现三个方法：

1. `IsValidDate(string dateString)` - 如果字符串是有效日期则返回 `true`，否则返回 `false`
2. `ParseDate(string dateString)` - 解析并返回 `DateTime`（保证输入有效）
3. `ParseAndFormat(string dateString, string format)` - 解析日期并返回格式化后的文本，如果解析失败则返回 `"Invalid"`

### 预期结果

```
IsValidDate("2024-03-15") -> true
IsValidDate("not a date") -> false
ParseDate("2024-03-15") -> 3/15/2024 12:00:00 AM
ParseAndFormat("March 15, 2024", "yyyy-MM-dd") -> "2024-03-15"
ParseAndFormat("invalid", "yyyy-MM-dd") -> "Invalid"
```

### 解答

```csharp
using System;
using System.Globalization;

public class Solution
{
    public static bool IsValidDate(string dateString)
    {
        // 检查字符串能否被解析为有效日期
        // 有效则返回 true，否则返回 false
        return DateTime.TryParse(dateString, out _);
    }
    
    public static DateTime ParseDate(string dateString)
    {
        // 解析字符串并返回 DateTime
        // 此方法假定输入总是有效的
        return DateTime.Parse(dateString);
    }
    
    public static string ParseAndFormat(string dateString, string format)
    {
        // 解析日期字符串并返回格式化后的结果
        // 解析失败时返回 "Invalid"
        if (DateTime.TryParse(dateString, out DateTime date))
        {
            return date.ToString(format);
        }
        return "Invalid";
    }
}
```
