### PLINQ 与 AsParallel 操作符

Parallel LINQ (PLINQ) 是 LINQ to Objects 的并行实现，能够在多个 CPU 核心上并发执行查询操作。
当您拥有一个大型集合且每个元素都可以独立处理时，PLINQ 可以通过自动将工作分配到多个线程来显著减少总计算时间。
您无需自行管理线程、分区或同步 - 运行时会自动处理这些。

### 工作原理

在任何 `IEnumerable<T>` 上调用 `.AsParallel()` 会将其转换为 `ParallelQuery<T>`。
这会向 PLINQ 引擎发出信号以执行以下操作：

1. **分区**（Partition）：将源序列拆分为多个数据块
2. **分配**（Assign）：将每个数据块分配给线程池中的工作线程
3. **执行**（Execute）：在这些线程中并行执行所有链式 LINQ 操作符（Select、Where 等）
4. **合并**（Merge）：将局部结果合并回单个输出序列

这意味着在 `AsParallel()` 之后链式调用的任何标准 LINQ 操作符，例如 `Select`、`Where`、`Aggregate`，都无需编写任何额外代码即可并行运行。

⚠️ **不保证顺序！**
由于分区是并发执行的，输出中的元素可能会以任意顺序到达。
如果您需要保留原始输入的顺序，必须在 `.AsParallel()` 之后显式调用 `.AsOrdered()`。
或者，您可以使用 `OrderBy` 对最终结果进行排序。

### 语法

```csharp
// 转换为并行查询
IEnumerable<T> source = ...;
ParallelQuery<T> parallel = source.AsParallel();

// 链式调用操作符 - 它们并行运行
var result = source
    .AsParallel()
    .Where(x => /* 过滤 */)
    .Select(x => /* 转换 */)
    .ToArray();

// 保留原始顺序（有一定开销）
var ordered = source
    .AsParallel()
    .AsOrdered()
    .Select(x => /* 转换 */)
    .ToArray();
```

### 示例

```csharp
// 示例 1：对大型数据集进行并行过滤
double[] temperatures = GetSensorReadings(); // 数百万条读数
double[] aboveThreshold = temperatures
    .AsParallel()
    .Where(t => t > 100.0)
    .ToArray();
// 同时在所有 CPU 核心上进行过滤

// 示例 2：并行字符串转换并排序
string[] words = { "banana", "apple", "cherry", "date" };
string[] uppercaseSorted = words
    .AsParallel()
    .Select(w => w.ToUpper())
    .OrderBy(w => w)
    .ToArray();
// 结果：["APPLE", "BANANA", "CHERRY", "DATE"]
// 无论线程执行顺序如何，OrderBy 都能确保确定性的输出

// 示例 3：并行聚合
int[] sales = { 120, 340, 560, 210, 780, 90 };
int totalAbove200 = sales
    .AsParallel()
    .Where(s => s > 200)
    .Sum();
// 结果：1890
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `.AsParallel().Select(...)` | 并行转换每个元素 |
| `.AsParallel().Where(...)` | 并行过滤元素 |
| `.AsParallel().AsOrdered().Select(...)` | 并行转换并保留输入顺序 |
| `.AsParallel().Select(...).OrderBy(...)` | 并行转换，然后对结果排序 |
| `.AsParallel().Aggregate(...)` | 并行规约 / 折叠 |

### 重要注意事项

- PLINQ 在处理大型集合上的 **CPU 密集型**（CPU-bound）任务时表现优异。
  对于小型集合或 I/O 密集型任务，分区和合并带来的开销可能会超过其带来的收益。
- 传递给并行操作符的 lambda 表达式应保持**无副作用**：避免在没有同步的情况下修改共享状态。
- 在 `AsParallel()` 之后使用 `OrderBy` 会对合并后的输出进行排序，无论哪个线程先完成，都能产生确定性的结果。

### 你的任务

编写一个方法，接收一个整数数组，使用并行处理对每个元素求平方，并将平方后的值按升序排序作为 `int[]` 返回。

该方法必须使用 `AsParallel()` 启用并行执行，使用 `Select` 计算平方，并使用 `OrderBy` 确保确定性的排序输出。

### 方法签名

```csharp
public static int[] ParallelSquares(int[] numbers)
```

### 预期结果

```scss
ParallelSquares([1, 2, 3, 4, 5]) -> [1, 4, 9, 16, 25]
ParallelSquares([5, 3, 1]) -> [1, 9, 25]
ParallelSquares([-2, 0, 2]) -> [0, 4, 4]
ParallelSquares([10]) -> [100]
ParallelSquares([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ParallelSquares(int[] numbers)
    {
        // 并行求平方，再用 OrderBy 得到确定性的升序结果
        return numbers
            .AsParallel()
            .Select(n => n * n)
            .OrderBy(n => n)
            .ToArray();
    }
}
```
