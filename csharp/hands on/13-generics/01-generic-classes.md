### 泛型类

泛型类允许你创建适用于任何类型的可重用容器。
你无需为 `BoxOfInt`、`BoxOfString` 等分别编写独立的类，只需编写一个 `Box<T>` 类。

### 类型参数

```csharp
// T 是类型参数 - 任意类型的占位符
public class Box<T>
{
    public T Value { get; set; }
    
    public Box(T value)
    {
        Value = value;
    }
}
```

### 使用泛型类

```csharp
// 为不同类型创建 box
Box<int> intBox = new Box<int>(42);
Box<string> stringBox = new Box<string>("Hello");
Box<double> doubleBox = new Box<double>(3.14);

// 访问值 - 强类型！
int number = intBox.Value;      // 42
string text = stringBox.Value;  // "Hello"
```

### 相比 object 的优势

```csharp
// 不使用泛型（使用 object）- 需要强制转换，不是类型安全的
object box = 42;
int value = (int)box;  // 必须强制转换，可能在运行时抛出异常

// 使用泛型 - 编译时类型安全
Box<int> box = new Box<int>(42);
int value = box.Value;  // 无需强制转换，编译器确保类型安全
```

### 你的任务

1. 在 `Box.cs` 中完成 `Box<T>` 类：

   - 添加一个类型为 `T` 的 `Value` 属性
   - 添加一个接受 `T` 类型参数并设置 `Value` 的构造函数
2. 在 `Main.cs` 中实现两个辅助方法：

   - `CreateBox<T>(T value)` - 创建并返回一个新的 `Box<T>`
   - `GetBoxValue<T>(Box<T> box)` - 返回存储在 box 中的值

### 方法签名

```csharp
public static Box<T> CreateBox<T>(T value)
public static T GetBoxValue<T>(Box<T> box)
```

### 预期结果

```
CreateBox(42).Value -> 42
CreateBox("Hello").Value -> "Hello"
GetBoxValue(new Box<int>(100)) -> 100
```

### 解答

Main.cs

```csharp
using System;

public class Solution
{
    public static Box<T> CreateBox<T>(T value)
    {
        // 创建并返回一个包含该值的新 Box
        return new Box<T>(value);
    }
    
    public static T GetBoxValue<T>(Box<T> box)
    {
        // 返回 box 中存储的值
        return box.Value;
    }
}
```

Box.cs

```csharp
/// <summary>
/// 一个可以存储任意类型值的泛型 Box 类。
/// 类型参数 T 在创建实例时指定。
/// </summary>
/// <typeparam name="T">要存储在 box 中的值的类型</typeparam>
public class Box<T>
{
    // 存储值的属性
    public T Value { get; set; }
    
    // 接受初始值的构造函数
    public Box(T value)
    {
        Value = value;
    }
}
```
