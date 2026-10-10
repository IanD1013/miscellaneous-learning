### JSON 反序列化

`JsonSerializer.Deserialize` 将 JSON 字符串转换回 C# 对象。
这是序列化的逆过程，获取以 JSON 文本形式存储的数据，并将其重建为可在代码中使用的类型化对象。

### 基本用法

```csharp
using System.Text.Json;

// 将 JSON 字符串反序列化为对象
string json = "{\"Name\":\"Apple\",\"Price\":1.50}";
Product product = JsonSerializer.Deserialize<Product>(json);

// 现在可以访问属性
Console.WriteLine(product.Name);  // Apple
Console.WriteLine(product.Price); // 1.50
```

### 序列化与反序列化

| 操作 | 输入 | 输出 | 方法 |
| --- | --- | --- | --- |
| 序列化 | C# 对象 | JSON 字符串 | `JsonSerializer.Serialize(obj)` |
| 反序列化 | JSON 字符串 | C# 对象 | `JsonSerializer.Deserialize<T>(json)` |

### 属性匹配

默认情况下，JSON 属性名称必须与 C# 属性名称匹配（区分大小写）。
JSON `{"Name":"Test"}` 映射到 C# 属性 `Name`。

```csharp
// 这段 JSON:
// {"Name":"Laptop","Price":999.99,"Quantity":5}

// 映射到这个类:
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Quantity { get; set; }
}
```

### 你的任务

将表示产品的 JSON 字符串解析为 `Product` 对象并将其返回。
`Product` 类已在 `Product.cs` 中定义，具有 `Name`、`Price` 和 `Quantity` 属性。

### 方法签名

```csharp
public static Product DeserializeProduct(string json)
```

### 预期结果

```swift
DeserializeProduct("{\"Name\":\"Apple\",\"Price\":1.50,\"Quantity\":10}") -> Product with Name="Apple", Price=1.50, Quantity=10
DeserializeProduct("{\"Name\":\"Laptop\",\"Price\":999.99,\"Quantity\":1}") -> Product with Name="Laptop", Price=999.99, Quantity=1
```

### 解答

```csharp
using System;
using System.Text.Json;

public class Solution
{
    public static Product DeserializeProduct(string json)
    {
        // 将 JSON 字符串解析为 Product 对象
        return JsonSerializer.Deserialize<Product>(json);
    }
}
```
