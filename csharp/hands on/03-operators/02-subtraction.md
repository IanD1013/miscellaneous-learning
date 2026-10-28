### 减法运算符

减法运算符（`-`）计算两个数字之间的差值。
它从左操作数中减去右操作数。

### 基本用法

```csharp
int result = 10 - 3;    // result 为 7
int diff = 100 - 45;    // diff 为 55
int negative = 5 - 10;  // negative 为 -5
```

### 减法与加法

加法是将数值合并，而减法是求差值：

```csharp
int sum = 8 + 3;        // 11（合并）
int difference = 8 - 3; // 5（求差值）
```

### 处理负数

减法可以产生负数结果，也可以对负操作数进行运算：

```csharp
int result1 = 3 - 10;     // -7（正数减去更大的正数）
int result2 = -5 - 3;     // -8（负数减去正数）
int result3 = -5 - (-3);  // -2（减去负数相当于加）
```

### 你的任务

实现一个方法，从第一个数字中减去第二个数字并返回结果。

### 方法签名

```csharp
public static int Subtract(int a, int b)
```

### 预期结果

```
Subtract(10, 3) -> 7
Subtract(5, 5) -> 0
Subtract(3, 10) -> -7
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Subtract(int a, int b)
    {
        // 从 a 中减去 b
        return a - b;
    }
}
```
