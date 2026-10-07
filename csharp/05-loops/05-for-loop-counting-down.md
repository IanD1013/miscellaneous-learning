### For 循环 - 递减计数

通过更改循环变量的递增/递减操作，for 循环可以朝任意方向计数。
倒数（递减计数）在倒计时、反向迭代以及需要从后往前处理元素的场景中非常有用。

### 使用 `i--` 递减

```csharp
// 递增计数：从小值开始，到大值结束，递增
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine(i);  // 打印：1, 2, 3, 4, 5
}

// 递减计数：从大值开始，到小值结束，递减
for (int i = 5; i >= 1; i--)
{
    Console.WriteLine(i);  // 打印：5, 4, 3, 2, 1
}
```

### 与递增计数的关键区别

| 递增计数 | 递减计数 |
| --- | --- |
| 从较小的值开始 | 从较大的值开始 |
| 条件：`i <= max` | 条件：`i >= min` |
| 递增：`i++` | 递减：`i--` |

### 递减变体

```csharp
// 每次减 1
for (int i = 10; i >= 1; i--)

// 每次减 2（倒序的偶数）
for (int i = 10; i >= 2; i -= 2)  // 10, 8, 6, 4, 2

// 每次减自定义的数量
for (int i = 100; i >= 0; i -= 10)  // 100, 90, 80, ..., 0
```

### 你的任务

编写一个方法，打印从 5 到 1 的倒计时。
每个数字应单独占一行。

### 方法签名

```csharp
public static void Countdown()
```

### 预期输出

```
5
4
3
2
1
```

### 解答

```csharp
using System;

public class Solution
{
    public static void Countdown()
    {
        // 从 5 递减到 1，每个数字占一行
        for (int i = 5; i >= 1; i--)
        {
            Console.WriteLine(i);
        }
    }
}
```
