### 取模运算符（Modulo Operator）

取模运算符（`%`）返回整数除法后的余数。
它在检查奇偶数、数值循环以及索引回绕等任务中至关重要。

### 基本用法

```csharp
int remainder = 17 % 5;  // 2（因为 17 = 5 * 3 + 2）
int noRemainder = 10 % 2; // 0（10 能被 2 整除）
int smallerDividend = 3 % 7; // 3（3 小于 7，所以余数为 3）
```

### 除法与取模

```csharp
// 除法告诉你除数能容纳多少次
int quotient = 17 / 5;   // 3

// 取模告诉你剩下多少
int remainder = 17 % 5;  // 2

// 两者共同满足：被除数 = (商 * 除数) + 余数
// 17 = (3 * 5) + 2 ✓
```

### 常见用例

| 模式 | 示例 | 结果 |
| --- | --- | --- |
| 检查是否为偶数 | `number % 2 == 0` | 如果为偶数则为 true |
| 检查是否为奇数 | `number % 2 != 0` | 如果为奇数则为 true |
| 获取最后一位数字 | `number % 10` | 个位数 |
| 回绕循环 | `index % arrayLength` | 在 0 到 length-1 之间循环 |

### 你的任务

实现一个方法，返回被除数除以除数后的余数。

### 方法签名

```csharp
public static int GetRemainder(int dividend, int divisor)
```

### 预期结果

```
GetRemainder(17, 5) -> 2
GetRemainder(10, 3) -> 1
GetRemainder(20, 4) -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetRemainder(int dividend, int divisor)
    {
        // 使用 % 运算符返回余数
        return dividend % divisor;
    }
}
```
