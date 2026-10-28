### ToLookup - 具有 O(1) 键访问性能的即时分组

在 LINQ 中处理分组数据时，你可能已经用过 `GroupBy`，它会生成一个延迟计算的分组序列。
但是，如果你需要根据键重复查找分组而无需重新枚举，该怎么办？
这就是 `ToLookup` 的用武之地。

`ToLookup` 会**立即**将分组具体化为 `Lookup<TKey, TElement>`，这是一种针对一对多关系进行优化的类似字典的结构。
与延迟执行的 `GroupBy` 不同，`ToLookup` 会立即进行计算并将所有分组存储在内存中，从而在此后为你提供 **O(1) 的键访问**性能。

### 工作原理

当你在序列上调用 `.ToLookup(keySelector)` 时，每个元素都会被立即计算，并根据选择器返回的键放入对应的分组中。
返回的结果是一个 `Lookup<TKey, TElement>` 对象，你可以通过 `lookup[key]` 进行索引访问。

相比于 `Dictionary<TKey, List<TValue>>` 甚至是 `GroupBy`，它的核心优势在于**对缺失键的安全访问**：如果你请求一个不存在的键，`Lookup` 会返回一个**空序列**，而不是抛出 `KeyNotFoundException`。
这样就无需进行 `ContainsKey` 检查或使用 `TryGetValue` 模式。

### 语法

```csharp
// 只带键选择器的基本 ToLookup
ILookup<TKey, TElement> lookup = source.ToLookup(element => keyExpression);

// 带键选择器和元素选择器
ILookup<TKey, TResult> lookup = source.ToLookup(
    element => keyExpression,
    element => valueExpression
);

// 按键访问分组 - 始终安全，从不抛出异常
IEnumerable<TElement> group = lookup[someKey];
```

### 示例

```csharp
// 按部门对员工分组
var employees = new[] {
    new { Name = "Alice", Dept = "Engineering" },
    new { Name = "Bob", Dept = "Sales" },
    new { Name = "Carol", Dept = "Engineering" },
    new { Name = "Dave", Dept = "HR" }
};

var byDept = employees.ToLookup(e => e.Dept);

// O(1) 访问 - 返回 Alice、Carol
var engineers = byDept["Engineering"];

// 缺失的键返回空序列，不会抛出异常！
var marketing = byDept["Marketing"]; // 空序列，不是错误
Console.WriteLine(marketing.Count()); // 0

// 遍历所有分组
foreach (var group in byDept)
{
    Console.WriteLine($"{group.Key}: {group.Count()} people");
}
```

```csharp
// 按客户对订单金额分组，然后查询特定客户
var orders = new[] {
    new { Customer = "Acme", Amount = 150.0 },
    new { Customer = "Globex", Amount = 300.0 },
    new { Customer = "Acme", Amount = 200.0 }
};

var byCustomer = orders.ToLookup(o => o.Customer, o => o.Amount);

// 计算特定客户的总额
double acmeTotal = byCustomer["Acme"].Sum(); // 350.0

// 安全访问未知客户
double unknownTotal = byCustomer["Initech"].Sum(); // 0.0
```

### GroupBy 与 ToLookup 的对比

| 特性 | GroupBy | ToLookup |
| --- | --- | --- |
| 执行方式 | 延迟执行 (lazy) | 立即执行 (eager) |
| 返回类型 | `IEnumerable<IGrouping>` | `ILookup<TKey, TElement>` |
| 键访问 | 必须通过枚举查找 | `lookup[key]` - O(1) |
| 缺失键 | 不适用（无索引器） | 返回空序列 |
| 最佳适用场景 | 流式处理 / 单次遍历 | 重复按键查找 |

### 你的任务

编写一个方法，接收一个单词数组和一个整数长度数组。
从单词数组构建一个以单词长度为键的 `Lookup`。
然后，针对 `lengths` 数组中的每个查询长度，查找具有该长度的所有单词，并用逗号（无空格）将它们连接起来。
如果没有单词匹配给定的长度，则该项返回 `"none"`。
以与 `lengths` 数组相同的顺序返回 `string[]` 结果。

### 方法签名

```csharp
public static string[] LookupByLength(string[] words, int[] lengths)
```

### 预期结果

```css
LookupByLength(["cat", "dog", "elephant", "rat", "bear"], [3, 8, 5]) -> ["cat,dog,rat", "elephant", "none"]
LookupByLength(["hi", "go"], [2, 4]) -> ["hi,go", "none"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] LookupByLength(string[] words, int[] lengths)
    {
        // 以单词长度为键立即构建 Lookup
        var byLength = words.ToLookup(w => w.Length);

        // 按查询顺序取出对应分组，缺失的键返回空序列，此时输出 "none"
        return lengths
            .Select(len => byLength[len].Any() ? string.Join(",", byLength[len]) : "none")
            .ToArray();
    }
}
```
