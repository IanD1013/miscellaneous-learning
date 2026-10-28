### 嵌套循环 (Nested Loops)

嵌套循环是指放置在另一个循环内部的循环。
外层循环每进行一次迭代，内层循环都会完整地执行其所有的迭代。

### 基本结构

```csharp
for (int outer = 1; outer <= 3; outer++)
{
    for (int inner = 1; inner <= 3; inner++)
    {
        Console.Write($"({outer},{inner}) ");
    }
    Console.WriteLine(); // 内层循环完成后换行
}
// 输出：
// (1,1) (1,2) (1,3)
// (2,1) (2,2) (2,3)
// (3,1) (3,2) (3,3)
```

### 嵌套循环的执行过程

1. 外层循环开始：`outer = 1`
2. 内层循环完整运行：`inner = 1, 2, 3`
3. 外层循环递增：`outer = 2`
4. 内层循环再次完整运行：`inner = 1, 2, 3`
5. 依此继续，直到外层循环结束

### 常见用途

| 模式 | 描述 |
| --- | --- |
| 网格/表格 | 处理行和列 |
| 矩阵 | 访问二维数据结构 |
| 图案打印 | 使用字符生成各种形状 |
| 元素比较 | 将每个元素与其他所有元素进行比较 |

### 你的任务

使用嵌套循环创建一个 3x3 的乘法表。
外层循环代表行号（1 到 3），内层循环代表列号（1 到 3）。

对于每个单元格，打印 `row * column` 的结果。
同一行中的各个数值之间用空格分隔，每行输出完成后换行。
注意：每行的最后一个数值后面不要打印空格。

### 方法签名

```csharp
public static void PrintMultiplicationTable()
```

### 预期输出

```
1 2 3
2 4 6
3 6 9
```

第 1 行：1×1=1, 1×2=2, 1×3=3
第 2 行：2×1=2, 2×2=4, 2×3=6
第 3 行：3×1=3, 3×2=6, 3×3=9

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintMultiplicationTable()
    {
        // 外层循环代表行号，内层循环代表列号
        for (int row = 1; row <= 3; row++)
        {
            for (int column = 1; column <= 3; column++)
            {
                Console.Write(row * column);
                // 只在数值之间打印空格，最后一个数值后面不打印
                if (column < 3)
                {
                    Console.Write(" ");
                }
            }
            // 每行输出完成后换行
            Console.WriteLine();
        }
    }
}
```
