### LINQ 序列处理管道

现实世界中的数据处理通常需要将多个操作链接在一起：过滤行、选择结果窗口、将它们分成批次，然后对每个批次进行汇总。
LINQ 提供了一个流畅的 API，其中每个方法都返回一个 `IEnumerable<T>`，让你可以用简单的构建块组合出复杂的管道。

本练习将四个关键的 LINQ 方法组合成一个管道：**Skip**、**Take**、**Chunk** 和 **Select**。

### 每个方法的工作原理

**Skip(n)** 跳过前 `n` 个元素并生成剩余元素。
可以把它看作是快进跳过你不需要的元素。

**Take(n)** 仅从接收到的序列中生成前 `n` 个元素。
它是你查看数据子集的窗口。

**Chunk(size)** 将序列分割为大小至多为 `size` 个元素的数组。
如果元素不能被整除，最后一个分块可能会更小。
它返回 `IEnumerable<T[]>`。

**Select** 转换每个元素。
当使用重载 `Select((element, index) => ...)` 时，你还可以访问每个元素从零开始的索引。

### 语法

```csharp
// Skip 和 Take 用于缩小序列范围
var window = source.Skip(n).Take(m);

// Chunk 用于拆分成批次
var batches = source.Chunk(batchSize); // IEnumerable<T[]>

// 带有索引的 Select 用于转换每个元素
var labels = source.Select((item, i) => $"Item {i}: {item}");
```

### 示例

```csharp
// 示例 1：使用 Skip 和 Take 获取一页结果
string[] cities = { "Oslo", "Berlin", "Tokyo", "Lima", "Cairo", "Delhi" };
var page2 = cities.Skip(3).Take(3);
// 结果: ["Lima", "Cairo", "Delhi"]

// 示例 2：Chunk 均匀拆分
int[] ids = { 10, 20, 30, 40, 50, 60 };
var batches = ids.Chunk(2);
// 结果: [[10, 20], [30, 40], [50, 60]]

// 示例 3：Chunk 拆分后有不均匀的余数
int[] vals = { 1, 2, 3, 4, 5 };
var groups = vals.Chunk(2);
// 结果: [[1, 2], [3, 4], [5]]

// 示例 4：带有索引的 Select 用于打标签
double[] scores = { 88.5, 92.0, 76.3 };
var report = scores.Select((s, i) => $"Student {i + 1}: {s}");
// 结果: ["Student 1: 88.5", "Student 2: 92", "Student 3: 76.3"]

// 示例 5：结合所有四种方法的完整管道
string[] words = { "a", "bb", "ccc", "dd", "eeeee", "ff", "g", "hh" };
var result = words
    .Skip(1)          // ["bb", "ccc", "dd", "eeeee", "ff", "g", "hh"]
    .Take(4)          // ["bb", "ccc", "dd", "eeeee"]
    .Chunk(2)         // [["bb", "ccc"], ["dd", "eeeee"]]
    .Select((chunk, i) => $"Group {i + 1}: {chunk.Sum(w => w.Length)}")
    .ToArray();
// 结果: ["Group 1: 5", "Group 2: 7"]
```

### 实用参考

| 方法 | 返回值 | 描述 |
| --- | --- | --- |
| `Skip(n)` | `IEnumerable<T>` | 跳过前 `n` 个元素 |
| `Take(n)` | `IEnumerable<T>` | 获取前 `n` 个元素 |
| `Chunk(size)` | `IEnumerable<T[]>` | 分割为大小至多为 `size` 的数组 |
| `Select((el, i) => ...)` | `IEnumerable<TResult>` | 带有索引的转换 |
| `Sum()` | `int` / `double` | 对数值元素求和 |
| `string.Join(sep, arr)` | `string` | 使用分隔符连接元素 |

### 你的任务

编写一个方法，通过多步管道处理整数数组：

1. **跳过（Skip）** 前 `skipCount` 个元素
2. **获取（Take）** 接下来的 `takeCount` 个元素
3. 将结果**分块（Chunk）** 为大小为 `chunkSize` 的组
4. 对每个分块**求和（Sum）**
5. 将每个分块**格式化（Format）** 为 `"Chunk N: S"`，其中 `N` 是从 1 开始的分块编号，`S` 是总和
6. 使用 `", "` **连接（Join）** 所有格式化后的字符串并返回结果

如果在跳过和获取之后没有剩余元素，则返回一个空字符串 `""`。

### 方法签名

```csharp
public static string SliceAndDice(int[] numbers, int skipCount, int takeCount, int chunkSize)
```

### 预期结果

```rust
SliceAndDice([1,2,3,4,5,6,7,8,9,10], 2, 6, 2) -> "Chunk 1: 7, Chunk 2: 11, Chunk 3: 15"
SliceAndDice([10,20,30,40,50], 1, 3, 2) -> "Chunk 1: 50, Chunk 2: 40"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string SliceAndDice(int[] numbers, int skipCount, int takeCount, int chunkSize)
    {
        // 跳过、获取、分块，然后把每个分块格式化为 "Chunk N: S"
        var parts = numbers
            .Skip(skipCount)
            .Take(takeCount)
            .Chunk(chunkSize)
            .Select((chunk, i) => $"Chunk {i + 1}: {chunk.Sum()}");

        // 使用 ", " 连接，没有元素时得到空字符串
        return string.Join(", ", parts);
    }
}
```
