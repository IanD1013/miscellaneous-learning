### 格式说明符

格式说明符允许你控制值如何显示为字符串。
它们位于字符串插值或 `string.Format()` 中的冒号之后。

### 货币格式 (:C)

```csharp
decimal price = 1234.50m;
string currency = string.Format("{0:C}", price);  // "¤1,234.50" (InvariantCulture)
string interpolated = $"{price:C}";               // 使用插值得到相同的结果
```

`:C` 说明符会添加货币符号和千位分隔符。

### 数字格式 (:N)

```csharp
double bigNumber = 1234567.89;
string formatted = string.Format("{0:N}", bigNumber);  // "1,234,567.89"
string withDecimals = string.Format("{0:N3}", bigNumber); // "1,234,567.890" (3 位小数)
```

`:N` 说明符会添加千位分隔符，并默认保留 2 位小数。

### 百分比格式 (:P)

```csharp
double ratio = 0.1234;
string percent = string.Format("{0:P}", ratio);  // "12.34 %"
string noDecimals = string.Format("{0:P0}", ratio); // "12 %"
```

`:P` 说明符会将值乘以 100 并添加百分比符号。

### 使用 CultureInfo

```csharp
using System.Globalization;

// 为了在不同系统上获得一致的输出：
string.Format(CultureInfo.InvariantCulture, "{0:C}", 99.99m); // "¤99.99"
```

### 你的任务

实现三个使用特定格式说明符对值进行格式化的方法：

1. `FormatAsCurrency` - 使用 `:C` 将 decimal 格式化为货币
2. `FormatAsNumber` - 使用 `:N` 将 double 格式化为带有千位分隔符的数字
3. `FormatAsPercent` - 使用 `:P` 将比率格式化为百分比

使用 `CultureInfo.InvariantCulture` 来确保输出一致。

### 方法签名

```csharp
public static string FormatAsCurrency(decimal amount)
public static string FormatAsNumber(double value)
public static string FormatAsPercent(double ratio)
```

### 预期结果

```
FormatAsCurrency(1234.56m) -> "¤1,234.56"
FormatAsNumber(1234567.89) -> "1,234,567.89"
FormatAsPercent(0.25) -> "25.00 %"
```

### 解答

```csharp
using System;
using System.Globalization;

public class Solution
{
    public static string FormatAsCurrency(decimal amount)
    {
        // 使用 :C 说明符将金额格式化为货币
        // 使用 CultureInfo.InvariantCulture 确保输出一致
        return string.Format(CultureInfo.InvariantCulture, "{0:C}", amount);
    }
    
    public static string FormatAsNumber(double value)
    {
        // 使用 :N 说明符将值格式化为带千位分隔符的数字
        // 使用 CultureInfo.InvariantCulture 确保输出一致
        return string.Format(CultureInfo.InvariantCulture, "{0:N}", value);
    }
    
    public static string FormatAsPercent(double ratio)
    {
        // 使用 :P 说明符将比率格式化为百分比
        // 使用 CultureInfo.InvariantCulture 确保输出一致
        return string.Format(CultureInfo.InvariantCulture, "{0:P}", ratio);
    }
}
```
