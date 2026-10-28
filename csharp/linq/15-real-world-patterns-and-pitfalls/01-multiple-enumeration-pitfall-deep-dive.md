### LINQ 中多次枚举的陷阱

C# 中的 LINQ 查询采用**延迟执行**（deferred execution）：当你声明查询时，它并不会立即计算。
相反，它会构建操作的描述，只有当你实际枚举结果时才会执行。
这在性能方面非常强大，但它隐藏了一个危险的陷阱：**每次你枚举延迟查询时，它都会从头重新执行一次**。

如果底层数据源是数据库调用、网络请求或带有副作用的计算，枚举两次就意味着执行两次昂贵的操作。
即使对于内存中的集合，多余的枚举也会浪费 CPU 周期，并且如果数据源在两次枚举之间发生变化，还可能会产生不一致的结果。

### 工作原理

思考以下代码：

```csharp
IEnumerable<int> filtered = scores.Where(s => s >= 60);
int passing = filtered.Count();   // 第 1 次枚举
int highest = filtered.Max();     // 第 2 次枚举
```

每次对 `Count()` 和 `Max()` 的调用都会独立遍历 `filtered`。
对于每次枚举，`Where` 谓词都会对每个元素运行一次，因此对于 1000 个元素，该谓词将执行 2000 次，而不是 1000 次。

现在想象一下数据源不是简单的数组，而是一个数据库查询：

```csharp
IEnumerable<Order> expensiveOrders = db.Orders.Where(o => o.Total > 500);
int count = expensiveOrders.Count();    // 第 1 次 SQL 查询
Order first = expensiveOrders.First();  // 第 2 次 SQL 查询
```

两次独立的 SQL 查询会直接访问数据库。
在两次查询之间，数据可能会发生变化，从而导致不一致：`count` 可能是 5，但当 `First()` 运行时，数据可能已经不同了。

### 解决方法：物化一次

解决方案是使用 `ToList()` 或 `ToArray()` 将查询**物化**（materialize）为具体的集合。
这会强制执行单次枚举并将结果存储在内存中：

```csharp
List<string> activeCities = customers
    .Where(c => c.IsActive)
    .Select(c => c.City)
    .Distinct()
    .ToList();  // 只枚举一次，并存储结果

// 现在这些操作都从内存中的列表读取，不会重新枚举
int cityCount = activeCities.Count;  // 是属性而不是方法，O(1)
string firstCity = activeCities[0];
bool hasNewYork = activeCities.Contains("New York");
```

请注意，物化为 `List<T>` 后，你可以使用 `.Count` 属性（O(1) 查找），而不是 `.Count()` LINQ 扩展方法。

### 识别问题

诸如 ReSharper 和 Rider 等工具会发出 "possible multiple enumeration of IEnumerable" 的警告。
需要注意的模式：

| 危险模式 | 安全替代方案 |
| --- | --- |
| 多次使用同一个 `IEnumerable<T>` 变量 | 先调用 `.ToList()` 或 `.ToArray()` |
| 在同一个查询上先调用 `.Count()` 再调用 `.First()` | 物化后，使用 `.Count` 属性和索引器 |
| 将 `IEnumerable<T>` 传递给多个方法 | 在传递之前进行物化 |
| 在循环条件中进行枚举 | 在循环之前进行物化 |

### 何时使用 `ToList()` 与 `ToArray()`

- **`ToList()`** - 当你以后可能会添加/删除元素，或者需要使用 `List<T>` 的方法时
- **`ToArray()`** - 当集合大小固定且你希望减少微小的内存开销时

两者都会强制对数据源进行且仅进行一次枚举。

### 你的任务

编写一个方法，接收一个整数数组，过滤以仅保留**正数**（大于零），将过滤后的结果物化为一个 `List<int>` 且仅物化一次，然后从该物化列表中计算四个聚合值：

1. 正数的**数量**（Count）
2. 正数的**总和**（Sum）
3. 正数的**最小值**（Minimum）
4. 正数的**最大值**（Maximum）

以 `int[]` 的形式按 `[count, sum, min, max]` 的顺序返回这四个值。

关键约束：**所有四个聚合操作都必须在同一个物化列表上进行**，而不是在延迟查询上操作。

### 方法签名

```csharp
public static int[] SafeProcess(int[] numbers)
```

### 预期结果

```scss
SafeProcess([1, 2, 3, 4, 5])        -> [5, 15, 1, 5]
SafeProcess([-3, -1, 0, 2, 7])      -> [2, 9, 2, 7]
SafeProcess([42])                    -> [1, 42, 42, 42]
SafeProcess([10, -5, 3, -2, 8, 0])  -> [3, 21, 3, 10]
```

### 解答

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

public class Solution
{
    public static int[] SafeProcess(int[] numbers)
    {
        // 过滤出正数，并且只物化一次
        List<int> positives = numbers.Where(n => n > 0).ToList();

        // 所有聚合都在同一个物化列表上进行
        return new int[] { positives.Count, positives.Sum(), positives.Min(), positives.Max() };
    }
}
```
