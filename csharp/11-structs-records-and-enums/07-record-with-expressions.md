### 记录的 With 表达式

`with` 表达式用于创建记录（record）的一个**副本**，并更改其中一个或多个属性。
由于记录默认是不可变的（immutable），因此 `with` 是创建修改后版本的惯用方式。

### 基本语法

```csharp
record Person(string Name, int Age);

var alice = new Person("Alice", 30);
var olderAlice = alice with { Age = 31 };  // 新的记录，alice 不变

// alice.Age 仍然是 30
// olderAlice.Age 是 31
```

### 更改多个属性

```csharp
record Address(string Street, string City, string Country);

var home = new Address("123 Main St", "London", "UK");
var newHome = home with { Street = "456 Oak Ave", City = "Manchester" };

// Country 保持为 "UK"，只有 Street 和 City 被更改
```

### 为什么使用 With？

| 方式 | 结果 | 原对象是否被修改？ |
| --- | --- | --- |
| 直接赋值 | 相同对象 | 是（如果可变） |
| `with` 表达式 | 新副本 | 否（不可变） |

这种不可变模式可以防止由于共享状态引起的错误，并使代码更容易推导和理解。

### 你的任务

使用 `with` 表达式实现三个方法：

1. **UpdateAge**：返回具有指定年龄的新 `Person`
2. **ApplyDiscount**：返回具有指定价格的新 `Product`
3. **Promote**：返回更新了职位头衔与薪资的新 `Employee`（将增加的金额加到当前薪资上）

记录类型定义在 Models.cs 中。

### 方法签名

```csharp
public static Person UpdateAge(Person person, int newAge)
public static Product ApplyDiscount(Product product, decimal newPrice)
public static Employee Promote(Employee employee, string newTitle, int salaryIncrease)
```

### 预期结果

```
UpdateAge(Person("Bob", 25), 26) -> Person { Name = Bob, Age = 26 }
ApplyDiscount(Product("Laptop", 999.99m, 10), 799.99m) -> Product { Name = Laptop, Price = 799.99, Stock = 10 }
Promote(Employee("Jane", "Developer", 50000), "Senior Developer", 10000) -> Employee { Name = Jane, Title = Senior Developer, Salary = 60000 }
```

### 解答

```csharp
using System;

public class Solution
{
    public static Person UpdateAge(Person person, int newAge)
    {
        // 使用 with 表达式创建一个更新了年龄的新 Person
        return person with { Age = newAge };
    }
    
    public static Product ApplyDiscount(Product product, decimal newPrice)
    {
        // 使用 with 表达式创建一个更新了价格的新 Product
        return product with { Price = newPrice };
    }
    
    public static Employee Promote(Employee employee, string newTitle, int salaryIncrease)
    {
        // 使用 with 表达式创建一个更新了职位头衔和薪资的新 Employee
        return employee with { Title = newTitle, Salary = employee.Salary + salaryIncrease };
    }
}
```
