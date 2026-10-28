### Convert 类

`Convert` 类提供了在不同数据类型之间进行安全转换的方法。
与类型转换（casting）不同，`Convert` 方法可以处理 null 值并执行正确的舍入。

### 常用的 Convert 方法

```csharp
// 字符串转数字
int num = Convert.ToInt32("42");       // 返回 42
double d = Convert.ToDouble("3.14");   // 返回 3.14

// 数字转字符串
string s = Convert.ToString(123);       // 返回 "123"

// double 转 int（舍入到最接近的值）
int rounded = Convert.ToInt32(3.7);     // 返回 4（向上舍入）
int rounded2 = Convert.ToInt32(3.4);    // 返回 3（向下舍入）

// 布尔值转换
string boolStr = Convert.ToString(true); // 返回 "True"
int boolInt = Convert.ToInt32(true);     // 返回 1
```

### Convert 与 Casting 对比

| 操作 | Casting | Convert |
| --- | --- | --- |
| `(int)3.7` | 截断为 3 | `Convert.ToInt32(3.7)` 舍入为 4 |
| `(int)null` | 报错 | `Convert.ToInt32(null)` 返回 0 |
| 字符串转 int | 不可行 | `Convert.ToInt32("42")` 可行 |

### 你的任务

实现一个方法以完成以下操作：

1. 使用 `Convert.ToInt32` 将字符串转换为整数
2. 使用 `Convert.ToInt32` 将 double 转换为整数
3. 使用 `Convert.ToString` 将布尔值转换为字符串
4. 以 `"sum:boolString"` 的格式返回两个整数之和与布尔字符串

### 方法签名

```csharp
public static string ConvertValues(string numberString, double decimalValue, bool boolValue)
```

### 预期结果

```
ConvertValues("10", 5.7, true) -> "16:True"
ConvertValues("3", 2.4, false) -> "5:False"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ConvertValues(string numberString, double decimalValue, bool boolValue)
    {
        // 使用 Convert.ToInt32 将字符串转换为整数
        int fromString = Convert.ToInt32(numberString);
        // 使用 Convert.ToInt32 将 double 转换为整数（舍入到最接近的值，.5 时舍入到偶数）
        int fromDouble = Convert.ToInt32(decimalValue);
        // 使用 Convert.ToString 将布尔值转换为字符串
        string boolString = Convert.ToString(boolValue);
        // 返回格式："sum:boolString"
        return $"{fromString + fromDouble}:{boolString}";
    }
}
```
