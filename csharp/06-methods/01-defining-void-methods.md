### Void 方法

**void 方法**是一种执行操作但不返回任何值的方法。
当你的方法需要执行代码而不向调用者返回数据时，请使用 `void` 作为返回类型。

### 定义 Void 方法

```csharp
// 基本的 void 方法语法
public static void SayHello()
{
    Console.WriteLine("Hello!");
}

// 带参数的 void 方法
public static void PrintNumber(int number)
{
    Console.WriteLine(number);
}
```

### 访问修饰符

方法可以具有不同的访问级别：

| 修饰符 | 描述 |
| --- | --- |
| `public` | 可从任何地方访问 |
| `private` | 仅可在同一个类中访问 |

```csharp
// 私有方法 - 只能从 Solution 类内部调用
private static void SecretMethod()
{
    Console.WriteLine("This is private!");
}

// 公共方法 - 可以从外部调用
public static void PublicMethod()
{
    SecretMethod(); // 在类内部调用私有方法
}
```

`static` 不是访问修饰符。
它是一个独立的关键字，表示该方法属于类本身，而不是属于从该类创建的对象。
两者通常结合使用，如 `private static void`。
下一节将解释在调用方法时这意味着什么。

### 调用静态方法与实例方法

调用方法的方式取决于它是 **static**（静态）还是 **instance method**（实例方法）：

```csharp
public class Example
{
    // 静态方法 - 属于类本身
    public static void StaticMethod()
    {
        Console.WriteLine("I'm static!");
    }

    // 实例方法 - 属于对象
    public void InstanceMethod()
    {
        Console.WriteLine("I'm an instance method!");
    }
}

// 调用静态方法 - 使用类名或在同一个类中直接调用
Example.StaticMethod();  // 从类外部调用
StaticMethod();          // 从同一个类内部调用

// 调用实例方法 - 需要先创建一个对象
Example obj = new Example();
obj.InstanceMethod();  // 必须在实例上调用
```

**关键区别：** 静态方法可以直接使用类名（或在同一个类中直接使用方法名）来调用。
实例方法要求你先使用 `new` 创建一个对象。

在本练习中，我们使用的是 `static` 方法，因此你可以在同一个类中直接通过名称调用它们。

### 你的任务

1. 创建一个名为 `PrintGreeting` 的 **private static** 方法，该方法将 `Hello, World!` 打印到控制台
2. 在 `Greet` 方法内部调用 `PrintGreeting`

### 方法签名

```csharp
public static void Greet()
private static void PrintGreeting()
```

### 预期结果

```
Greet() 打印：Hello, World!
```

### 解答

```csharp
using System;

public class Solution
{
    public static void Greet()
    {
        // 在这里调用私有的问候方法
        PrintGreeting();
    }

    // 定义一个名为 PrintGreeting 的私有方法，打印 "Hello, World!"
    private static void PrintGreeting()
    {
        Console.WriteLine("Hello, World!");
    }
}
```
