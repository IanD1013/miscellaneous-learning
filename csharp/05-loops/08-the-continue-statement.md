### continue 语句

`continue` 语句会跳过当前循环迭代的剩余部分，并跳转到下一次迭代。
与完全退出循环的 `break` 不同，`continue` 只是进入下一个循环周期。

### 基本用法

```csharp
for (int i = 1; i <= 5; i++)
{
    if (i == 3)
    {
        continue; // 当 i 为 3 时跳过
    }
    Console.WriteLine(i);
}
// 输出：1, 2, 4, 5（跳过了 3）
```

### break 与 continue 对比

| 语句 | 行为 | 何时使用 |
| --- | --- | --- |
| `break` | 完全退出循环 | 已找到所需内容 |
| `continue` | 跳到下一次迭代 | 应忽略当前项 |

```csharp
// break 示例 - 在 3 处停止
for (int i = 1; i <= 5; i++)
{
    if (i == 3) break;
    Console.WriteLine(i);
}
// 输出：1, 2

// continue 示例 - 跳过 3
for (int i = 1; i <= 5; i++)
{
    if (i == 3) continue;
    Console.WriteLine(i);
}
// 输出：1, 2, 4, 5
```

### 检查倍数

使用取模运算符 `%` 来检查一个数是否是另一个数的倍数：

```csharp
if (number % 3 == 0)  // 如果 number 是 3 的倍数则为 True
```

### 你的任务

打印从 1 到 10 的数字，但跳过所有 3 的倍数（3、6、9）。
使用 `continue` 语句跳过这些数字。

### 预期输出

```
1
2
4
5
7
8
10
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintSkippingMultiplesOfThree()
    {
        // 打印 1 到 10，用 continue 跳过 3 的倍数
        for (int i = 1; i <= 10; i++)
        {
            if (i % 3 == 0)
            {
                continue;
            }
            Console.WriteLine(i);
        }
    }
}
```
