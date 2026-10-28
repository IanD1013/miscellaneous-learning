### AsOrdered：在 PLINQ 中保持源顺序

当你使用 `AsParallel()` 来并行化 LINQ 查询时，运行时会将你的数据划分到多个线程中以加快处理速度。
然而，由于各个线程完成工作的速度不同，**输出顺序会变得不确定**，结果可能以任意顺序返回。
这对于像 `Sum()` 或 `Count()` 这样的聚合操作完全没有问题，但当元素的相对位置很重要时（例如渲染排序列表或维护时间序列顺序），这就会成为一个问题。

`AsOrdered()` 告诉 PLINQ 引擎：“进行并行处理，但要**保证**输出遵循原始源顺序。”
运行时会在后台跟踪每个元素的索引，并在生成结果之前将它们按正确顺序重新组装。
由于记录和合并操作的存在，这会引入少量的开销，但结果是确定且有序的。

### 工作原理

如果没有 `AsOrdered()`，PLINQ 将使用无序合并：哪个分区先完成，就先输出哪个分区的结果。
有了 `AsOrdered()`，引擎会缓冲分区结果，并且仅在能够保证顺序时才输出它们。
你可以把它想象成邮局分拣中心：信件同时从多辆卡车（线程）运达，但它们完全按照邮政编码（源索引）放入邮箱（输出）。

重要提示：`AsOrdered()` 必须**紧跟在** `AsParallel()` 之后链式调用。
将其放置在管道的后续位置将不会起作用。

### 语法

```csharp
// 通用模式
var result = source
    .AsParallel()
    .AsOrdered()        // 保留元素的原始顺序
    .SomeLinqOperator()  // Select、Where 等
    .ToArray();          // 或 ToList() 等
```

### 示例

```csharp
// 示例 1：有序并行 Select - 转换每个值，保持源顺序
string[] cities = { "Tokyo", "Berlin", "Cairo", "Lima" };
string[] upper = cities
    .AsParallel()
    .AsOrdered()
    .Select(c => c.ToUpper())
    .ToArray();
// upper 始终为：["TOKYO", "BERLIN", "CAIRO", "LIMA"]

// 示例 2：不使用 AsOrdered - 不保证顺序
string[] unordered = cities
    .AsParallel()
    .Select(c => c.ToUpper())
    .ToArray();
// 可能是 ["CAIRO", "TOKYO", "LIMA", "BERLIN"] 或任意排列

// 示例 3：有序过滤 - 移除短名称，保持相对顺序
string[] names = { "Al", "Catherine", "Bo", "Elizabeth", "Jo" };
string[] longNames = names
    .AsParallel()
    .AsOrdered()
    .Where(n => n.Length > 2)
    .ToArray();
// 始终为：["Catherine", "Elizabeth"]
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `.AsParallel().AsOrdered().Where(...)` | 并行过滤，有序结果 |
| `.AsParallel().AsOrdered().Select(...)` | 并行转换，有序结果 |
| `.AsParallel().AsOrdered().Take(n)` | 从有序并行流中获取前 N 个元素 |
| `.AsParallel().AsUnordered()` | 显式放弃顺序（默认行为） |

### 性能考量

`AsOrdered()` 并不是没有代价的。
运行时必须缓冲并排序结果，这会消耗额外的内存和同步开销。
仅在顺序确实很重要时才使用它。
如果你只需要一个聚合操作（sum、count、any 等），请省略 `AsOrdered()` 以获得更好的吞吐量。

### 你的任务

编写一个方法，该方法接收一个整数数组，并返回一个仅包含**偶数**的新数组，同时保持它们的**原始源顺序**。
过滤操作必须使用 PLINQ 并行执行，并保持顺序。

例如，给定 `[9, 4, 7, 2, 11, 6]`，按源顺序排列的偶数为 `[4, 2, 6]`。

### 方法签名

```csharp
public static int[] ParallelFilterOrdered(int[] numbers)
```

### 预期结果

```scss
ParallelFilterOrdered([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]
ParallelFilterOrdered([10, 3, 8, 1, 6]) -> [10, 8, 6]
ParallelFilterOrdered([7, 9, 11]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ParallelFilterOrdered(int[] numbers)
    {
        // AsOrdered 紧跟 AsParallel，并行过滤偶数并保持源顺序
        return numbers
            .AsParallel()
            .AsOrdered()
            .Where(n => n % 2 == 0)
            .ToArray();
    }
}
```
