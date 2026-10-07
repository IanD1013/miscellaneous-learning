### Decimal

`decimal` 类型是一种 128 位的精确十进制数字，非常适合要求精度的金融计算。
与 `double` 不同，decimal 可以避免浮点舍入误差。

### 何时使用 Decimal 与 Double

```csharp
// Double：科学计算、图形等允许微小误差的场景
double distance = 3.14159265358979;

// Decimal：金钱、财务数据等精度至关重要的场景
decimal price = 19.99m;  // 注意 'm' 后缀！
decimal taxAmount = 1.60m;
```

### 'm' 后缀

Decimal 需要 `m` 或 `M` 后缀以区别于 double：

```csharp
decimal cost = 29.99m;      // 正确
decimal rate = 0.075M;      // 同样正确
// decimal wrong = 29.99;   // 错误！编译器会把它视为 double
```

### 用于算术运算的 Decimal 方法

`decimal` 类型提供了在不使用运算符的情况下执行算术运算的静态方法：

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| decimal.Add(a, b) | 将两个 decimal 相加 | decimal.Add(10.50m, 3.25m) = 13.75 |
| decimal.Subtract(a, b) | 从 a 中减去 b | decimal.Subtract(10.50m, 3.25m) = 7.25 |
| decimal.Multiply(a, b) | 将两个 decimal 相乘 | decimal.Multiply(10.00m, 2m) = 20.00 |
| decimal.Divide(a, b) | 将 a 除以 b | decimal.Divide(10.00m, 4m) = 2.50 |

### 使用 Decimal 方法

```csharp
decimal itemPrice = 15.99m;
decimal shippingCost = 4.50m;

// 将两个价格相加
decimal total = decimal.Add(itemPrice, shippingCost);  // 20.49

// 组合多个商品
decimal item1 = 9.99m;
decimal item2 = 14.50m;
decimal item3 = 3.25m;
decimal subtotal = decimal.Add(decimal.Add(item1, item2), item3);  // 27.74
```

### 你的任务

`AddPrices` 方法已经声明，并且两个价格会作为 `price1` 和 `price2` 传递给你，每次测试时它们的值都会有所不同。
你无需自行定义它们，也不用调用该方法。
请补全方法体：使用 `decimal.Add()` 将这两个价格相加并返回总和。

### 方法签名

```csharp
public static decimal AddPrices(decimal price1, decimal price2)
```

### 预期结果

```
AddPrices(10.00m, 5.99m) -> 15.99
AddPrices(19.99m, 0.01m) -> 20.00
AddPrices(0.00m, 7.50m) -> 7.50
```

### 解答

```csharp
using System;

public class Solution
{
    public static decimal AddPrices(decimal price1, decimal price2)
    {
        // 使用 decimal.Add() 将两个价格相加并返回总和
        return decimal.Add(price1, price2);
    }
}
```
