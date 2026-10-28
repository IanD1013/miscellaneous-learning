### 方法参数

方法可以接收多个参数，允许你将数据传递给它们进行处理。
参数在方法名称后面的圆括号中定义，并用逗号分隔。

### 定义多个参数

```csharp
// 带两个参数的方法
public static void Greet(string firstName, string lastName)
{
    Console.WriteLine("Hello, " + firstName + " " + lastName);
}

// 带三个参数的方法
public static void PrintRectangleArea(int width, int height, string unit)
{
    Console.WriteLine(width * height + " " + unit);
}
```

### 调用带参数的方法

调用方法时，必须按照定义参数的相同顺序提供实参：

```csharp
// 实参与参数的顺序一一对应
Greet("John", "Doe");        // firstName = "John", lastName = "Doe"
PrintRectangleArea(5, 10, "cm²");  // width = 5, height = 10, unit = "cm²"
```

### 从 Main 中调用

`Main` 方法是程序的入口点。
你可以从 `Main` 中调用其他方法：

```csharp
public static void Main()
{
    SayHello();      // 调用一个没有参数的方法
    Add(10, 20);     // 调用一个带两个参数的方法
}
```

### 你的任务

`PrintSum` 方法已为你预先声明，它带有两个整数参数 `a` 和 `b`。
请填充其方法体，使其将它们的和打印到控制台。
然后从 `Main` 中使用参数值 `5` 和 `3` 调用它，这次单次调用即为 `Main` 应该执行的全部内容。

### 方法签名

```csharp
public static void PrintSum(int a, int b)
```

### 预期结果

仅从 `Main` 中调用 `PrintSum(5, 3)`，使你的程序刚好打印一行：

```
8
```

随后你的 `PrintSum` 方法将使用更多值单独进行测试：

```
PrintSum(10, 20)   打印：30
PrintSum(-5, 5)    打印：0
PrintSum(0, 0)     打印：0
PrintSum(100, 250) 打印：350
PrintSum(-10, -15) 打印：-25
```

### 解答

```csharp
using System;

public class Solution
{
    public static void Main()
    {
        // 使用 5 和 3 调用 PrintSum
        PrintSum(5, 3);
    }
    
    public static void PrintSum(int a, int b)
    {
        // 打印 a 与 b 的和
        Console.WriteLine(a + b);
    }
}
```
