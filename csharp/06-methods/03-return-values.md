### 返回值

方法可以使用 `return` 语句将数据返回给调用它们的代码。
方法签名中的返回类型告诉 C# 将要返回什么类型的值。

### 返回类型对比 void

```csharp
// void 方法 - 执行操作，不返回任何值
public static void SayHello()
{
    Console.WriteLine("Hello!");
}

// 带返回类型的方法 - 返回一个值
public static int GetAge()
{
    return 25;
}

public static string GetGreeting()
{
    return "Welcome!";
}
```

### return 语句

`return` 语句做两件事：

1. 指定要返回的值
2. 立即退出该方法

```csharp
public static int Double(int x)
{
    return x * 2;  // 返回结果并退出
}

public static bool IsPositive(int number)
{
    return number > 0;  // 返回 true 或 false
}
```

### 使用返回值

```csharp
// 将返回值存储在变量中
int result = Double(5);  // result = 10

// 直接在表达式中使用
int total = Double(3) + Double(4);  // total = 14

// 在条件中使用
if (IsPositive(5))
{
    Console.WriteLine("Positive!");
}
```

### 你的任务

创建一个名为 `Square` 的方法，该方法接受一个整数并返回它的平方（即该数字乘以它本身）。

### 方法签名

```csharp
public static int Square(int number)
```

### 预期结果

```
Square(2) -> 4
Square(5) -> 25
Square(-3) -> 9
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Square(int number)
    {
        // 返回该数字乘以它本身
        return number * number;
    }
}
```
