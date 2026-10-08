### 只读属性

只读属性使用 `{ get; }` 且不包含 setter，这意味着它们只能在构造函数中被赋值，之后便不能再更改。

### 声明语法

```csharp
public class Product
{
    // 只读属性 - 只能在构造函数中设置
    public string ProductId { get; }
    public decimal Price { get; }
    
    public Product(string id, decimal price)
    {
        ProductId = id;  // ✓ 有效 - 在构造函数中设置
        Price = price;   // ✓ 有效 - 在构造函数中设置
    }
    
    public void UpdatePrice(decimal newPrice)
    {
        // Price = newPrice;  // ✗ 错误！构造之后不能再赋值
    }
}
```

### 只读属性与自动属性

```csharp
// 带 getter 和 setter 的自动属性（可变）
public string Name { get; set; }  // 随时可以更改

// 只读属性（构造之后不可变）
public string Id { get; }
  // 只能在构造函数中设置

// 私有 setter（仅在类内部可变）
public int Count { get; private set; }  // 可以被类的方法更改
```

### 为什么使用只读属性？

| 优势 | 说明 |
| --- | --- |
| 不可变性 | 对象创建后值无法更改 |
| 线程安全 | 不存在并发修改的风险 |
| 可预测性 | 对象状态在整个生命周期中保持一致 |
| 数据完整性 | 防止意外修改关键值 |

### 你的任务

创建一个包含两个只读属性的 `Person` 类：

- `Name` (string) - 姓名
- `BirthYear` (int) - 出生年份

这两个属性都应当只能通过构造函数进行设置。

### 方法签名

```csharp
public class Person
{
    public string Name { get; }
    public int BirthYear { get; }
    public Person(string name, int birthYear)
}
```

### 预期结果

```
GetPersonInfo("Alice", 1990) -> "Alice was born in 1990"
GetPersonInfo("Bob", 2000) -> "Bob was born in 2000"
```

### 解答

```csharp
using System;

public class Person
{
    // string 类型的只读属性 Name
    public string Name { get; }
    // int 类型的只读属性 BirthYear
    public int BirthYear { get; }
    
    // 构造函数接收 name 和 birthYear 参数，并设置只读属性
    public Person(string name, int birthYear)
    {
        Name = name;
        BirthYear = birthYear;
    }
}

public class Solution
{
    public static string GetPersonInfo(string name, int birthYear)
    {
        Person person = new Person(name, birthYear);
        return $"{person.Name} was born in {person.BirthYear}";
    }
}
```
