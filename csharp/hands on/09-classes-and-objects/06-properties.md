### 属性与封装

属性是在 C# 中实现**封装**（encapsulation）的核心机制。
封装是面向对象编程的四大支柱之一，它意味着隐藏数据存储方式的内部细节，同时通过公共接口提供受控的访问。

### 为什么封装很重要

如果没有封装，任何人都可以直接以无效的方式修改对象的数据：

```csharp
// 没有封装（危险！）
public class Product
{
    public decimal price;  // 公共字段 - 任何人都可以设置为 -100！
}

Product p = new Product();
p.price = -100;  // 没有保护！允许无效数据。
```

有了封装，你就可以保护你的数据：

```csharp
// 有封装（安全！）
public class Product
{
    private decimal _price;  // 对外部隐藏
    
    public decimal Price     // 受控的访问入口
    {
        get { return _price; }
        set { if (value > 0) _price = value; }  // 验证！
    }
}
```

### 属性的剖析

```csharp
private string _name;  // 后备字段（存储实际数据 - PRIVATE）

public string Name     // 属性（控制访问 - PUBLIC）
{
    get                // 读取属性时调用
    {
        return _name;
    }
    set                // 写入属性时调用
    {
        _name = value; // 'value' 是传入的数据
    }
}
```

后备字段是 `private` 的，不能从类外部直接访问。
属性是 `public` 的，它是访问数据的受控入口。

### 添加验证逻辑

属性允许你在 setter 中添加**验证**或**转换**逻辑：

```csharp
private int _age;
public int Age
{
    get { return _age; }
    set
    {
        if (value >= 0 && value <= 150)  // 验证！
        {
            _age = value;
        }
        // 如果无效，该值会被直接忽略
    }
}
```

### `value` 关键字

在 `set` 访问器内部，`value` 表示正在被赋值的传入数据：

```csharp
person.Age = 25;  // 在 setter 内部 'value' 为 25
```

### 你的任务

创建一个演示封装特性的 `Product` 类：

1. 一个 **private** 后备字段 `_name` 和一个 **public** `Name` 属性
2. 一个 **private** 后备字段 `_price` 和一个 **public** `Price` 属性
3. `Price` 的 setter 应**仅接受正数值**（大于 0），这可以保护对象免受无效数据的影响

### 方法签名

```csharp
public class Product
{
    private string _name;   // 已封装 - 对外部隐藏
    private decimal _price; // 已封装 - 对外部隐藏
    
    public string Name { get { ... } set { ... } }      // 公共访问入口
    public decimal Price { get { ... } set { ... } }    // 带验证
}
```

### 预期结果

```
GetProductInfo("Laptop", 999.99m) -> "Laptop: $999.99"
GetProductInfo("Coffee", -5.00m) -> "Coffee: $0"  // 负价格被封装逻辑拒绝
```

### 解答

```csharp
using System;

public class Product
{
    // 第 1 步：name 的私有后备字段
    private string _name;
    
    // 第 2 步：price 的私有后备字段
    private decimal _price;
    
    // 第 3 步：带 get 和 set 访问器的 Name 属性
    public string Name
    {
        get { return _name; }
        set { _name = value; }
    }
    
    // 第 4 步：带 get 和 set 访问器的 Price 属性
    // 只接受正数值（value <= 0 时保留当前价格）
    public decimal Price
    {
        get { return _price; }
        set
        {
            if (value > 0)
            {
                _price = value;
            }
        }
    }
}

public class Solution
{
    public static string GetProductInfo(string name, decimal price)
    {
        Product product = new Product();
        product.Name = name;
        product.Price = price;
        return $"{product.Name}: ${product.Price}";
    }
}
```
