### 默认接口方法

默认接口方法（在 C# 8.0 中引入）允许你直接在接口中为方法提供默认实现。
类可以选择使用该默认实现，也可以使用自己的实现对其进行重写（override）。

### 为什么使用默认接口方法？

```csharp
// C# 8 之前：向接口添加方法会破坏所有实现
public interface IOldInterface
{
    void ExistingMethod(); // 所有类都必须实现这个方法
    void NewMethod();      // 添加这个方法会破坏现有代码！
}

// C# 8+：默认方法提供向后兼容性
public interface INewInterface
{
    void ExistingMethod();
    
    // 默认实现 - 现有类不需要修改
    public void NewMethod()
    {
        Console.WriteLine("Default behavior");
    }
}
```

### 使用与重写默认方法

```csharp
public interface IGreeter
{
    string Name { get; }
    
    // 默认实现
    public string Greet() => $"Hello, {Name}!";
}

// 使用默认实现 - 不需要实现 Greet()
public class SimpleGreeter : IGreeter
{
    public string Name { get; }
    public SimpleGreeter(string name) => Name = name;
}

// 使用自定义行为进行重写
public class FormalGreeter : IGreeter
{
    public string Name { get; }
    public FormalGreeter(string name) => Name = name;
    
    public string Greet() => $"Good day, {Name}. How may I assist you?";
}
```

### 重要提示：调用默认方法

```csharp
IGreeter greeter = new SimpleGreeter("Alice");
string result = greeter.Greet(); // 可行！返回 "Hello, Alice!"

// 注意：必须通过接口类型调用
SimpleGreeter simple = new SimpleGreeter("Bob");
// simple.Greet(); // 编译错误！无法通过这种方式访问
string result2 = ((IGreeter)simple).Greet(); // 强制转换后可行
```

### 你的任务

完成实现 `IVehicle` 的 `Bicycle` 和 `Car` 类。
查看 `IVehicle.cs` 文件以了解带有默认 `GetDescription()` 方法的接口。

1. **Bicycle**：实现 `IVehicle`，但**不要**重写 `GetDescription()`，让它使用默认实现
2. **Car**：实现 `IVehicle` **并**重写 `GetDescription()` 以返回 `"Car: {Brand} ({Horsepower} HP)"`
3. **GetVehicleInfo**：只需在 vehicle 上调用并返回 `GetDescription()` 的结果

### 预期结果

```
GetVehicleInfo(new Bicycle("Trek")) -> "Vehicle: Trek"
GetVehicleInfo(new Car("Tesla", 450)) -> "Car: Tesla (450 HP)"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetVehicleInfo(IVehicle vehicle)
    {
        // 调用 vehicle 的 GetDescription() 方法
        // 该方法在接口中有默认实现
        // 有些交通工具会重写它，有些则使用默认实现
        return vehicle.GetDescription();
    }
}

// 使用 IVehicle 接口实现这个类
// 不要重写 GetDescription()，使用默认实现
public class Bicycle : IVehicle
{
    public string Brand { get; }
    
    public Bicycle(string brand)
    {
        Brand = brand;
    }
    
    // Brand 属性已实现接口要求的成员
    // 不实现 GetDescription，让它使用默认实现
}

// 使用 IVehicle 接口实现这个类
// 重写 GetDescription() 以提供自定义行为
public class Car : IVehicle
{
    public string Brand { get; }
    public int Horsepower { get; }
    
    public Car(string brand, int horsepower)
    {
        Brand = brand;
        Horsepower = horsepower;
    }
    
    // Brand 属性已实现接口要求的成员
    // 重写 GetDescription，包含马力信息
    public string GetDescription()
    {
        return $"Car: {Brand} ({Horsepower} HP)";
    }
}
```
