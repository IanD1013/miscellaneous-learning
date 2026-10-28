### 乘法运算符

乘法运算符 `*` 将两个数字相乘。
每当你需要计算乘积、面积或按比例缩放数值时，都会用到它。

### 基本用法

```csharp
int product = 5 * 3;     // product = 15
int doubled = 7 * 2;     // doubled = 14
int scaled = 100 * 10;   // scaled = 1000
```

### 乘法与加法

加法是将数值组合在一起，而乘法则是将一个数值重复指定的次数：

```csharp
// 把 4 加三次
int sum = 4 + 4 + 4;      // sum = 12

// 用乘法更简短
int product = 4 * 3;      // product = 12
```

### 特殊情况

```csharp
int zero = 5 * 0;         // 任何数乘以零 = 0
int same = 8 * 1;         // 任何数乘以一 = 它本身（8）
int negative = 4 * -2;    // 正数乘以负数 = 负数（-8）
int positive = -3 * -3;   // 负数乘以负数 = 正数（9）
```

### 你的任务

实现 `Multiply` 方法，该方法接收两个整数，并使用 `*` 运算符返回它们的乘积。

### 方法签名

```csharp
public static int Multiply(int a, int b)
```

### 预期结果

```
Multiply(3, 4) -> 12
Multiply(7, 8) -> 56
Multiply(5, 0) -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Multiply(int a, int b)
    {
        // 使用 * 运算符返回两数之积
        return a * b;
    }
}
```
