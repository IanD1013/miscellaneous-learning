### 多接口实现

一个类可以实现多个接口，从而赋予它来自不同契约的能力。
这非常强大，因为 C# 不支持类的多重继承，但一个类可以根据需要实现任意数量的接口。

### 多接口语法

```csharp
public class MyClass : IFirstInterface, ISecondInterface
{
    // 必须实现两个接口中的所有方法
    public void MethodFromFirst() { }
    public void MethodFromSecond() { }
}
```

### 为什么使用多接口？

```csharp
// 每个接口定义一种特定的能力
public interface ISwimmable { void Swim(); }
public interface IFlyable { void Fly(); }

// 鸭子两者都能做到！
public class Duck : ISwimmable, IFlyable
{
    public void Swim() => Console.WriteLine("Swimming");
    public void Fly() => Console.WriteLine("Flying");
}
```

### 接口隔离

多个小接口通常比一个大接口更好：

```csharp
// 好的做法：专注的接口
public interface IPrintable { void Print(); }
public interface ISaveable { void Save(); }

// 一个文档可能同时实现两者
public class Document : IPrintable, ISaveable { ... }
```

### 你的任务

实现一个同时实现 `IMovable` 和 `ISoundMaker` 接口的 `Robot` 类。

接口定义在 `Interfaces.cs` 中（只读）：

- `IMovable` 拥有一个返回字符串的 `Move()` 方法
- `ISoundMaker` 拥有一个返回字符串的 `MakeSound()` 方法

你的 `Robot` 类应该：

- 在 `Move()` 中返回 `"Moving forward"`
- 在 `MakeSound()` 中返回 `"Beep boop!"`

同时完成 `TestRobot` 方法，调用这两个方法并返回合并后的结果。

### 方法签名

```csharp
public class Robot : IMovable, ISoundMaker
public static string TestRobot(Robot robot)
```

### 预期结果

```
TestRobot(new Robot()) -> "Moving forward Beep boop!"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string TestRobot(Robot robot)
    {
        // 调用 robot.Move() 和 robot.MakeSound()
        // 用一个空格将两个结果合并后返回
        return $"{robot.Move()} {robot.MakeSound()}";
    }
}

// Robot 类同时实现 IMovable 和 ISoundMaker
public class Robot : IMovable, ISoundMaker
{
    // Move() 返回 "Moving forward"
    public string Move()
    {
        return "Moving forward";
    }
    
    // MakeSound() 返回 "Beep boop!"
    public string MakeSound()
    {
        return "Beep boop!";
    }
}
```
