### Chunk 操作符

从 .NET 6 开始，LINQ 包含了 `Chunk` 方法，这是一种将序列拆分为指定大小的较小组的便捷方法。
每当您需要分批处理数据时（例如对结果进行分页、在固定大小的 API 请求中发送项或跨并行任务分配工作），这都非常有用。

### 工作原理

`Chunk(size)` 遍历源序列并将连续的元素分组为最多包含 `size` 个元素的数组。
如果元素总数不能被块大小整除，则最后一个数组将仅包含剩余的元素。
该方法是延迟执行的（lazy），它在您枚举时一次生成（yield）一个块。

### 语法

```csharp
IEnumerable<T[]> Chunk<T>(int size)
```

参数 `size` 必须是一个正整数。
每个生成的元素都是一个最多包含 `size` 个项的 `T[]`。

### 示例

```csharp
// 将字母拆分为每组 2 个
char[] letters = { 'A', 'B', 'C', 'D', 'E' };
var groups = letters.Chunk(2);
// groups：['A','B'], ['C','D'], ['E']

// 将姓名分批为每组 3 个
string[] names = { "Ana", "Ben", "Cal", "Dee", "Eve", "Fay", "Gus" };
var batches = names.Chunk(3);
// batches：["Ana","Ben","Cal"], ["Dee","Eve","Fay"], ["Gus"]

// 将 Chunk 与 Select 结合，转换每个组
double[] prices = { 10.0, 20.0, 30.0, 40.0 };
var maxPerGroup = prices.Chunk(2).Select(g => g.Max()).ToArray();
// maxPerGroup：[20.0, 40.0]
```

注意在最后一个示例中，`Chunk` 是如何自然地与 `Select` 结合使用的，先将数据拆分为组，然后独立地对每个组应用聚合或转换。

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `.Chunk(n).Select(g => g.Length)` | 获取每个块的大小 |
| `.Chunk(n).Select(g => g.Average())` | 每个块的平均值 |
| `.Chunk(n).Select(g => g.Min())` | 每个块的最小值 |
| `.Chunk(n).Select(g => string.Join(", ", g))` | 将每个块连接成一个字符串 |
| `.Chunk(n).Count()` | 计算块的总数 |

### 您的任务

编写一个方法，接收一个整数数组和一个块大小，使用 `Chunk` 操作符将数组拆分成块，计算每个块的**总和**，并将这些总和作为 `int[]` 返回。

例如，给定 `[10, 20, 30, 40, 50]` 且块大小为 `2`，块分别为 `[10, 20]`、`[30, 40]` 和 `[50]`，生成的总和为 `[30, 70, 50]`。

### 方法签名

```csharp
public static int[] ChunkSum(int[] numbers, int size)
```

### 预期结果

```scss
ChunkSum([1, 2, 3, 4, 5, 6, 7], 3) -> [6, 15, 7]
ChunkSum([10, 20, 30, 40, 50], 2) -> [30, 70, 50]
ChunkSum([5], 1) -> [5]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ChunkSum(int[] numbers, int size)
    {
        // 将数组拆分成块，并计算每个块的总和
        return numbers.Chunk(size).Select(chunk => chunk.Sum()).ToArray();
    }
}
```
