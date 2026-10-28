### 继承基础

继承允许一个类继承另一个类的属性和方法，从而促进代码重用，并在类型之间建立“is-a”（是一个）关系。

### `:` 语法

```csharp
// 基类（父类）
public class Vehicle
{ 
    public string Brand { get; set; }
    
    public Vehicle(string brand)
    {
        Brand = brand;
    }
    
    public string Honk()
    {
        return "Beep!";
    }
}

// 派生类（子类） - 继承自 Vehicle
public class Car : Vehicle
{
    public int Doors { get; set; }
    
    // 使用 : base() 调用基类构造函数
    public Car(string brand, int doors) : base(brand)
    {
        Doors = doors;
    }
}
```

### 会被继承的内容

- 所有 public 和 protected 成员（属性、方法、字段）
- 派生类可以直接访问继承的成员
- 构造函数**不会**被继承，你必须显式调用基类的构造函数

```csharp
Car myCar = new Car("Toyota", 4);
string brand = myCar.Brand;    // 继承的属性
string sound = myCar.Honk();   // 继承的方法
```

### 调用基类构造函数

```csharp
public class Dog : Animal
{
    // 使用 : base(args) 将值传递给父类构造函数
    public Dog(string name, int age) : base(name, age)
    {
        // 在这里进行 Dog 特有的额外初始化
    }
}
```

### 你的任务

创建一个继承自 `Animal` 基类的 `Dog` 类：

1. 使用 `: Animal` 语法声明继承
2. 创建一个接收 `name` 和 `age` 的构造函数，并使用 `: base(name, age)` 将它们传递给基类
3. 添加一个 `Speak()` 方法，返回 `"Woof! My name is {Name}"`

### 方法签名

```csharp
public class Dog : Animal
```

### 预期结果

```
MakeDogSpeak("Buddy", 3) -> "Woof! My name is Buddy"
GetDogInfo("Max", 5) -> "Max is 5 years old"
```

### 解答

```csharp
using System;

public class Animal
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public Animal(string name, int age)
    {
        Name = name;
        Age = age;
    }
    
    public string Speak()
    {
        return "Some sound";
    }
    
    public string GetInfo()
    {
        return $"{Name} is {Age} years old";
    }
}

// Dog 类继承自 Animal：
// 1. 使用 : 语法继承 Animal
// 2. 构造函数接收 name 和 age，并传递给基类
// 3. 新的 Speak() 方法返回 "Woof! My name is {Name}"
public class Dog : Animal
{
    // 使用 : base(name, age) 调用基类构造函数
    public Dog(string name, int age) : base(name, age)
    {
    }
    
    // 使用 new 隐藏基类的 Speak() 方法
    public new string Speak()
    {
        return $"Woof! My name is {Name}";
    }
}

public class Solution
{
    public static string MakeDogSpeak(string name, int age)
    {
        Dog dog = new Dog(name, age);
        return dog.Speak();
    }
    
    public static string GetDogInfo(string name, int age)
    {
        Dog dog = new Dog(name, age);
        return dog.GetInfo();
    }
}
```
