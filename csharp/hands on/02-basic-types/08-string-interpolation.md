### 字符串插值

字符串插值（String interpolation）允许你使用 `$` 前缀和大括号 `{}` 直接将变量和表达式嵌入到字符串中。

### 基本语法

```csharp
string name = "Alice";
int score = 95;

// 不使用插值（拼接）
string message1 = "Hello, " + name + "! Your score is " + score + ".";

// 使用插值（更简洁！）
string message2 = $"Hello, {name}! Your score is {score}.";
```

### 嵌入不同类型

```csharp
int quantity = 3;
double price = 9.99;
decimal total = 29.97m;

Console.WriteLine($"You bought {quantity} items");
Console.WriteLine($"Price per item: ${price}");
Console.WriteLine($"Total: ${total}");
```

### 花括号内的表达式

你可以在大括号内放入任何 C# 表达式：

```csharp
int a = 5;
int b = 3;
Console.WriteLine($"Sum: {a + b}");  // 打印：Sum: 8
Console.WriteLine($"Product: {a * b}");  // 打印：Product: 15
```

### 你的任务

创建一个方法，使用字符串插值打印格式化的用户个人资料。
该资料应在单独的行上分别显示用户的姓名、年龄、身高和账户余额。

### 方法签名

```csharp
public static void PrintUserProfile(string name, int age, double height, decimal balance)
```

### 预期输出格式

```
Name: [name]
Age: [age] years old
Height: [height]m
Balance: $[balance]
```

### 预期结果

```
PrintUserProfile("Alice", 25, 1.65, 1000.50m)
-> Name: Alice
   Age: 25 years old
   Height: 1.65m
   Balance: $1000.50
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintUserProfile(string name, int age, double height, decimal balance)
    {
        // 使用字符串插值打印格式化的用户资料，共 4 行
        Console.WriteLine($"Name: {name}");
        Console.WriteLine($"Age: {age} years old");
        Console.WriteLine($"Height: {height}m");
        // :F2 保证余额始终显示两位小数（例如 500 显示为 500.00）
        Console.WriteLine($"Balance: ${balance:F2}");
    }
}
```
