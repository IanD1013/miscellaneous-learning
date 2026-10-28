### 带有格式说明符的字符串插值

字符串插值（`$"..."`）允许你直接在字符串中嵌入表达式，并应用格式说明符来控制值的显示方式。

### 基本语法

```csharp
// 格式说明符位于花括号内的冒号之后
string result = "${value:formatSpecifier}";

// 示例
decimal price = 19.99m;
string currency = "${price:C}";  // "$19.99" (因区域性而异)

double rate = 0.15;
string percent = "${rate:P}";    // "15.00%"

int count = 1234567;
string number = "${count:N0}";   // "1,234,567"
```

### 字符串插值 vs String.Format

```csharp
// String.Format（旧的方式）
string old = string.Format("Price: {0:C}", price);

// 字符串插值（现代、更简洁）
string modern = $"Price: {price:C}";

// 两者产生相同的结果，但插值的可读性更好
```

### 常用格式说明符

| 说明符 | 描述 | 示例输入 | 示例输出 |
| --- | --- | --- | --- |
| :C | 货币 | 19.99m | $19.99 |
| :N | 带分隔符的数字 | 1234567 | 1,234,567.00 |
| :N0 | 数字，无小数 | 1234567 | 1,234,567 |
| :P | 百分比 | 0.15 | 15.00% |
| :P0 | 百分比，无小数 | 0.15 | 15% |

### 你的任务

使用带有格式说明符的字符串插值实现三个方法：

1. `FormatAsCurrency` - 使用 `:C` 将 decimal 格式化为货币
2. `FormatAsPercent` - 使用 `:P` 将 double 格式化为百分比
3. `FormatAsNumber` - 使用 `:N0` 将 integer 格式化为带千位分隔符的数字

### 方法签名

```csharp
public static string FormatAsCurrency(decimal amount)
public static string FormatAsPercent(double ratio)
public static string FormatAsNumber(int value)
```

### 预期结果

```
FormatAsCurrency(19.99m) -> "$19.99"
FormatAsPercent(0.25) -> "25.00%"
FormatAsNumber(1000000) -> "1,000,000"
```

注意：测试在美式文化（en-US）下运行，以确保格式化结果一致。

### 解答

```csharp
using System;
using System.Globalization;

public class Solution
{
    public static string FormatAsCurrency(decimal amount)
    {
        // 使用带 :C 格式说明符的字符串插值
        // 返回格式化后的货币字符串
        return $"{amount:C}";
    }
    
    public static string FormatAsPercent(double ratio)
    {
        // 使用带 :P 格式说明符的字符串插值
        // 返回格式化后的百分比字符串
        return $"{ratio:P}";
    }
    
    public static string FormatAsNumber(int value)
    {
        // 使用带 :N0 格式说明符的字符串插值（无小数位）
        // 返回格式化后的数字字符串
        return $"{value:N0}";
    }
}
```
