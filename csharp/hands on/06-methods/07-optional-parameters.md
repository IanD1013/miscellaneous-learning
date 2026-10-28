### 可选参数

可选参数允许你为方法参数定义默认值，从而在调用该方法时使其变为可选。

### 基本语法

```csharp
// 带默认值的参数 - 必须放在必填参数之后
public static void SayHello(string name, string greeting = "Hello")
{
    Console.WriteLine($"{greeting}, {name}!");
}

// 传入两个实参调用
SayHello("Alice", "Hi");  // 输出：Hi, Alice!

// 只传入必填实参调用 - 使用默认值
SayHello("Bob");          // 输出：Hello, Bob!
```

### 可选参数的规则

```csharp
// ✓ 可选参数必须放在必填参数之后
public static void Method(int required, int optional = 10) { }

// ✗ 这样无法编译 - 可选参数在必填参数之前
// public static void Method(int optional = 10, int required) { }

// 允许有多个可选参数
public static double Calculate(double value, double multiplier = 1.0, int precision = 2)
{
    return Math.Round(value * multiplier, precision);
}

Calculate(5.5);              // 使用默认值：multiplier=1.0, precision=2
Calculate(5.5, 2.0);         // 使用 multiplier=2
Calculate(5.5, 2.0, 3);      // 提供了全部实参
```

### 命名参数与可选参数

```csharp
public static string Format(string text, bool uppercase = false, bool addBrackets = false)
{
    var result = uppercase ? text.ToUpper() : text;
    return addBrackets ? $"[{result}]" : result;
}

// 使用命名参数跳过中间的可选参数
Format("hello", addBrackets: true);  // 返回：[hello]
```

### 你的任务

定义并实现一个返回个性化问候语的 `Greet` 方法。
该方法应该：

- 接收一个必填的 `name` 参数 (string)
- 接收一个可选的 `prefix` 参数，默认值为 `"Hello"`
- 以 `"{prefix}, {name}!"` 的格式返回问候语

你需要编写完整的方法定义，包括可选参数语法。

### 方法签名

```csharp
public static string Greet(string name, string prefix = "Hello")
```

### 预期结果

```
Greet("Alice") -> "Hello, Alice!"
Greet("Bob", "Hi") -> "Hi, Bob!"
Greet("World", "Greetings") -> "Greetings, World!"
```

### 解答

```csharp
using System;

public class Solution
{
    // 实现带可选 prefix 参数的 Greet 方法
    // 未提供 prefix 时默认为 "Hello"
    public static string Greet(string name, string prefix = "Hello")
    {
        return $"{prefix}, {name}!";
    }
}
```
