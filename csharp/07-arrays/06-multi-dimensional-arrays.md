### 二维数组

二维数组（2D array）以包含行和列的网格格式存储数据，非常适合用于表示表格、游戏棋盘或矩阵。

### 声明与创建

```csharp
// 声明一个 3 行 4 列的二维数组
int[,] matrix = new int[3, 4];

// 声明并用值初始化
int[,] grid = {
    { 1, 2, 3 },
    { 4, 5, 6 },
    { 7, 8, 9 }
};
```

### 访问元素

使用 `[row, col]` 语法来访问或修改元素：

```csharp
int[,] board = new int[3, 3];

// 设置第 0 行第 1 列的值
board[0, 1] = 5;

// 获取第 2 行第 2 列的值
int value = board[2, 2];
```

### 遍历二维数组

使用嵌套循环，外层循环遍历行，内层循环遍历列：

```csharp
int[,] data = new int[2, 3];

for (int row = 0; row < 2; row++)
{
    for (int col = 0; col < 3; col++)
    {
        Console.WriteLine(data[row, col]);
    }
}
```

### 常用属性

| 属性 | 描述 | 示例 |
| --- | --- | --- |
| `GetLength(0)` | 行数 | `grid.GetLength(0)` |
| `GetLength(1)` | 列数 | `grid.GetLength(1)` |
| `Length` | 元素总数 | `grid.Length` |

### 你的任务

创建一个 3x3 的二维数组，并用 1 到 9 的值填充它（逐行、从左到右）。
然后将每个值单独打印在一行上。

### 方法签名

```csharp
public static void PrintGrid()
```

### 预期输出

```
1
2
3
4
5
6
7
8
9
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintGrid()
    {
        // 创建一个 3x3 的二维数组，并逐行填充 1 到 9
        int[,] grid = {
            { 1, 2, 3 },
            { 4, 5, 6 },
            { 7, 8, 9 }
        };

        // 外层循环遍历行，内层循环遍历列，每个值各占一行
        for (int row = 0; row < grid.GetLength(0); row++)
        {
            for (int col = 0; col < grid.GetLength(1); col++)
            {
                Console.WriteLine(grid[row, col]);
            }
        }
    }
}
```
