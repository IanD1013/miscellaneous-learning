### 泛型约束

泛型约束限制了哪些类型可以用作类型参数。
它们确保泛型类型具有特定的功能，使你能够在泛型代码中安全地使用某些操作。

### `where` 关键字

```csharp
// 语法：where T : 约束
public static T DoSomething<T>() where T : new()
{
    return new T();  // 正是因为有该约束才能这样写
}

public static void Process<T>(T item) where T : class
{
    // T 必须是引用类型
}

public static T Add<T>(T a, T b) where T : struct
{
    // T 必须是值类型
}
```

### 常见约束

| 约束 | 描述 | 示例 |
| --- | --- | --- |
| `where T : new()` | T 必须具有无参数构造函数 | 允许 `new T()` |
| `where T : class` | T 必须是引用类型 | 类、接口 |
| `where T : struct` | T 必须是值类型 | int、double、结构体 |
| `where T : SomeClass` | T 必须继承自 SomeClass | 确保继承关系 |
| `where T : IInterface` | T 必须实现 IInterface | 确保具备相应功能 |

### 为什么约束很重要

```csharp
// 没有约束 - 这无法编译！
public static T Create<T>()
{
    return new T();  // 错误：T 可能没有构造函数
}

// 有约束 - 编译器知道 T 可以被实例化
public static T Create<T>() where T : new()
{
    return new T();  // 可以正常工作！
}
```

### 你的任务

创建一个泛型方法 `CreateInstance<T>()`，用于创建并返回类型为 `T` 的新实例。
该方法必须使用 `new()` 约束，以确保只能使用具有无参数构造函数的类型。

### 方法签名

```csharp
public static T CreateInstance<T>() where T : new()
```

### 预期结果

```csharp
CreateInstance<Person>() -> Person with Name="Unknown", Age=0
CreateInstance<Product>() -> Product with Title="Untitled", Price=0
CreateInstance<Counter>() -> Counter with Count=0
```

### 解答

```csharp
using System;

public class Solution
{
    public static T CreateInstance<T>() where T : new()
    {
        // new() 约束保证 T 有无参数构造函数，因此可以使用 new T()
        return new T();
    }
}

public class Person
{
    public string Name { get; set; } = "Unknown";
    public int Age { get; set; } = 0;
}

public class Product
{
    public string Title { get; set; } = "Untitled";
    public decimal Price { get; set; } = 0m;
}

public class Counter
{
    public int Count { get; set; } = 0;
}
```
