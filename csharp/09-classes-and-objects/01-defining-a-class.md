### C# 中的类

类是创建对象的蓝图。
它定义了对象所持有的数据以及可以执行的操作。
类是 C# 中面向对象编程的基础。

### 定义类

```csharp
// 最简单的类 - 只有一个名称
public class Car
{
}

// 带有字段（数据）的类
public class Dog
{
    public string Name;
}

// 带有方法（行为）的类
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

### 创建对象（实例化）

一旦定义了类，就可以使用 `new` 关键字从中创建对象：

```csharp
// 创建 Car 的实例
Car myCar = new Car();

// 创建 Dog 的实例
Dog myDog = new Dog();
myDog.Name = "Buddy";

// 创建并使用 Calculator
Calculator calc = new Calculator();
int result = calc.Add(5, 3);  // result = 8
```

### 类与对象

| 概念 | 描述 | 示例 |
| --- | --- | --- |
| 类（Class） | 蓝图/模板 | `class Person { }` |
| 对象（Object） | 从类创建的实例 | `new Person()` |
| 实例化（Instantiation） | 创建对象的操作 | 使用 `new` 关键字 |

### 你的任务

定义一个空的 `Person` 类，然后创建并返回它的一个实例。

### 方法签名

```csharp
public static Person CreatePerson()
```

### 预期结果

```
CreatePerson() -> a Person object (not null)
```

### 解答

```csharp
using System;

// 定义一个空的 Person 类
public class Person
{
}

public class Solution
{
    public static Person CreatePerson()
    {
        // 创建并返回一个新的 Person 实例
        return new Person();
    }
}
```
