### 使用 WithDegreeOfParallelism 控制并行度

当你使用 PLINQ (Parallel LINQ) 时，运行时会决定使用多少个线程，通常每个逻辑处理器对应一个线程。
这对于专用机器上的 CPU 密集型任务非常有用，但在生产环境中，你通常需要更精细的控制。
可能你的 Web 服务器需要保留一些核心来处理请求，或者 I/O 密集型管道可能会因为过多的并发连接而使数据库不堪重负。
`WithDegreeOfParallelism` 可以为你提供这种控制。

### 工作原理

对序列调用 `.AsParallel()` 可以启用后续 LINQ 操作符的并行执行。
默认情况下，PLINQ 最多可能使用 `Environment.ProcessorCount` 个线程。
当你链式调用 `.WithDegreeOfParallelism(n)` 时，你为查询设置了 `n` 个线程的**上限**。
如果运行时确定使用更少的线程更有效率，它仍可能使用更少的线程，但绝不会超过 `n`。

这只是一个**提示**（hint），而不是强制命令：PLINQ 的调度程序将其视为最大值。
该值必须在 1 到 512 之间（包含 1 和 512）。

### 语法

```csharp
source
    .AsParallel()
    .WithDegreeOfParallelism(maxThreads)
    .Where(predicate)
    .Select(transform)
    .ToList();
```

你可以将 `WithDegreeOfParallelism` 与任何其他 PLINQ 操作符结合使用：`Where`、`Select`、`OrderBy`、`Aggregate` 等等。

### 示例

```csharp
// 示例 1：计算偶数的平方时限制为 2 个线程
var evenSquares = Enumerable.Range(1, 1000)
    .AsParallel()
    .WithDegreeOfParallelism(2)
    .Where(x => x % 2 == 0)
    .Select(x => x * x)
    .ToArray();
// evenSquares 包含 [4, 16, 36, ...]（除非排序，否则无序）

// 示例 2：单线程并行查询（顺序执行但使用 PLINQ 基础设施）
var names = new[] { "Charlie", "Alice", "Bob" }
    .AsParallel()
    .WithDegreeOfParallelism(1)
    .OrderBy(n => n)
    .ToList();
// names: ["Alice", "Bob", "Charlie"]

// 示例 3：在受限并行度和排序下进行处理
var results = Enumerable.Range(-50, 100)
    .AsParallel()
    .WithDegreeOfParallelism(4)
    .Where(x => x > 0 && x % 3 == 0)
    .OrderBy(x => x)
    .ToArray();
// results: [3, 6, 9, 12, ..., 48]
```

### 常见模式

| 场景 | 建议并行度 | 原因 |
| --- | --- | --- |
| CPU 密集型，专用机器 | `Environment.ProcessorCount`（默认） | 最大化吞吐量 |
| CPU 密集型，共享服务器 | `ProcessorCount / 2` 或更低 | 为其他服务保留核心 |
| I/O 密集型（数据库、HTTP） | 2–8，取决于目标资源 | 避免使资源过载 |
| 调试 / 确定性测试 | 1 | 更容易理清顺序 |

### 关于排序的重要说明

PLINQ 默认**不会**保留源序列的顺序。
如果你需要排序后的输出，必须显式使用 `.OrderBy()`（或使用 `.AsOrdered()` 来保留输入顺序）。
在本练习中，你需要**升序**排列的输出结果。

### 你的任务

编写一个方法，接收一个整数数组和最大并行度。
该方法应：

1. 使用具有指定并行度的 PLINQ
2. 过滤并仅保留**正数**（严格大于零）
3. 将结果按**升序**排序并作为 `int[]` 返回

处理边界情况：输入数组可能为空、不包含任何正数，或者完全由正数组成。

### 方法签名

```csharp
public static int[] BoundedParallelFilter(int[] numbers, int maxDegree)
```

### 预期结果

```scss
BoundedParallelFilter([-1, 2, -3, 4, -5, 6], 2) -> [2, 4, 6]
BoundedParallelFilter([10, 3, 7, 1, 5], 1)       -> [1, 3, 5, 7, 10]
BoundedParallelFilter([-1, -2, -3], 4)            -> []
BoundedParallelFilter([], 2)                      -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] BoundedParallelFilter(int[] numbers, int maxDegree)
    {
        // 限制并行度，只保留正数，再按升序排序
        return numbers
            .AsParallel()
            .WithDegreeOfParallelism(maxDegree)
            .Where(n => n > 0)
            .OrderBy(n => n)
            .ToArray();
    }
}
```
