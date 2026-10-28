### JSON 序列化

JSON（JavaScript Object Notation）是一种用于存储和交换数据的轻量级数据格式。
`JsonSerializer.Serialize` 可以将 C# 对象转换为 JSON 字符串。

### 使用 System.Text.Json

```csharp
using System.Text.Json;

// 将对象序列化为 JSON 字符串
Person person = new Person { Name = "Alice", Age = 30 };
string json = JsonSerializer.Serialize(person);
// 结果: {"Name":"Alice","Age":30}
```

### 为什么序列化为 JSON？

| 使用场景 | 描述 |
| --- | --- |
| 保存到文件 | 以可读格式存储对象数据 |
| 通过网络发送 | API 通常使用 JSON 进行数据交换 |
| 配置文件 | 将应用程序设置存储在 JSON 文件中 |
| 日志记录 | 记录结构化数据以便进行分析 |

### 属性命名

默认情况下，`JsonSerializer` 会使用类中完全相同的属性名称：

```csharp
public class Item { public string ItemName { get; set; } }
// 序列化为: {"ItemName":"Widget"}
```

### 你的任务

使用提供的参数创建一个 `Product` 对象，并使用 `JsonSerializer.Serialize` 将其序列化为 JSON 字符串。

`Product` 类在 `Product.cs` 中定义，具有以下属性：`Name`、`Price` 和 `Quantity`。

### 方法签名

```csharp
public static string SerializeProduct(string name, decimal price, int quantity)
```

### 预期结果

```rust
SerializeProduct("Apple", 1.50, 10) -> {"Name":"Apple","Price":1.50,"Quantity":10}
SerializeProduct("Laptop", 999.99, 5) -> {"Name":"Laptop","Price":999.99,"Quantity":5}
```

### 解答

```csharp
using System;
using System.Text.Json;

public class Solution
{
    public static string SerializeProduct(string name, decimal price, int quantity)
    {
        // 用参数创建 Product 对象
        // price + 0.00m 让 decimal 至少保留 2 位小数，所以 1.5 序列化为 1.50，25 序列化为 25.00
        Product product = new Product { Name = name, Price = price + 0.00m, Quantity = quantity };

        // 将对象序列化为 JSON 字符串
        return JsonSerializer.Serialize(product);
    }
}
```
