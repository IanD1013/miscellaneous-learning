### 泛型方法

泛型方法是定义了自己类型参数的方法，独立于它们所属的任何类。
当你需要为单个操作提供类型灵活性而无需创建泛型类时，请使用它们。

### 方法语法

```csharp
// 泛型方法声明
public static T Identity<T>(T input)
{
    return input;
}

// 方法名后面的 <T> 声明了类型参数
public static void Display<T>(T item)
{
    Console.WriteLine(item);
}
```

### 类型推断

编译器通常可以从你传入的参数中推断出类型参数：

```csharp
// 显式类型实参
string result1 = Identity<string>("hello");

// 类型推断 - 编译器推断出 T 是 int
int result2 = Identity(42);
```

### 获取类型信息

在泛型方法内部，你可以获取有关实际类型的信息：

```csharp
public static string GetTypeName<T>(T value)
{
    // typeof(T) 获取 T 的 Type 对象
    return typeof(T).Name;  // 返回 "Int32"、"String" 等
}
```

### 泛型方法 vs 泛型类

| 方面 | 泛型类 | 泛型方法 |
| --- | --- | --- |
| 作用域 | 整个类 | 单个方法 |
| 声明 | `class Box<T>` | `void Print<T>(T value)` |
| 使用场景 | 可复用容器 | 一次性操作 |

### 你的任务

创建一个泛型 `Print` 方法，该方法接收任意值并返回一个格式化字符串，显示该值及其类型名称。

### 方法签名

```csharp
public static string Print<T>(T value)
```

### 预期结果

```
Print(42) -> "Value: 42, Type: Int32"
Print("hello") -> "Value: hello, Type: String"
Print(3.14) -> "Value: 3.14, Type: Double"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string Print<T>(T value)
    {
        // 使用 typeof(T).Name 获取类型名称，并与值一起格式化
        return $"Value: {value}, Type: {typeof(T).Name}";
    }
}
```
