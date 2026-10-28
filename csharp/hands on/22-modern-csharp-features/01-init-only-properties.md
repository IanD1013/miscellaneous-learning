### Init-Only 属性

Init-only（仅初始化）属性允许您仅在对象初始化期间设置属性值。
对象创建完成后，该属性将变为只读。

### 基本语法

```csharp
public class Product
{
    public string Name { get; init; }  // 只能在初始化期间设置
    public decimal Price { get; init; }
}

// 用法 - 在初始化期间设置值
var product = new Product
{
    Name = "Laptop",
    Price = 999.99m
};

// 这会导致编译错误：
// product.Name = "Desktop";  // 错误！初始化后无法赋值
```

### Init 与 Set 的对比

```csharp
public class Comparison
{
    public string Mutable { get; set; }   // 可以随时更改
    public string Immutable { get; init; } // 只能在初始化期间设置
}

var obj = new Comparison { Mutable = "A", Immutable = "B" };
obj.Mutable = "Changed";    // 正常工作
// obj.Immutable = "Changed"; // 编译错误！
```

### 为什么使用 Init-Only？

| 优势 | 说明 |
| --- | --- |
| 不可变性 (Immutability) | 防止在创建后被意外修改 |
| 线程安全 (Thread Safety) | 不可变对象在并发代码中更安全 |
| 意图明确 (Clear Intent) | 表明这些值不应被更改 |
| 支持对象初始化器 | 与只读字段不同，它支持与对象初始化器配合使用 |

### 你的任务

创建一个包含三个 init-only 属性的 `Person` 类：

- `Name` (string)
- `Age` (int)
- `City` (string)

然后实现 `CreateAndDescribePerson` 方法以创建一个 Person 并返回格式化后的描述。

### 方法签名

```csharp
public static string CreateAndDescribePerson(string name, int age, string city)
```

### 预期结果

```
CreateAndDescribePerson("Alice", 30, "London") -> "Name: Alice, Age: 30, City: London"
CreateAndDescribePerson("Bob", 25, "Paris") -> "Name: Bob, Age: 25, City: Paris"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CreateAndDescribePerson(string name, int age, string city)
    {
        // 使用 init-only 属性创建一个 Person
        var person = new Person
        {
            Name = name,
            Age = age,
            City = city
        };

        // 按格式返回描述："Name: {name}, Age: {age}, City: {city}"
        return $"Name: {person.Name}, Age: {person.Age}, City: {person.City}";
    }
}

// 带有 init-only 属性的 Person 类
public class Person
{
    public string Name { get; init; }
    public int Age { get; init; }
    public string City { get; init; }
}
```
