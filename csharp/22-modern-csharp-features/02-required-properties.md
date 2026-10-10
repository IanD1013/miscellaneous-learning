### Required 属性

`required` 修饰符（C# 11+）用于标记在对象初始化期间**必须**设置的属性。
编译器会强制执行此规则，防止创建缺少必填数据的对象。

### 基本语法

```csharp
public class User
{
    public required string Username { get; set; }
    public required string Email { get; set; }
    public string? Bio { get; set; }  // 可选 - 没有 required 修饰符
}

// 必须提供 Username 和 Email
var user = new User
{
    Username = "john_doe",
    Email = "john@example.com"
    // Bio 是可选的，可以省略
};
```

### 编译器强制检查

```csharp
// 这将无法编译 - 缺少 required 属性
var user = new User
{
    Username = "john_doe"
    // 错误：Required member 'User.Email' must be set
};
```

### Required 与 Init-Only 的对比

| 特性 | `required` | `init` | 组合使用 |
| --- | --- | --- | --- |
| 创建时必须设置 | ✓ | ✗ | ✓ |
| 创建后不可变 | ✗ | ✓ | ✓ |
| 语法 | `required string Name { get; set; }` | `string Name { get; init; }` | `required string Name { get; init; }` |

```csharp
// 组合使用 required 和 init，实现不可变的必填属性
public class Order
{
    public required string OrderId { get; init; }  // 必须设置，不能更改
    public required decimal Total { get; init; }
}
```

### 你的任务

创建一个包含三个 **required** 属性的 `Product` 类：

- `Name` (string)
- `Price` (decimal)
- `Category` (string)

然后实现 `CreateProduct` 来创建一个 Product 实例并返回其描述。

### 方法签名

```csharp
public static string CreateProduct(string name, decimal price, string category)
```

### 预期结果

```
CreateProduct("Laptop", 999.99m, "Electronics") -> "Product: Laptop, Price: $999.99, Category: Electronics"
CreateProduct("Coffee", 4.50m, "Beverages") -> "Product: Coffee, Price: $4.50, Category: Beverages"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CreateProduct(string name, decimal price, string category)
    {
        // 使用 required 属性创建一个 Product
        var product = new Product
        {
            Name = name,
            Price = price,
            Category = category
        };

        // 按格式返回描述："Product: {Name}, Price: ${Price}, Category: {Category}"
        // 价格格式化为恰好 2 位小数，例如 $4.50、$0.00
        return $"Product: {product.Name}, Price: ${product.Price:F2}, Category: {product.Category}";
    }
}

// 带有 required 属性的 Product 类
public class Product
{
    public required string Name { get; set; }
    public required decimal Price { get; set; }
    public required string Category { get; set; }
}
```
