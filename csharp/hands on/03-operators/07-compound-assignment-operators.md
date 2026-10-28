### 复合赋值运算符

复合赋值运算符将算术运算与赋值结合在一起。
当你想要基于变量自身的值来修改该变量时，它能让代码更加简洁。

### 标准赋值与复合赋值

```csharp
// 标准赋值 - 冗长
int score = 10;
score = score + 5;  // score 现在为 15

// 复合赋值 - 简洁
int score = 10;
score += 5;  // score 现在为 15（结果相同！）
```

### 四种算术复合运算符

```csharp
int x = 20;

x += 5;   // x = x + 5  → x 现在为 25
x -= 3;   // x = x - 3  → x 现在为 22
x *= 2;   // x = x * 2  → x 现在为 44
x /= 4;   // x = x / 4  → x 现在为 11
```

### 快速参考

| 运算符 | 含义 | 示例 | 结果（若 x = 10） |
| --- | --- | --- | --- |
| `+=` | 加后赋值 | `x += 3` | x 变为 13 |
| `-=` | 减后赋值 | `x -= 3` | x 变为 7 |
| `*=` | 乘后赋值 | `x *= 3` | x 变为 30 |
| `/=` | 除后赋值 | `x /= 2` | x 变为 5 |

### 你的任务

实现四个方法，每个方法使用不同的复合赋值运算符：

- `ApplyAdditionAssignment`：使用 `+=` 将 amount 加到 value 上
- `ApplySubtractionAssignment`：使用 `-=` 从 value 中减去 amount
- `ApplyMultiplicationAssignment`：使用 `*=` 将 value 乘以 amount
- `ApplyDivisionAssignment`：使用 `/=` 将 value 除以 amount

### 方法签名

```csharp
public static int ApplyAdditionAssignment(int value, int amount)
public static int ApplySubtractionAssignment(int value, int amount)
public static int ApplyMultiplicationAssignment(int value, int amount)
public static int ApplyDivisionAssignment(int value, int amount)
```

### 预期结果

```
ApplyAdditionAssignment(10, 5) -> 15
ApplySubtractionAssignment(20, 8) -> 12
ApplyMultiplicationAssignment(7, 3) -> 21
ApplyDivisionAssignment(100, 4) -> 25
```

### 解答

```csharp
using System;

public class Solution
{
    // 使用 += 将 amount 加到 value 上并返回结果
    public static int ApplyAdditionAssignment(int value, int amount)
    {
        value += amount;
        return value;
    }

    // 使用 -= 从 value 中减去 amount 并返回结果
    public static int ApplySubtractionAssignment(int value, int amount)
    {
        value -= amount;
        return value;
    }

    // 使用 *= 将 value 乘以 amount 并返回结果
    public static int ApplyMultiplicationAssignment(int value, int amount)
    {
        value *= amount;
        return value;
    }

    // 使用 /= 将 value 除以 amount 并返回结果
    public static int ApplyDivisionAssignment(int value, int amount)
    {
        value /= amount;
        return value;
    }
}
```
