### 命名元组元素

命名元组元素为元组字段提供了有意义的名称，而不是默认的 `Item1`、`Item2` 等。
这使您的代码更具可读性和自解释性。

### 声明命名元组

```csharp
// 不带名称（难以阅读）
(string, int) person1 = ("Alice", 30);
Console.WriteLine(person1.Item1); // "Alice"

// 带名称（清晰易读）
(string Name, int Age) person2 = ("Bob", 25);
Console.WriteLine(person2.Name); // "Bob"
Console.WriteLine(person2.Age);  // 25
```

### 创建命名元组

```csharp
// 在类型声明中指定名称
(string FirstName, string LastName) fullName = ("John", "Doe");

// 在创建值时指定名称
var employee = (Name: "Sarah", Department: "Engineering", Years: 5);
Console.WriteLine(employee.Department); // "Engineering"

// 从方法返回命名元组
public static (int Width, int Height) GetDimensions()
{
    return (Width: 1920, Height: 1080);
}
```

### 命名访问与未命名访问

| 访问方式 | 示例 | 说明 |
| --- | --- | --- |
| 命名访问 | `person.Name` | 可读性高，自解释 |
| 位置访问 | `person.Item1` | 仍然有效，但不够清晰 |

### 您的任务

实现两个方法：

1. `CreateNamedPersonTuple` - 创建并返回包含 `Name`、`Age` 和 `City` 元素的命名元组
2. `GetPersonDescription` - 使用命名元组构建描述字符串

### 方法签名

```csharp
public static (string Name, int Age, string City) CreateNamedPersonTuple(string name, int age, string city)
public static string GetPersonDescription(string name, int age, string city)
```

### 预期结果

```
GetPersonDescription("Alice", 30, "London") -> "Alice is 30 years old and lives in London"
GetPersonDescription("Bob", 25, "Paris") -> "Bob is 25 years old and lives in Paris"
```

### 解答

```csharp
using System;

public class Solution
{
    public static (string Name, int Age, string City) CreateNamedPersonTuple(string name, int age, string city)
    {
        return (Name: name, Age: age, City: city);
    }
    
    public static string GetPersonDescription(string name, int age, string city)
    {
        // 使用 CreateNamedPersonTuple 并访问命名元素
        var person = CreateNamedPersonTuple(name, age, city);
        return $"{person.Name} is {person.Age} years old and lives in {person.City}";
    }
}
```
