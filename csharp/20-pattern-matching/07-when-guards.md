### When 守卫（When Guards）

When 守卫使用 `when` 关键字为模式匹配添加额外条件。
它们允许你在仅检查类型的基础上做进一步细化，在将模式判定为匹配之前检查附加条件。

### 基本语法

```csharp
object value = 42;
string result = value switch
{
    int n when n > 0 => "Positive",
    int n when n < 0 => "Negative",
    int => "Zero",
    _ => "Not an integer"
};
```

### 多个条件

```csharp
// 可以在 when 守卫中使用 && 和 ||
string category = person switch
{
    Person p when p.Age >= 18 && p.HasLicense => "Can drive",
    Person p when p.Age >= 18 => "Adult without license",
    Person => "Minor",
    _ => "Unknown"
};
```

### 顺序至关重要

模式是自上而下进行评估的。
更具体的模式（带有 when 守卫）应该放在更通用的模式之前：

```csharp
// 正确的顺序 - 具体的在前
int x when x > 100 => "Large",
int x when x > 0 => "Positive",
int => "Zero or negative"
```

### 常见的守卫条件

| 条件 | 示例 |
| --- | --- |
| 范围检查 | `when n >= 1 && n <= 10` |
| Null 检查 | `when s != null` |
| 字符串检查 | `when string.IsNullOrEmpty(s)` |
| 属性检查 | `when p.Age >= 18` |

### 你的任务

实现一个方法，使用带有 when 守卫的类型模式对值进行分类：

- 负整数 → "Negative integer"
- 零 → "Zero"
- 1-10 之间的正整数 → "Small positive integer"
- 大于 10 的正整数 → "Large positive integer"
- 负 double 浮点数 → "Negative decimal"
- 非负 double 浮点数 → "Non-negative decimal"
- 空或 null 字符串 → "Empty string"
- 非空字符串 → "Non-empty string"
- Null → "Null value"
- 其他任何值 → "Unknown type"

### 方法签名

```csharp
public static string ClassifyNumber(object value)
```

### 预期结果

```
ClassifyNumber(-5) -> "Negative integer"
ClassifyNumber(0) -> "Zero"
ClassifyNumber(7) -> "Small positive integer"
ClassifyNumber(100) -> "Large positive integer"
ClassifyNumber(-3.14) -> "Negative decimal"
ClassifyNumber("") -> "Empty string"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ClassifyNumber(object value)
    {
        // 使用带 when 守卫的类型模式，更具体的模式放在前面
        return value switch
        {
            int n when n < 0 => "Negative integer",
            int n when n == 0 => "Zero",
            int n when n <= 10 => "Small positive integer",
            int => "Large positive integer",
            double d when d < 0 => "Negative decimal",
            double => "Non-negative decimal",
            string s when string.IsNullOrEmpty(s) => "Empty string",
            string => "Non-empty string",
            null => "Null value",
            _ => "Unknown type"
        };
    }
}
```
