### 构造函数重载

构造函数重载允许一个类拥有多个具有不同参数列表的构造函数，从而在创建对象时提供灵活性。

### 为什么要重载构造函数？

不同的情况需要不同的初始化选项：

```csharp
// 有时你只知道名字
Person guest = new Person("Anonymous");

// 有时你拥有全部详细信息
Person member = new Person("Alice", 25);
```

### 重载的工作原理

C# 根据构造函数的**签名**（参数的数量和类型）来区分它们：

```csharp
public class Product
{
    public string Name;
    public decimal Price;
    
    // 带一个参数的构造函数
    public Product(string name)
    {
        Name = name;
        Price = 0.00m;  // 默认值
    }
    
    // 带两个参数的构造函数
    public Product(string name, decimal price)
    {
        Name = name;
        Price = price;
    }
}
```

### 选择正确的构造函数

编译器会根据你提供的参数来选择对应的构造函数：

```csharp
Product p1 = new Product("Widget");           // 使用第一个构造函数
Product p2 = new Product("Gadget", 19.99m);   // 使用第二个构造函数
```

### 你的任务

创建一个包含两个重载构造函数的 `Person` 类：

1. 一个仅接受 `name` 参数并将 `Age` 设置为 0 的构造函数
2. 一个同时接受 `name` 和 `age` 参数的构造函数

### 方法签名

```csharp
public Person(string name)
public Person(string name, int age)
```

### 预期结果

```
CreatePerson("Alice") -> "Alice is 0 years old"
CreatePersonWithAge("Bob", 30) -> "Bob is 30 years old"
```

### 解答

```csharp
using System;

public class Person
{
    public string Name;
    public int Age;
    
    // 只接收 name 参数的构造函数，Age 默认为 0
    public Person(string name)
    {
        Name = name;
        Age = 0;
    }
    
    // 同时接收 name 和 age 参数的构造函数
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
    
    public string GetInfo()
    {
        return $"{Name} is {Age} years old";
    }
}

public class Solution
{
    public static string CreatePerson(string name)
    {
        Person person = new Person(name);
        return person.GetInfo();
    }
    
    public static string CreatePersonWithAge(string name, int age)
    {
        Person person = new Person(name, age);
        return person.GetInfo();
    }
}
```
