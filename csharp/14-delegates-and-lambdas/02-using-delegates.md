### 使用委托

一旦定义了委托类型，就可以通过分配与其签名匹配的方法来创建它的实例。
然后，你可以像调用普通方法一样调用委托。

### 将方法分配给委托

```csharp
// 定义委托类型
public delegate int Calculator(int x, int y);

// 与委托签名匹配的方法
public static int Add(int a, int b) => a + b;
public static int Multiply(int a, int b) => a * b;

// 将方法分配给委托实例
Calculator calc = Add;        // 直接赋值
Calculator calc2 = Multiply;  // 不同的方法，相同的签名
```

### 调用委托

```csharp
// 一旦赋值，就可以像普通方法一样调用
Calculator calc = Add;
int result = calc(5, 3);  // 调用 Add(5, 3)，返回 8

// 也可以显式使用 .Invoke()
int result2 = calc.Invoke(10, 2);  // 等同于 calc(10, 2)
```

### 委托作为参数

```csharp
// 方法可以接收委托作为参数
public static int ApplyTwice(int value, Calculator operation)
{
    int temp = operation(value, value);
    return operation(temp, temp);
}

// 用法
int doubled = ApplyTwice(2, Add);      // (2+2) 然后 (4+4) = 8
int squared = ApplyTwice(2, Multiply); // (2*2) 然后 (4*4) = 16
```

### 你的任务

系统已为你提供了一个预先定义好的 `Greeter` 委托和三个问候方法。
请完成 `ExecuteGreeting` 方法，该方法接收一个名称和一个 `Greeter` 委托，然后使用该名称调用委托并返回结果。

### 方法签名

```csharp
public static string ExecuteGreeting(string name, Greeter greeter)
```

### 预期结果

```
ExecuteGreeting("Alice", FormalGreeting) -> "Good day, Alice. How may I assist you?"
ExecuteGreeting("Bob", CasualGreeting) -> "Hey Bob! What's up?"
ExecuteGreeting("Charlie", ShortGreeting) -> "Hi Charlie!"
```

### 解答

```csharp
using System;

// 接收一个 string 并返回一个 string 的委托类型
public delegate string Greeter(string name);

public class Solution
{
    // 该方法生成正式的问候语
    public static string FormalGreeting(string name)
    {
        return $"Good day, {name}. How may I assist you?";
    }
    
    // 该方法生成随意的问候语
    public static string CasualGreeting(string name)
    {
        return $"Hey {name}! What's up?";
    }
    
    // 该方法生成简短的问候语
    public static string ShortGreeting(string name)
    {
        return $"Hi {name}!";
    }
    
    public static string ExecuteGreeting(string name, Greeter greeter)
    {
        // 调用委托并返回结果
        return greeter(name);
    }
}
```
