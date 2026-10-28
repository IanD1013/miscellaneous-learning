### 交错数组

交错数组（Jagged Array）是数组的数组，其中每个内部数组可以具有不同的长度，这与形成固定矩形网格的多维数组不同。

### 声明与初始化

```csharp
// 声明一个有 3 行的交错数组
int[][] jagged = new int[3][];

// 每一行都必须单独初始化
jagged[0] = new int[] { 1, 2 };       // 2 个元素
jagged[1] = new int[] { 3, 4, 5 };    // 3 个元素
jagged[2] = new int[] { 6 };          // 1 个元素

// 或者一次性全部初始化
int[][] numbers = new int[][]
{
    new int[] { 1, 2 },
    new int[] { 3, 4, 5 },
    new int[] { 6 }
};
```

### 访问元素

```csharp
int[][] data = new int[2][];
data[0] = new int[] { 10, 20, 30 };
data[1] = new int[] { 40, 50 };

int first = data[0][0];    // 10（第 0 行，第 0 列）
int last = data[1][1];     // 50（第 1 行，第 1 列）
int rowLength = data[0].Length;  // 3（第一行的长度）
```

### 交错数组对比多维数组

| 特性 | 交错数组 `int[][]` | 多维数组 `int[,]` |
| --- | --- | --- |
| 行长度 | 可以不同 | 所有行长度相同 |
| 内存 | 各行单独存储 | 单一连续内存块 |
| 使用场景 | 不规则数据（三角形、树等） | 网格、矩阵 |
| 访问方式 | `array[row][col]` | `array[row, col]` |

### 遍历交错数组

```csharp
int[][] jagged = new int[][] { new int[] { 1 }, new int[] { 2, 3 } };

for (int row = 0; row < jagged.Length; row++)
{
    for (int col = 0; col < jagged[row].Length; col++)
    {
        Console.Write(jagged[row][col] + " ");
    }
    Console.WriteLine();
}
// 输出：
// 1 
// 2 3
```

### 你的任务

创建一个表示 4 行三角形图案的交错数组：

- 第 0 行：包含 `[1]`
- 第 1 行：包含 `[1, 2]`
- 第 2 行：包含 `[1, 2, 3]`
- 第 3 行：包含 `[1, 2, 3, 4]`

将每行打印在单独的一行上，元素之间用空格分隔。

### 方法签名

```csharp
public static void PrintTriangle()
```

### 预期输出

```
1
1 2
1 2 3
1 2 3 4
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintTriangle()
    {
        // 创建一个有 4 行的交错数组，每行长度不同
        int[][] triangle = new int[][]
        {
            new int[] { 1 },
            new int[] { 1, 2 },
            new int[] { 1, 2, 3 },
            new int[] { 1, 2, 3, 4 }
        };

        for (int row = 0; row < triangle.Length; row++)
        {
            for (int col = 0; col < triangle[row].Length; col++)
            {
                // 只在元素之间加空格，避免行尾多出空格
                if (col > 0)
                {
                    Console.Write(" ");
                }
                Console.Write(triangle[row][col]);
            }
            // 每行结束后换行
            Console.WriteLine();
        }
    }
}
```
