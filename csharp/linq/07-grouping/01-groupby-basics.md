### LINQ GroupBy - 按键划分序列

在实际应用程序中，你经常需要对数据进行分类：按状态划分订单、按部门划分员工、按严重程度划分日志条目。
LINQ 的 `GroupBy` 运算符允许你根据定义的键将序列划分为不同的组，从而使你可以对每个组单独进行聚合、计数或转换。

### 工作原理

`GroupBy` 会遍历序列中的每个元素，对每个元素计算**键选择器**（key selector）函数，并将该元素放入由此键标识的存储桶（bucket）中。
其结果是一个 `IGrouping<TKey, TElement>` 对象序列。
每个 `IGrouping` 包含：

- **`Key`** - 该组中所有元素所共有的共享值。
- 分组本身是一个 `IEnumerable<TElement>` - 你可以遍历其成员、对它们进行计数、对属性求和或将它们投影为新的形式。

需要注意的是，`GroupBy` 采用**延迟执行**（deferred execution）。
在枚举结果（例如使用 `foreach`、`ToArray()` 或 `ToList()`）之前，分组不会具体化。

### 语法

```csharp
// 基本分组
IEnumerable<IGrouping<TKey, TElement>> groups = source.GroupBy(element => keySelector);

// 遍历分组
foreach (var group in groups)
{
    Console.WriteLine(group.Key);        // 共享键
    Console.WriteLine(group.Count());    // 共享该键的元素数量
}
```

### 示例

假设你有一个订单列表，并且想要查看每个状态下的订单数量：

```csharp
var orders = new[] { "Shipped", "Pending", "Shipped", "Cancelled", "Pending", "Pending" };

var grouped = orders.GroupBy(o => o);
// grouped 包含 3 个组：
//   Key="Shipped"   -> 2 个元素
//   Key="Pending"   -> 3 个元素
//   Key="Cancelled" -> 1 个元素
```

你可以将每个组投影为汇总字符串：

```csharp
var temperatures = new[] { 18, 22, 35, 28, 15, 31 };

var buckets = temperatures
    .GroupBy(t => t >= 30 ? "Hot" : t >= 20 ? "Warm" : "Cool")
    .Select(g => $"{g.Key}: {g.Count()} readings")
    .ToArray();
// 可能生成：["Warm: 2 readings", "Hot: 2 readings", "Cool: 2 readings"]
```

请注意，`GroupBy` 保留了每个键首次出现的顺序。
如果你需要按字母或数字排序，可以在分组后链式调用 `.OrderBy()`。

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 每组计数 | `g.Count()` |
| 每组求和 | `g.Sum(x => x.Amount)` |
| 列出每组的项 | `g.ToList()` |
| 按键对组排序 | `.OrderBy(g => g.Key)` |
| 按计算出的键分组 | `.GroupBy(x => x.Name.Length)` |

### 你的任务

编写一个方法，接收一个单词数组并按它们的**首字符**进行分组（不区分大小写，输出为小写）。
对于每个组，生成一个格式为 `"char: count"` 的字符串，其中 `char` 是小写的首字母，`count` 是以该字母开头的单词数量。
将结果作为按字符字母顺序排序的 `string[]` 返回。

### 方法签名

```csharp
public static string[] CountByFirstChar(string[] words)
```

### 预期结果

```css
CountByFirstChar(["apple", "avocado", "banana", "blueberry", "cherry"]) -> ["a: 2", "b: 2", "c: 1"]
CountByFirstChar(["Dog", "deer", "Cat"]) -> ["c: 1", "d: 2"]
CountByFirstChar(["zebra"]) -> ["z: 1"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] CountByFirstChar(string[] words)
    {
        // 按小写首字母分组，按键排序后格式化为 "char: count"
        return words
            .GroupBy(w => char.ToLower(w[0]))
            .OrderBy(g => g.Key)
            .Select(g => $"{g.Key}: {g.Count()}")
            .ToArray();
    }
}
```
