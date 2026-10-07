### If-Else 语句

`if-else` 语句通过在条件为 false 时提供备用代码块来扩展 `if`。

### 基本结构

```csharp
if (condition)
{
    // condition 为 true 时运行
}
else
{
    // condition 为 false 时运行
}
```

### If 与 If-Else

仅使用 `if` 时，代码块之后的代码始终会运行。
而使用 `if-else` 时，只会恰好执行其中一个代码块：

```csharp
// 只有 if - 没有备选操作
if (temperature > 30)
{
    Console.WriteLine("It's hot!");
}

// If-else - 总会走其中一条路径
if (temperature > 30)
{
    Console.WriteLine("It's hot!");
}
else
{
    Console.WriteLine("It's not hot.");
}
```

### 取模运算符

`%` 运算符返回除法运算后的余数。
它非常适合用来检查整除性：

| 表达式 | 结果 | 解释 |
| --- | --- | --- |
| `10 % 2` | 0 | 10 ÷ 2 = 5，余数 0 |
| `7 % 2` | 1 | 7 ÷ 2 = 3，余数 1 |
| `15 % 3` | 0 | 15 ÷ 3 = 5，余数 0 |

如果 `number % 2 == 0`，则该数字为**偶数**（even），否则为**奇数**（odd）。

### 你的任务

编写一个方法，如果数字能被 2 整除，则打印 "Even"，否则打印 "Odd"。

### 方法签名

```csharp
public static void PrintEvenOrOdd(int number)
```

### 预期结果

```
PrintEvenOrOdd(4)  -> 打印 "Even"
PrintEvenOrOdd(7)  -> 打印 "Odd"
PrintEvenOrOdd(0)  -> 打印 "Even"
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintEvenOrOdd(int number)
    {
        // 能被 2 整除（余数为 0）则为偶数，否则为奇数
        if (number % 2 == 0)
        {
            Console.WriteLine("Even");
        }
        else
        {
            Console.WriteLine("Odd");
        }
    }
}
```
