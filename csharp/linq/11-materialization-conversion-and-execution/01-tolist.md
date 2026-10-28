### ToList - 主要的物化操作符

在 LINQ 中，大多数查询操作符（如 `Where`、`Select` 和 `OrderBy`）都采用**延迟执行**（deferred execution）：它们在您遍历结果之前并不会实际处理数据。
这意味着每次枚举查询时（例如在 `foreach` 循环中或通过调用 `.Count()`），整个管道都会从头重新运行。
`ToList()` 是**物化**（materialize）查询最常用的方式：它会强制立即执行并将所有结果存储在一个具体的 `List<T>` 中。

在以下情况下，这至关重要：

- **复用**查询结果而无需重新执行管道
- **修改**结果（添加、删除或修改元素）
- **通过索引访问元素**（例如 `result[0]`）
- 将结果传递给期望接收 `List<T>` 而非 `IEnumerable<T>` 的代码

### 运作原理

当您在任何 `IEnumerable<T>` 上调用 `ToList()` 时，LINQ 会完整遍历一次序列，对每个元素进行求值，并将它们复制到一个新的 `List<T>` 中。
物化之后，该列表完全独立于原始数据源：对列表的更改不会影响数据源，对数据源的更改也不会影响列表。

因为 `List<T>` 实现了 `IList<T>`，所以您将获得普通 `IEnumerable<T>` 所不具备的功能：索引访问、`.Add()`、`.Remove()`、`.Insert()`、作为属性（而不是重新枚举的方法）的 `.Count` 等等。

### 语法

```csharp
// 通用模式：链式调用 LINQ 操作符，然后物化
List<T> result = source
    .Where(predicate)
    .Select(transform)
    .ToList();

// 现在 'result' 是一个具体的 List<T>，可以复用和修改
result.Add(newItem);
result.RemoveAt(0);
int count = result.Count; // 不会重新枚举
```

### 示例

```csharp
// 示例 1：物化过滤后的字符串并添加一个元素
string[] words = { "cat", "elephant", "dog", "butterfly" };
List<string> longWords = words.Where(w => w.Length > 3).ToList();
// longWords 为 ["elephant", "butterfly"] - 一个真正的 List<string>
longWords.Add("giraffe");
// longWords 现在为 ["elephant", "butterfly", "giraffe"]

// 示例 2：复用已物化的查询进行多个操作
double[] temps = { 36.5, 38.1, 37.0, 39.2, 36.8 };
List<double> fevers = temps.Where(t => t >= 38.0).ToList();
double avg = fevers.Average();  // 使用该列表 - 不会重新过滤
double max = fevers.Max();       // 再次复用同一个列表

// 示例 3：物化后的索引访问
int[] scores = { 90, 45, 78, 62, 88 };
List<int> passing = scores.Where(s => s >= 60).ToList();
int first = passing[0];   // 90 - 索引访问可用
int last = passing[passing.Count - 1]; // 88
```

### 延迟执行 vs. 立即执行

| 操作 | 执行类型 | 返回值 |
| --- | --- | --- |
| `.Where()` | 延迟执行 | `IEnumerable<T>` |
| `.Select()` | 延迟执行 | `IEnumerable<T>` |
| `.OrderBy()` | 延迟执行 | `IOrderedEnumerable<T>` |
| **`.ToList()`** | **立即执行** | **`List<T>`** |
| `.ToArray()` | 立即执行 | `T[]` |
| `.Count()` | 立即执行 | `int` |
| `.Sum()` | 立即执行 | 数值类型 |

### 您的任务

编写一个方法，接收一个整数数组，仅过滤出**正数**（大于零），将结果物化为 `List<int>`，计算该列表的**总和**，将总和**追加**到列表末尾，最后将列表作为 `int[]` 返回。

例如，给定 `[1, -2, 3, -4, 5]`：

1. 过滤正数 → `[1, 3, 5]`
2. 物化为 `List<int>`
3. 计算总和 → `1 + 3 + 5 = 9`
4. 将总和添加到列表 → `[1, 3, 5, 9]`
5. 作为 `int[]` 返回

### 方法签名

```csharp
public static int[] MaterializeAndModify(int[] numbers)
```

### 预期结果

```scss
MaterializeAndModify([1, -2, 3, -4, 5]) -> [1, 3, 5, 9]
MaterializeAndModify([10, 20, 30])       -> [10, 20, 30, 60]
MaterializeAndModify([-1, -2, -3])       -> [0]
MaterializeAndModify([])                 -> [0]
```

### 解答

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

public class Solution
{
    public static int[] MaterializeAndModify(int[] numbers)
    {
        // 过滤出正数并物化为 List<int>
        List<int> positives = numbers.Where(n => n > 0).ToList();

        // 计算总和并追加到列表末尾
        int sum = positives.Sum();
        positives.Add(sum);

        // 作为 int[] 返回
        return positives.ToArray();
    }
}
```
