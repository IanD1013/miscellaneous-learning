### C# 中的匿名类型

匿名类型允许您在不预先定义类的情况下创建具有只读属性的对象。
它们非常适合在方法内进行临时数据分组，例如在对几个相关值进行格式化或投影之前将它们组合在一起。

### 创建匿名类型

```csharp
// 使用 new { } 的基本语法
var person = new { Name = "Alice", Age = 30 };

// 属性名称从变量名推断而来
string city = "London";
int population = 9000000;
var cityInfo = new { city, population };  // 属性：city, population

// 混合使用：部分显式指定，部分推断
var item = new { Name = "Widget", price, InStock = true };
```

### 访问属性

```csharp
var book = new { Title = "C# Basics", Pages = 350, Price = 29.99m };

Console.WriteLine(book.Title);   // "C# Basics"
Console.WriteLine(book.Pages);   // 350
Console.WriteLine(book.Price);   // 29.99
```

### 一致地格式化数字

当您通过字符串插值直接打印 `decimal` 时，C# 仅显示其存储的数字。
因此 `10m` 会打印为 `10`，而 `10.50m` 会打印为 `10.50`。
对于货币，您通常希望保留**一致**的小数位数。

在插值内部使用格式说明符来控制这一点：

```csharp
decimal amount = 5m;
Console.WriteLine($"{amount}");      // 5
Console.WriteLine($"{amount:F2}");   // 5.00  （始终保留 2 位小数）

decimal tax = 8.5m;
Console.WriteLine($"{tax:F2}");      // 8.50
```

`:F2` 说明符表示“固定保留恰好 2 位小数”，无论传入什么值。

### 匿名类型的关键特性

- 属性是**只读**的（不可变）
- 类型由编译器生成
- 使用 `var`，因为您无法指定类型名称
- 非常适合 LINQ 投影和临时数据

### 您的任务

创建一个匿名类型来保存产品信息（名称、价格、数量），然后将其格式化为描述字符串。
价格必须**始终**显示恰好两位小数（例如，价格 `10` 变为 `$10.00`，价格 `75.5` 变为 `$75.50`）。

所需格式为：

```
Product: {Name}, Price: ${Price}, Qty: {Quantity}
```

### 方法签名

```csharp
public static string DescribeProduct(string name, decimal price, int quantity)
```

### 预期结果

```
DescribeProduct("Laptop", 999.99m, 5) -> "Product: Laptop, Price: $999.99, Qty: 5"
DescribeProduct("Cable", 10m, 500) -> "Product: Cable, Price: $10.00, Qty: 500"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string DescribeProduct(string name, decimal price, int quantity)
    {
        // 创建一个包含 Name、Price 和 Quantity 属性的匿名类型
        var product = new { Name = name, Price = price, Quantity = quantity };
        
        // 然后使用这些属性返回格式化字符串
        // 价格格式化为恰好 2 位小数，例如 $75.00
        // 示例输出："Product: Laptop, Price: $999.99, Qty: 5"
        return $"Product: {product.Name}, Price: ${product.Price:F2}, Qty: {product.Quantity}";
    }
}
```
