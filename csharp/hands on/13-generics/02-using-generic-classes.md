### 实例化泛型类

当你使用泛型类时，必须指定替换类型参数 `T` 的实际类型。
这将创建该类的一个具体且类型安全的版本。

### 指定类型实参

```csharp
// 泛型类定义
public class Box<T>
{
    public T Value { get; set; }

    public Box(T value)
    {
        Value = value;
    }
}

// 使用具体类型创建实例
Box<int> intBox = new Box<int>(42);        // T 变为 int
Box<string> stringBox = new Box<string>("hello");  // T 变为 string
Box<double> doubleBox = new Box<double>(3.14);     // T 变为 double
```

### 类型安全实战

一旦指定了类型，编译器就会对其进行强制约束：

```csharp
Box<int> numbers = new Box<int>(100);
int value = numbers.Value;     // 无需强制转换！
// numbers.Value = "text";     // 编译错误！不能将 string 赋值给 int

Box<string> words = new Box<string>("C#");
string text = words.Value;     // 类型安全的访问
```

### 不同的类型，相同的类

每次实例化都会创建一个不同的类型：

```csharp
Box<int> box1 = new Box<int>(5);
Box<string> box2 = new Box<string>("five");
// box1 和 box2 是完全不同的类型
// 但共享同一个底层泛型定义
```

### 一次返回两个值

本练习要求从一个方法中返回两个 box。
C# 允许你将多个值用圆括号组合在一起并同时返回：

```csharp
// 返回类型按顺序列出两个类型
public static (int, string) GetPair()
{
    return (42, "hello");
}

// 使用 Item1、Item2 等读取它们
var pair = GetPair();
int number = pair.Item1;   // 42
string text = pair.Item2;  // "hello"
```

这种组合被称为元组（tuple）。
在课程后面的章节中会有专门关于元组的详细讲解；目前你只需掌握上面的语法即可。

### 你的任务

使用两种不同的类型实参创建泛型类 `Box<T>` 的实例：

1. 创建一个包含给定数字的 `Box<int>`
2. 创建一个包含给定文本的 `Box<string>`
3. 将这两个 box 作为元组返回

### 方法签名

```csharp
public static (Box<int>, Box<string>) CreateBoxes(int number, string text)
```

### 预期结果

```
GetBoxContents(42, "hello") -> "Int: 42, String: hello"
GetBoxContents(0, "empty") -> "Int: 0, String: empty"
```

### 解答

```csharp
using System;

public class Box<T>
{
    public T Value { get; set; }
    
    public Box(T value)
    {
        Value = value;
    }
}

public class Solution
{
    public static (Box<int>, Box<string>) CreateBoxes(int number, string text)
    {
        // 创建一个包含 number 的 Box<int>
        Box<int> intBox = new Box<int>(number);
        // 创建一个包含 text 的 Box<string>
        Box<string> stringBox = new Box<string>(text);
        // 将两个 box 作为元组返回
        return (intBox, stringBox);
    }
    
    public static string GetBoxContents(int number, string text)
    {
        var boxes = CreateBoxes(number, text);
        return $"Int: {boxes.Item1.Value}, String: {boxes.Item2.Value}";
    }
}
```
