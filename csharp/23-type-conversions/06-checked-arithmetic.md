### Checked 算术运算

默认情况下，C# 算术运算在发生溢出时会静默绕回（wrap around）。
`checked` 关键字会强制运行时检测溢出并抛出 `OverflowException`。

### Unchecked 与 Checked 行为

```csharp
// Unchecked（默认）- 静默绕回
int max = int.MaxValue;  // 2,147,483,647
int wrapped = max + 1;   // -2,147,483,648（没有错误！）

// Checked - 抛出 OverflowException
checked
{
    int result = max + 1;  // 抛出 OverflowException
}
```

### 使用 Checked 语句块

```csharp
// 将运算包裹在 checked 块中
checked
{
    int a = 1000000;
    int b = 3000;
    int product = a * b;  // 发生溢出时抛出异常
}

// 或者对单个运算使用 checked 表达式
int result = checked(a * b);
```

### 捕获溢出

```csharp
try
{
    checked
    {
        int result = int.MaxValue * 2;
    }
}
catch (OverflowException)
{
    Console.WriteLine("Overflow detected!");
}
```

### 何时使用 Checked

| 场景 | 建议 |
| --- | --- |
| 财务计算 | 使用 checked |
| 用户输入乘法 | 使用 checked |
| 性能关键循环 | 保持 unchecked |
| 有意的绕回（哈希计算） | 保持 unchecked |

### 你的任务

编写一个方法，使用 `checked` 块安全地将两个整数相乘。
如果乘法会导致溢出，请捕获该异常并返回字符串 `"overflow"`。
否则，将结果作为字符串返回。

### 方法签名

```csharp
public static string SafeMultiply(int a, int b)
```

### 预期结果

```
SafeMultiply(5, 3) -> "15"
SafeMultiply(1000000, 3000) -> "overflow"
SafeMultiply(-10, 5) -> "-50"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string SafeMultiply(int a, int b)
    {
        try
        {
            // 在 checked 块中相乘，溢出时抛出 OverflowException
            checked
            {
                int result = a * b;
                return result.ToString();
            }
        }
        catch (OverflowException)
        {
            // 发生溢出时返回 "overflow"
            return "overflow";
        }
    }
}
```
