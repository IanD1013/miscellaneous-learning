### 抽象方法

抽象方法是在抽象类中声明的没有实现的方法，它仅定义了方法签名。
任何继承自该抽象类的非抽象类都**必须**提供具体实现。

### 声明抽象方法

```csharp
public abstract class Animal
{
    // 抽象方法 - 没有方法体，以分号结尾
    public abstract void MakeSound();
    
    // 带返回类型的抽象方法
    public abstract int GetLegs();
}
```

### 实现抽象方法

```csharp
public class Dog : Animal
{
    // 必须使用 'override' 关键字
    public override void MakeSound()
    {
        Console.WriteLine("Woof!");
    }

    public override int GetLegs()
    {
        return 4;
    }
}
```

### 抽象方法与虚方法

| 特性 | 抽象方法 | 虚方法 |
| --- | --- | --- |
| 包含方法体 | 否 | 是（默认实现） |
| 必须重写 | 是 | 否（可选） |
| 使用 `override` | 是 | 是 |
| 仅可存在于 | 抽象类 | 任何类 |

### 为什么使用抽象方法？

抽象方法强制执行一种契约，它们确保所有派生类都会具有特定签名的特定方法。
当你知道应该存在**什么**操作，但每个子类都需要定义**如何**实现它时，这非常有用。

### 你的任务

1. 在 `Shape` 抽象类中，声明一个返回 `double` 的抽象方法 `GetArea()`
2. 在 `Rectangle` 类中，重写并实现 `GetArea()` 以返回面积（width × height）

### 方法签名

```csharp
// 在 Shape 类中：
public abstract double GetArea();

// 在 Rectangle 类中：
public override double GetArea()
```

### 预期结果

```
CalculateArea(5.0, 3.0) -> 15.0
CalculateArea(10.0, 10.0) -> 100.0
```

### 解答

```csharp
using System;

public abstract class Shape
{
    public string Name { get; set; }

    public Shape(string name)
    {
        Name = name;
    }

    // 声明返回 double 的抽象方法 GetArea()
    // 抽象方法没有方法体，只有签名并以分号结尾
    public abstract double GetArea();
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }

    public Rectangle(double width, double height) : base("Rectangle")
    {
        Width = width;
        Height = height;
    }

    // 重写并实现 GetArea() 方法
    // 返回矩形的面积（width * height）
    public override double GetArea()
    {
        return Width * Height;
    }
}

public class Solution
{
    public static double CalculateArea(double width, double height)
    {
        Rectangle rect = new Rectangle(width, height);
        return rect.GetArea();
    }
}
```
