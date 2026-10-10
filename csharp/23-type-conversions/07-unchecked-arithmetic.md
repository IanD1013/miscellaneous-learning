### Unchecked 算术运算

默认情况下，C# 允许整数溢出并静默回绕（wrap around）。
`unchecked` 关键字可以显式允许此行为，即使项目在全局启用了溢出检查。

### 默认行为与 Unchecked

```csharp
// 默认情况下两者产生相同的结果
int result1 = int.MaxValue + 1;           // 回绕为 int.MinValue

unchecked
{
    int result2 = int.MaxValue + 1;       // 同样回绕为 int.MinValue
}
```

### 为什么使用 Unchecked？

```csharp
// 1. 可以接受溢出的性能关键代码
unchecked
{
    int hash = value1 * 31 + value2;     // 哈希计算经常会溢出
}

// 2. 当项目设置了 <CheckForOverflowUnderflow>true</CheckForOverflowUnderflow> 时
// unchecked 块会覆盖全局设置
```

### 回绕行为

```csharp
unchecked
{
    int max = int.MaxValue;       // 2147483647
    int overflow = max + 1;       // -2147483648（回绕为 int.MinValue）
    
    int min = int.MinValue;       // -2147483648
    int underflow = min - 1;      // 2147483647（回绕为 int.MaxValue）
}
```

### Checked 与 Unchecked 对比

| 关键字 | 溢出行为 | 使用场景 |
| --- | --- | --- |
| checked | 抛出 OverflowException | 财务计算、关键数据 |
| unchecked | 静默回绕 | 哈希函数、位操作 |

### 你的任务

编写一个使用 `unchecked` 块将两个整数相加的方法，允许溢出时发生回绕而不抛出异常。

### 方法签名

```csharp
public static int UncheckedAdd(int a, int b)
```

### 预期结果

```
UncheckedAdd(5, 3) -> 8
UncheckedAdd(int.MaxValue, 1) -> -2147483648
UncheckedAdd(int.MinValue, -1) -> 2147483647
```

### 解答

```csharp
using System;

public class Solution
{
    public static int UncheckedAdd(int a, int b)
    {
        // 在 unchecked 块中相加，溢出时静默回绕
        unchecked
        {
            return a + b;
        }
    }
}
```
