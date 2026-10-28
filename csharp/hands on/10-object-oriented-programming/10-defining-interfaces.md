### C# 中的接口

接口定义了类必须遵循的契约。
它指定了一个类**做什么**，而不是**如何做**。
当你希望不相关的类共享通用行为时，可以使用接口。

### 定义接口

```csharp
// 使用 'interface' 关键字
public interface IMovable
{
    // 只有方法签名 - 没有实现
    string Move();
}

// 接口可以有多个成员
public interface IVehicle
{
    string Start();
    string Stop();
    int Speed { get; set; }
}
```

### 接口与抽象类的对比

| 特性 | 接口 | 抽象类 |
| --- | --- | --- |
| 实现 | 无方法体 | 可以有方法体 |
| 继承 | 类可以实现多个接口 | 类只能继承一个抽象类 |
| 字段 | 无实例字段 | 可以有字段 |
| 构造函数 | 无构造函数 | 可以有构造函数 |

### 实现接口

```csharp
public class Dog : IMovable
{
    // 必须实现接口的所有成员
    public string Move()
    {
        return "Dog is running";
    }
}

public class Fish : IMovable
{
    public string Move()
    {
        return "Fish is swimming";
    }
}
```

### 为什么使用接口？

```csharp
// 你可以统一地处理不同的类型
public static void MoveAll(IMovable[] movables)
{
    foreach (var m in movables)
    {
        Console.WriteLine(m.Move());
    }
}

// 适用于任何 IMovable！
MoveAll(new IMovable[] { new Dog(), new Fish() });
```

### 你的任务

1. 定义一个包含单个方法 `string Move()` 的 `IMovable` 接口
2. `TestMovement` 方法应接受任意 `IMovable` 并返回调用 `Move()` 的结果
3. 查看 `Vehicles.cs`，它包含了已经实现 `IMovable` 的 `Car`、`Boat` 和 `Airplane` 类。一旦你正确定义了接口，它们就能够正常编译！

### 方法签名

```csharp
public static string TestMovement(IMovable movable)
```

### 预期结果

```
TestMovement(new Car("Tesla")) -> "Tesla is driving on the road"
TestMovement(new Boat("Titanic")) -> "Titanic is sailing on water"
TestMovement(new Airplane("AA100")) -> "Flight AA100 is flying through the sky"
```

### 解答

```csharp
using System;

// 定义 IMovable 接口
public interface IMovable
{
    // Move() 方法签名
    string Move();
}

public class Solution
{
    public static string TestMovement(IMovable movable)
    {
        // 调用 movable 对象的 Move() 方法并返回结果
        return movable.Move();
    }
}
```
