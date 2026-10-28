### 运算顺序

C# 遵循数学中的运算符优先级规则（PEMDAS/BODMAS）。
乘法和除法会在加法和减法之前执行。
圆括号可以改变这种默认顺序。

### 默认优先级

```csharp
int result1 = 2 + 3 * 4;    // = 2 + 12 = 14（先算乘法）
int result2 = 10 - 6 / 2;   // = 10 - 3 = 7（先算除法）
int result3 = 8 / 4 * 2;    // = 2 * 2 = 4（相同优先级从左到右）
```

### 使用圆括号

无论默认优先级如何，圆括号都会强制优先执行括号内的运算。

```csharp
int result1 = (2 + 3) * 4;  // = 5 * 4 = 20（先算圆括号）
int result2 = (10 - 6) / 2; // = 4 / 2 = 2（先算圆括号）
int result3 = 10 / (2 + 3); // = 10 / 5 = 2（先算圆括号）
```

### 运算符优先级表

| 优先级 | 运算符 | 说明 |
| --- | --- | --- |
| 1 (高) | `( )` | 圆括号 |
| 2 | `*`, `/`, `%` | 乘法、除法、取模 |
| 3 (低) | `+`, `-` | 加法、减法 |

### 你的任务

编写一个计算 `(a + b) * c` 的方法。
你必须使用圆括号来确保加法在乘法之前执行。

### 方法签名

```csharp
public static int Calculate(int a, int b, int c)
```

### 预期结果

```
Calculate(2, 3, 4) -> 20
Calculate(5, 5, 2) -> 20
Calculate(0, 10, 5) -> 50
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Calculate(int a, int b, int c)
    {
        // 用圆括号确保先计算 (a + b)，再乘以 c
        return (a + b) * c;
    }
}
```
