### params 关键字

`params` 关键字允许方法接受可变数量的同类型参数。
调用者无需手动创建数组，可以直接传递任意数量的参数。

### 基本语法

```csharp
// 不使用 params - 调用者必须创建一个数组
public static void PrintNumbers(int[] numbers) { }
PrintNumbers(new int[] { 1, 2, 3 }); // 比较繁琐

// 使用 params - 调用者直接传递值
public static void PrintNumbers(params int[] numbers) { }
PrintNumbers(1, 2, 3);        // 简洁！
PrintNumbers(1, 2, 3, 4, 5);  // 任意数量的参数
PrintNumbers();               // 零个参数也可以
```

### 工作原理

```csharp
public static double Average(params double[] values)
{
    if (values.Length == 0) return 0;
    
    double sum = 0;
    foreach (double value in values)
    {
        sum += value;
    }
    return sum / values.Length;
}

// 以下所有调用都是有效的：
Average(5.0);                    // 1 个参数
Average(10.0, 20.0);             // 2 个参数
Average(1.5, 2.5, 3.5, 4.5);     // 4 个参数
```

### params 的规则

| 规则 | 描述 |
| --- | --- |
| 位置 | 必须是方法签名中的最后一个参数 |
| 数量 | 每个方法只允许有一个 `params` 参数 |
| 类型 | 必须是数组类型，例如 `int[]`。从 C# 13 开始，它也可以是 span 或集合类型，例如 `IEnumerable<T>` 或 `List<T>`。不允许使用多维数组，如 `int[,]` |
| 可选 | 调用者可以传递零个或多个参数 |

本课程使用数组形式 `params int[]`。
请在下面的练习中保持给定的方法签名。

### 与其他参数结合使用

```csharp
public static string FormatMessage(string prefix, params string[] words)
{
    return prefix + ": " + string.Join(", ", words);
}

FormatMessage("Items", "apple", "banana", "cherry");
// 返回: "Items: apple, banana, cherry"
```

### 你的任务

实现一个方法，使用 `params` 关键字计算传递给它的所有数字之和。
该方法应能处理任意数量的整数参数，包括零个参数（此时应返回 0）。

### 方法签名

```csharp
public static int SumAll(params int[] numbers)
```

### 预期结果

```
SumAll(1, 2, 3) -> 6
SumAll(10) -> 10
SumAll() -> 0
SumAll(5, 5, 5, 5, 5) -> 25
```

### 解答

```csharp
using System;

public class Solution
{
    public static int SumAll(params int[] numbers)
    {
        // 没有参数时 numbers 是空数组，循环不执行，返回 0
        int sum = 0;
        foreach (int number in numbers)
        {
            sum += number;
        }
        return sum;
    }
}
```
