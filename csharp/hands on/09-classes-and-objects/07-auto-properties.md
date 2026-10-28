### 自动属性（Auto-Properties）

自动属性提供了一种简洁的方式来声明属性，而无需显式定义支持字段（backing fields）。
编译器会自动为你创建一个隐藏的支持字段。

### 基本语法

```csharp
// 使用支持字段的传统方式
private string _name;
public string Name
{
    get { return _name; }
    set { _name = value; }
}

// 自动属性 - 行为相同，代码少得多
public string Name { get; set; }
```

### 字段与自动属性对比

| 方面 | 字段 | 自动属性 |
| --- | --- | --- |
| 语法 | `public string Name;` | `public string Name { get; set; }` |
| 封装 | 直接暴露 | 使用 getter/setter |
| 后续变更 | 添加逻辑属于破坏性变更 | 之后可以添加逻辑 |

### 不同的访问级别

```csharp
// 可读写属性
public string Name { get; set; }

// 外部只读，内部可设置
public int Age { get; private set; }

// 只读（必须在构造函数中设置）
public string Id { get; }
```

### 你的任务

重构 `Person` 类，使用自动属性替代手动的支持字段以及 getter/setter 方法。

1. 使用自动属性替换私有字段（`_name`、`_age`、`_email`）
2. 移除手动的 getter/setter 方法（`GetName`、`SetName` 等）
3. 更新构造函数以使用新的属性名称

`Solution.GetPersonInfo` 已经直接访问了这些属性（`person.Name`），因此在这些属性存在之前它将无法编译。
让代码能够成功编译正是本练习的目的。

### 属性名称

- `Name` (string)
- `Age` (int)
- `Email` (string)

### 预期结果

```
GetPersonInfo("Alice", 30) -> "Alice, 30, test@example.com"
GetPersonInfo("Bob", 25) -> "Bob, 25, test@example.com"
```

### 解答

```csharp
using System;

public class Person
{
    // 使用自动属性替代私有字段
    public string Name { get; set; }
    public int Age { get; set; }
    public string Email { get; set; }
    
    public Person(string name, int age, string email)
    {
        Name = name;
        Age = age;
        Email = email;
    }
}

public class Solution
{
    public static string GetPersonInfo(string name, int age)
    {
        var person = new Person(name, age, "test@example.com");
        return $"{person.Name}, {person.Age}, {person.Email}";
    }
}
```
