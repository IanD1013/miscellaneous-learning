### 使用 ToString 格式化日期

`DateTime.ToString()` 方法接受用于控制日期显示外观的格式字符串。
这对于向用户展示日期或生成标准化输出至关重要。

### 自定义格式说明符

```csharp
DateTime date = new DateTime(2024, 3, 15);

date.ToString("yyyy-MM-dd")    // "2024-03-15"（ISO 格式）
date.ToString("dd/MM/yyyy")    // "15/03/2024"（欧洲风格）
date.ToString("MM/dd/yyyy")    // "03/15/2024"（美国风格）
date.ToString("MMMM dd, yyyy") // "March 15, 2024"（完整月份名称）
```

### 格式说明符参考

| 说明符 | 描述 | 示例 |
| --- | --- | --- |
| `yyyy` | 4 位数年份 | 2024 |
| `yy` | 2 位数年份 | 24 |
| `MM` | 2 位数月份 | 03 |
| `M` | 1 位或 2 位数月份 | 3 |
| `MMMM` | 完整月份名称 | March |
| `MMM` | 缩写月份名称 | Mar |
| `dd` | 2 位数日期 | 15 |
| `d` | 1 位或 2 位数日期 | 15 |

### 标准格式字符串

C# 还提供了单字符快捷方式：

```csharp
date.ToString("d")  // 短日期："3/15/2024"
date.ToString("D")  // 长日期："Friday, March 15, 2024"
date.ToString("f")  // 完整日期/时间："Friday, March 15, 2024 12:00 AM"
```

### 你的任务

实现三个以不同方式格式化 `DateTime` 的方法：

1. **FormatAsIso**：以 ISO 格式 `yyyy-MM-dd` 返回日期
2. **FormatAsLongDate**：以 `MMMM dd, yyyy` 格式返回日期
3. **FormatAsCustom**：以 `dd/MM/yyyy` 格式返回日期

### 方法签名

```csharp
public static string FormatAsIso(DateTime date)
public static string FormatAsLongDate(DateTime date)
public static string FormatAsCustom(DateTime date)
```

### 预期结果

```
FormatAsIso(March 15, 2024) -> "2024-03-15"
FormatAsLongDate(March 15, 2024) -> "March 15, 2024"
FormatAsCustom(March 15, 2024) -> "15/03/2024"
```

### 解答

```csharp
using System;

public class Solution
{
    // 格式化为 ISO 日期：yyyy-MM-dd（例如 "2024-03-15"）
    public static string FormatAsIso(DateTime date)
    {
        return date.ToString("yyyy-MM-dd");
    }
    
    // 格式化为长日期：MMMM dd, yyyy（例如 "March 15, 2024"）
    public static string FormatAsLongDate(DateTime date)
    {
        return date.ToString("MMMM dd, yyyy");
    }
    
    // 格式化为：dd/MM/yyyy（例如 "15/03/2024"）
    public static string FormatAsCustom(DateTime date)
    {
        return date.ToString("dd/MM/yyyy");
    }
}
```
