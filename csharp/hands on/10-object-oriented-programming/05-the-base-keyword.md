### base 关键字

`base` 关键字允许派生类访问其基类的成员，包括构造函数和方法。
这对于继承体系中的正确初始化和代码重用至关重要。

### 调用基类构造函数

```csharp
public class Animal
{
    public string Name { get; set; }
    
    public Animal(string name)
    {
        Name = name;
    }
}

public class Dog : Animal
{
    public string Breed { get; set; }
    
    // 使用 : base(name) 调用父类构造函数
    public Dog(string name, string breed) : base(name)
    {
        Breed = breed;
    }
}
```

### 调用基类方法

```csharp
public class Vehicle
{
    public virtual string GetDescription()
    {
        return "This is a vehicle";
    }
}

public class Car : Vehicle
{
    public override string GetDescription()
    {
        // 调用基类方法并对其进行扩展
        return base.GetDescription() + " with four wheels";
    }
}
```

### 为什么使用 base？

| 场景 | 目的 |
| --- | --- |
| 构造函数中的 `base(args)` | 初始化基类属性 |
| `base.MethodName()` | 在重写中重用基类逻辑 |
| 避免代码重复 | 不重复编写初始化逻辑 |

### 你的任务

完成继承自 `Person` 的 `Employee` 类：

1. 实现构造函数，使用 `: base(name)` 并传入 name 参数来调用基类构造函数
2. 重写 `GetInfo()` 以调用 `base.GetInfo()` 并附加部门信息

### 方法签名

```csharp
public Employee(string name, string department) : base(name)
public override string GetInfo()
```

### 预期结果

```
CreateEmployee("Alice", "Engineering") -> "Name: Alice, Department: Engineering"
CreateEmployee("Bob", "Sales") -> "Name: Bob, Department: Sales"
```

### 解答

```csharp
using System;

public class Person
{
    public string Name { get; protected set; }
    
    public Person(string name)
    {
        Name = name;
    }
    
    public virtual string GetInfo()
    {
        return $"Name: {Name}";
    }
}

public class Employee : Person
{
    public string Department { get; private set; }
    
    // 使用 base 关键字以 name 调用 Person 构造函数
    // 然后设置 Department 属性
    public Employee(string name, string department) : base(name)
    {
        Department = department;
    }
    
    // 重写 GetInfo，使用 base 调用基类的 GetInfo 方法
    // 然后附加部门信息
    public override string GetInfo()
    {
        return base.GetInfo() + $", Department: {Department}";
    }
}

public class Solution
{
    public static string CreateEmployee(string name, string department)
    {
        Employee emp = new Employee(name, department);
        return emp.GetInfo();
    }
}
```
