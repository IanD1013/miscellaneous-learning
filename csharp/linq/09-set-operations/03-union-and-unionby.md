### Union 和 UnionBy - 合并无重复项的序列

在处理多个集合时，你经常需要将它们合并为一个仅包含唯一元素的单一序列。
LINQ 提供了 `Union` 和 `UnionBy` 来专门处理这种情况，它们会连接两个序列并自动移除重复项。
这在整合来自不同来源的数据时是一个常见操作，例如合并来自两个数据库的客户列表，或合并多篇文章的标签集合。

### 工作原理

`Union` 合并两个序列，并使用默认的相等性比较移除重复元素。
从概念上讲，它等同于先调用 `Concat`（首尾相接合并序列）然后调用 `Distinct`（移除重复项），但 `Union` 在一个步骤中完成了这两件事。

`UnionBy`（在 .NET 6 中引入）以相同的方式工作，但允许你指定一个**键选择器**（key selector）函数。
它不会比较整个元素，而是根据投影出的键来确定唯一性。
当两个元素具有相同的键时，将保留遇到的第一个元素。

### 语法

```csharp
// Union：通过比较整个元素进行去重
IEnumerable<T> result = firstSequence.Union(secondSequence);

// UnionBy：根据你选择的键进行去重
IEnumerable<T> result = firstSequence.UnionBy(secondSequence, element => element.SomeProperty);
```

### 示例

```csharp
// 使用 Union 合并两个字符串数组
string[] teamA = { "Alice", "Bob", "Charlie" };
string[] teamB = { "Bob", "Diana", "Alice" };
var allMembers = teamA.Union(teamB);
// 结果："Alice", "Bob", "Charlie", "Diana"
// 注意：重复项 "Bob" 和 "Alice" 仅出现一次

// Union 保留首次出现的顺序
double[] prices1 = { 9.99, 14.50, 9.99 };
double[] prices2 = { 14.50, 22.00 };
var uniquePrices = prices1.Union(prices2);
// 结果：9.99, 14.50, 22.00

// 带有键选择器的 UnionBy：按类别对产品去重
var storeA = new[] { new { Name = "Widget", Category = "Tools" }, new { Name = "Bolt", Category = "Hardware" } };
var storeB = new[] { new { Name = "Wrench", Category = "Tools" }, new { Name = "Nail", Category = "Hardware" } };
var merged = storeA.UnionBy(storeB, p => p.Category);
// 结果：Widget (Tools), Bolt (Hardware)
// "Wrench" 和 "Nail" 被丢弃，因为它们的类别已经出现过
```

### 重要细节

- `Union` 使用默认的相等性比较：对于像 `int` 和 `string` 这样的值类型，它会直接比较值。
- `Union` **不**保证输出结果具有任何特定顺序。
  如果需要排序后的结果，你必须显式进行排序。
- `Union` 返回 `IEnumerable<T>`，因此你需要使用 `.ToArray()` 或 `.ToList()` 来实例化结果。
- `Union` 和 `UnionBy` 都是惰性的，它们通过延迟执行按需生成元素。

### 你的任务

编写一个方法 `MergeUnique`，接收两个整数数组，并返回一个**升序排序**的**单一去重数组**，其中包含两个数组中的所有唯一元素。

例如：

- 数组 `[1, 3, 5]` 和 `[2, 3, 4]` 共享元素 `3`。
  合并、去重并排序后的结果为 `[1, 2, 3, 4, 5]`。

### 方法签名

```csharp
public static int[] MergeUnique(int[] a, int[] b)
```

### 预期结果

```css
MergeUnique([1, 3, 5], [2, 3, 4]) -> [1, 2, 3, 4, 5]
MergeUnique([1, 1, 1], [1, 1, 1]) -> [1]
MergeUnique([], [4, 2, 6])        -> [2, 4, 6]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] MergeUnique(int[] a, int[] b)
    {
        // 使用 Union 合并并去重，再按升序排序
        return a.Union(b).OrderBy(x => x).ToArray();
    }
}
```
