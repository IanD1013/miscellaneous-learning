### LINQ 综合练习：GroupBy、Count、MinBy 与 MaxBy

在实际的数据分析中，经常需要对记录进行分组，然后从每个组中提取汇总统计数据。
例如销售仪表盘按地区对交易进行分组，并显示每个地区的最高销售额、最低销售额以及总交易数。
LINQ 为此提供了强大的流水线：使用 **GroupBy** 划分数据，使用 **Count** 统计项目数量，使用 **MinBy / MaxBy** 查找每个分区内的极值。

本练习将所有这四个操作合并到一个流畅的流水线中。

### 工作原理

**GroupBy** 根据键选择器将序列拆分为多个组。
每个组都是一个 `IGrouping<TKey, TElement>`，其行为类似于带有键的集合，你可以对其进行进一步查询。

**Count()** 返回组（或任何序列）中的元素数量。

**MaxBy(selector)** 和 **MinBy(selector)**（在 .NET 6 中引入）返回根据投影具有最大或最小值的*元素*，而不是投影值本身。
当多个元素具有相同的极值时，返回首次出现的元素。

### 语法

```csharp
// GroupBy 返回 IEnumerable<IGrouping<TKey, TElement>>
var groups = items.GroupBy(item => item.SomeProperty);

foreach (var group in groups)
{
    var key = group.Key;           // 分组键
    var count = group.Count();     // 共享该键的项数量
    var best = group.MaxBy(x => x.Score);   // Score 最高的元素
    var worst = group.MinBy(x => x.Score);  // Score 最低的元素
}
```

### 示例

```csharp
// 示例 1：按偶数/奇数对数字分组并找出极值
int[] nums = { 3, 8, 1, 4, 7, 2 };
var summary = nums.GroupBy(n => n % 2 == 0 ? "Even" : "Odd")
    .Select(g => $"{g.Key}: Count={g.Count()}, Max={g.MaxBy(n => n)}, Min={g.MinBy(n => n)}");
// "Even: Count=3, Max=8, Min=2"
// "Odd: Count=3, Max=7, Min=1"

// 示例 2：按部门对员工分组
var employees = new[] {
    new { Name = "Alice", Dept = "Eng", Salary = 95000 },
    new { Name = "Bob", Dept = "Eng", Salary = 110000 },
    new { Name = "Carol", Dept = "HR", Salary = 72000 }
};
var deptStats = employees.GroupBy(e => e.Dept)
    .Select(g => $"{g.Key}: {g.Count()} people, top earner={g.MaxBy(e => e.Salary).Name}");
// "Eng: 2 people, top earner=Bob"
// "HR: 1 people, top earner=Carol"

// 示例 3：平局处理 - MinBy/MaxBy 在值相同时返回首次出现的元素
var names = new[] { "cat", "car", "cup" };
var shortest = names.MinBy(n => n.Length); // "cat"（长度都是 3，第一个胜出）
```

### 对分组排序

在 `GroupBy` 之后，使用 `OrderBy(g => g.Key)` 在投影结果之前按键对各组进行字母或数字升序排序。

### 实用参考

| 方法 | 返回值 | 描述 |
| --- | --- | --- |
| `GroupBy(keySelector)` | `IEnumerable<IGrouping<K,T>>` | 按键对元素进行分区 |
| `group.Key` | `K` | 该组共享的键 |
| `group.Count()` | `int` | 组中的元素数量 |
| `group.MaxBy(selector)` | `T` | 具有最大投影值的元素 |
| `group.MinBy(selector)` | `T` | 具有最小投影值的元素 |
| `OrderBy(selector)` | 有序序列 | 升序排序 |
| `char.ToLower(c)` | `char` | 将字符转换为小写 |

### 你的任务

编写一个方法，接收一个单词数组，按其**首字母**（转换为小写）进行分组，并为每个组生成一个严格符合以下格式的汇总字符串：

```makefile
K: Count=N, Longest=W, Shortest=W
```

其中：

- **K** 是该组的小写首字母
- **N** 是该组中的单词数量
- **Longest** 是字符数最多的单词（若长度相同，取首次出现的单词）
- **Shortest** 是字符数最少的单词（若长度相同，取首次出现的单词）

将结果作为按键字符字母顺序排序的 `string[]` 返回。

### 方法签名

```csharp
public static string[] SummarizeGroups(string[] words)
```

### 预期结果

```rust
SummarizeGroups(["apple", "avocado", "banana", "cherry", "apricot"])
  -> ["a: Count=3, Longest=avocado, Shortest=apple",
      "b: Count=1, Longest=banana, Shortest=banana",
      "c: Count=1, Longest=cherry, Shortest=cherry"]

SummarizeGroups(["dog", "deer", "dove", "duck"])
  -> ["d: Count=4, Longest=deer, Shortest=dog"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] SummarizeGroups(string[] words)
    {
        // 按小写首字母分组并按键排序，MaxBy/MinBy 在长度相同时取首次出现的单词
        return words
            .GroupBy(w => char.ToLower(w[0]))
            .OrderBy(g => g.Key)
            .Select(g => $"{g.Key}: Count={g.Count()}, Longest={g.MaxBy(w => w.Length)}, Shortest={g.MinBy(w => w.Length)}")
            .ToArray();
    }
}
```
