### break 语句

`break` 语句会立即退出当前循环，停止所有后续迭代。
当您已经找到了想要的内容并且不需要继续搜索时，请使用它。

### 基本用法

```csharp
for (int i = 1; i <= 10; i++)
{
    if (i == 5)
    {
        break; // 当 i 等于 5 时退出循环
    }
    Console.WriteLine(i);
}
// 打印：1, 2, 3, 4（在打印 5 之前停止）
```

### 查找第一个匹配项

```csharp
int[] numbers = { 3, 8, 15, 22, 7 };
foreach (int num in numbers)
{
    if (num > 10)
    {
        Console.WriteLine($"First number over 10: {num}");
        break; // 找到第一个匹配项后停止搜索
    }
}
// 打印：First number over 10: 15
```

### 为什么使用 break？

| 场景 | 不使用 break | 使用 break |
| --- | --- | --- |
| 查找第一个匹配项 | 检查所有项 | 在第一个匹配项处停止 |
| 循环迭代次数 | 全部 100 次 | 仅直到找到为止 |
| 效率 | 浪费时间 | 更高效 |

### 整除检查

要检查一个数是否能被另一个数整除，请使用取模运算符 `%`。
如果 `a % b == 0`，则表示 `a` 能被 `b` 整除。

```csharp
14 % 7 == 0  // True - 14 能被 7 整除
15 % 7 == 0  // False - 15 不能被 7 整除
```

### 你的任务

编写一个方法，查找 1 到 100（含）之间**第一个**能被 7 整除的数字。
打印该数字并使用 `break` 立即退出循环。

### 方法签名

```csharp
public static void FindFirstDivisibleBySeven()
```

### 预期结果

```
FindFirstDivisibleBySeven() 打印：7
```

### 解答

```csharp
using System;

public class Solution
{
    public static void FindFirstDivisibleBySeven()
    {
        // 使用 for 循环从 1 迭代到 100
        for (int i = 1; i <= 100; i++)
        {
            // 找到第一个能被 7 整除的数字，打印后立即用 break 退出循环
            if (i % 7 == 0)
            {
                Console.WriteLine(i);
                break;
            }
        }
    }
}
```
