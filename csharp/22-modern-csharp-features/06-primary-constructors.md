### 主构造函数

主构造函数（primary constructor，C# 12+）允许您直接在类声明中声明构造函数参数，从而消除简单类的样板代码。

### 传统构造函数 vs 主构造函数

```csharp
// 传统方式 - 冗长
public class Person
{
    private string _name;
    
    public Person(string name)
    {
        _name = name;
    }
    
    public string Name => _name;
}

// 主构造函数 - 简洁
public class Person(string name)
{
    public string Name => name;
}
```

### 使用主构造函数参数

```csharp
// 参数在整个类中都可用
public class Rectangle(double width, double height)
{
    public double Width => width;
    public double Height => height;
    public double Area => width * height;
    
    public string Describe() => $"{width} x {height}";
}
```

### 关键要点

| 方面 | 描述 |
| --- | --- |
| 语法 | `class Name(params)` |
| 作用域 | 参数在整个类主体中可用 |
| 捕获 | 参数被捕获，而不是存储为字段 |
| 属性 | 如有需要，必须显式创建属性 |

### 您的任务

将 `Employee` 类转换为使用主构造函数。
该类应满足：

1. 将 `name`、`department` 和 `yearsOfService` 作为主构造函数参数
2. 将它们公开为只读属性
3. 保持 `GetDescription()` 方法正常工作

### 方法签名

```csharp
public static string DescribeEmployee(string name, string department, int yearsOfService)
```

### 预期结果

```
DescribeEmployee("Alice", "Engineering", 5) -> "Alice works in Engineering for 5 years"
DescribeEmployee("Bob", "Marketing", 10) -> "Bob works in Marketing for 10 years"
```

### 解答

```csharp
using System;

// 使用主构造函数的 Employee 类
// name、department 和 yearsOfService 是主构造函数参数
public class Employee(string name, string department, int yearsOfService)
{
    // 将参数公开为只读属性
    public string Name => name;
    public string Department => department;
    public int YearsOfService => yearsOfService;

    public string GetDescription()
    {
        return $"{name} works in {department} for {yearsOfService} years";
    }
}

public class Solution
{
    public static string DescribeEmployee(string name, string department, int yearsOfService)
    {
        var employee = new Employee(name, department, yearsOfService);
        return employee.GetDescription();
    }
}
```
