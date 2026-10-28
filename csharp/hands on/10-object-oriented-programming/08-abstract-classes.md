### 抽象类

抽象类是一种不能被直接实例化的类，它可以包含派生类必须实现的抽象成员。
当你想要为相关类定义通用接口和共享行为时，请使用抽象类。

### 声明抽象类和方法

```csharp
// 抽象类 - 不能使用 'new' 创建实例
public abstract class Animal
{
    // 抽象方法 - 没有实现，必须被重写
    public abstract void MakeSound();
    
    // 普通方法 - 可以有实现
    public void Sleep()
    {
        Console.WriteLine("Sleeping...");
    }
}

// 派生类必须实现所有抽象方法
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Woof!");
    }
}
```

### 抽象方法与虚方法对比

| 方面 | Abstract | Virtual |
| --- | --- | --- |
| 包含方法体 | 否 | 是 |
| 必须重写 | 是 | 否 |
| 仅限抽象类 | 是 | 否 |

```csharp
public abstract class Vehicle
{
    // 必须被重写 - 没有默认行为
    public abstract void StartEngine();
    
    // 可以被重写 - 有默认行为
    public virtual void Honk()
    {
        Console.WriteLine("Beep!");
    }
}
```

### 为什么使用抽象类？

- **强制契约**：派生类必须实现特定的方法
- **防止不完整的使用**：避免意外创建没有尺寸的“基础”形状对象
- **共享通用代码**：非抽象方法可以正常被继承

### 你的任务

创建一个包含两个抽象方法的抽象类 `Shape`，然后实现两个具体的形状类：

1. **Shape**（抽象类）：

   - `public abstract double CalculateArea()`
   - `public abstract double CalculatePerimeter()`
2. **Circle**（继承自 Shape）：

   - 构造函数接收 `radius`（double）
   - 面积 = π × radius²
   - 周长 = 2 × π × radius
3. **Rectangle**（继承自 Shape）：

   - 构造函数接收 `width` 和 `height`（double）
   - 面积 = width × height
   - 周长 = 2 × (width + height)

### 预期结果

```
GetCircleArea(5.0) -> 78.54
GetCirclePerimeter(5.0) -> 31.42
GetRectangleArea(4.0, 6.0) -> 24.0
GetRectanglePerimeter(4.0, 6.0) -> 20.0
```

### 解答

```csharp
using System;

// 抽象类 Shape，包含两个抽象方法
public abstract class Shape
{
    public abstract double CalculateArea();
    public abstract double CalculatePerimeter();
}

// Circle 类继承自 Shape
// - 构造函数接收 double 类型的 radius
// - CalculateArea() 使用 Math.PI * radius * radius
// - CalculatePerimeter() 使用 2 * Math.PI * radius
public class Circle : Shape
{
    private double radius;
    
    public Circle(double radius)
    {
        this.radius = radius;
    }
    
    public override double CalculateArea()
    {
        return Math.PI * radius * radius;
    }
    
    public override double CalculatePerimeter()
    {
        return 2 * Math.PI * radius;
    }
}

// Rectangle 类继承自 Shape
// - 构造函数接收 double 类型的 width 和 height
// - CalculateArea() 使用 width * height
// - CalculatePerimeter() 使用 2 * (width + height)
public class Rectangle : Shape
{
    private double width;
    private double height;
    
    public Rectangle(double width, double height)
    {
        this.width = width;
        this.height = height;
    }
    
    public override double CalculateArea()
    {
        return width * height;
    }
    
    public override double CalculatePerimeter()
    {
        return 2 * (width + height);
    }
}

public class Solution
{
    public static double GetCircleArea(double radius)
    {
        Circle circle = new Circle(radius);
        return Math.Round(circle.CalculateArea(), 2);
    }
    
    public static double GetCirclePerimeter(double radius)
    {
        Circle circle = new Circle(radius);
        return Math.Round(circle.CalculatePerimeter(), 2);
    }
    
    public static double GetRectangleArea(double width, double height)
    {
        Rectangle rect = new Rectangle(width, height);
        return Math.Round(rect.CalculateArea(), 2);
    }
    
    public static double GetRectanglePerimeter(double width, double height)
    {
        Rectangle rect = new Rectangle(width, height);
        return Math.Round(rect.CalculatePerimeter(), 2);
    }
}
```
