### 实现接口

接口定义了类必须遵循的契约。
当一个类实现某个接口时，它必须为该接口中声明的所有成员提供具体的实现。

### 实现语法

```csharp
// 接口定义
public interface IMovable
{
    void Move(int distance);
    int TotalDistance { get; }
}

// 实现该接口的类
public class Robot : IMovable
{
    public int TotalDistance { get; private set; }
    
    public void Move(int distance)
    {
        TotalDistance += distance;
        Console.WriteLine($"Robot moved {distance} units");
    }
}
```

### 接口与抽象类的区别

| 特性 | 接口 | 抽象类 |
| --- | --- | --- |
| 实现 | 无实现 | 可以包含实现 |
| 多重继承 | 类可以实现多个接口 | 类只能继承一个基类 |
| 字段 | 无实例字段 | 可以包含字段 |
| 访问修饰符 | 成员默认为 public | 可以不同 |

### 理解多态

多态的意思是“多种形态”，它允许将不同类的对象视为同一个公共接口或基类型的对象。
当你使用接口时，你将获得**基于接口的多态性**：

```csharp
// 实现同一接口的不同类
public class Car : IMovable { /* 实现 */ }
public class Robot : IMovable { /* 实现 */ }
public class Drone : IMovable { /* 实现 */ }

// 多态的实际应用 - 一个方法适用于任何 IMovable
void MoveAll(IMovable[] movables, int distance)
{
    foreach (IMovable m in movables)
    {
        m.Move(distance);  // 为每种类型调用正确的 Move()！
    }
}

// 每个对象根据其实际类型做出不同的响应
IMovable[] fleet = { new Car("Tesla"), new Robot(), new Drone() };
MoveAll(fleet, 10);  // Car 移动、Robot 移动、Drone 移动 - 各自以自己的方式
```

多态的强大之处在于你的代码不需要知道具体类型，它只需要知道该对象可以执行 `Move()`。
这使得你的代码更加灵活且易于扩展。

### 使用接口类型

```csharp
// 你可以将接口用作类型
IMovable movable = new Robot();
movable.Move(10);  // 可行！使用 Robot 的实现

// 同一个变量可以保存任何 IMovable
movable = new Car("Honda");
movable.Move(10);  // 现在使用 Car 的实现
```

### 你的任务

在 `Car` 类中实现 `IMovable` 接口。
该接口定义在 `IMovable.cs` 中，要求：

- 一个 `Move(int distance)` 方法，用于将距离累加到 `TotalDistance`
- 一个 `TotalDistance` 属性（已声明，只需要 Move 方法来更新它）

然后完成 `GetTotalDistanceTraveled` 方法，根据 movements 数组中的每个值移动汽车，并返回总距离。

### 方法签名

```csharp
public static int GetTotalDistanceTraveled(Car car, int[] movements)
```

### 预期结果

```
GetTotalDistanceTraveled(new Car("Tesla"), [10, 20, 30]) -> 60
GetTotalDistanceTraveled(new Car("Honda"), [5]) -> 5
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetTotalDistanceTraveled(Car car, int[] movements)
    {
        // 根据每个 movement 值移动汽车
        foreach (int distance in movements)
        {
            car.Move(distance);
        }
        
        // 返回汽车的总行驶距离
        return car.TotalDistance;
    }
}

// 在 Car 类中实现 IMovable 接口
public class Car : IMovable
{
    public string Model { get; set; }
    public int TotalDistance { get; private set; }
    
    public Car(string model)
    {
        Model = model;
        TotalDistance = 0;
    }
    
    // 实现 IMovable 中的 Move 方法
    // 每次调用都将距离累加到 TotalDistance
    public void Move(int distance)
    {
        TotalDistance += distance;
    }
}
```
