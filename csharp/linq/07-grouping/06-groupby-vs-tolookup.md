### GroupBy 与 ToLookup：延迟求值与即时求值

LINQ 提供了两种根据键对元素进行分组的方法：`GroupBy` 和 `ToLookup`。
它们表面上看起来很相似，但在分组发生的**时机**以及复用结果的**安全性**方面有着本质的不同。

当你需要多次访问分组数据时（这是报表生成、缓存和数据转换管道中的常见模式），理解这种区别至关重要。

### 工作原理

**`GroupBy`** 使用延迟（惰性）执行。
在迭代结果之前，它实际上不会进行任何分组。
每次枚举结果时，源序列都会被重新计算。
当你只需要对分组进行单次遍历时，这种方式非常节省内存，但如果你重复访问同一个分组，则可能会导致细微的 bug 或性能问题，特别是当底层数据源在多次迭代之间发生变化时。

**`ToLookup`** 使用即时执行。
它会立即对整个源序列求值，并在内存中构建一个类似字典的结构（`ILookup<TKey, TElement>`）。
构建完成后，你可以随意多次访问任何键，而无需重新计算。
访问不存在的键会返回一个空序列，而不是抛出异常。

### 语法

```csharp
// GroupBy - 延迟执行，返回 IEnumerable<IGrouping<TKey, TElement>>
var grouped = source.GroupBy(item => item.KeyProperty);

// ToLookup - 立即执行，返回 ILookup<TKey, TElement>
var lookup = source.ToLookup(item => item.KeyProperty);

// 访问 Lookup 中的键（即使键不存在也是安全的）
IEnumerable<TElement> group = lookup[someKey];
```

### 示例

```csharp
// 示例 1：单次遍历场景使用 GroupBy
int[] scores = { 85, 92, 78, 95, 88, 72 };
var gradeGroups = scores.GroupBy(s => s >= 90 ? "A" : s >= 80 ? "B" : "C");
foreach (var group in gradeGroups)
    Console.WriteLine($"{group.Key}: {string.Join(", ", group)}");
// 一次性遍历完全没有问题

// 示例 2：重复随机按键访问使用 ToLookup
string[] cities = { "Paris", "Prague", "Berlin", "Boston", "Barcelona" };
var byFirstLetter = cities.ToLookup(c => c[0]);

// 多次访问 'P' 分组 - 不会重新求值
var pCities = byFirstLetter['P'];  // Paris, Prague
var pAgain = byFirstLetter['P'];   // Paris, Prague（结果相同，不会重新计算）

// 访问不存在的键 - 返回空序列，不抛出异常
var zCities = byFirstLetter['Z'];  // 空序列，不是 null 也不是异常

// 示例 3：组合 Lookup 中的分组
string[] fruits = { "apple", "apricot", "banana", "blueberry", "cherry" };
var byLength = fruits.ToLookup(f => f.Length);
var sixLetterTwice = byLength[6].Concat(byLength[6]).ToArray();
// ["banana", "cherry", "banana", "cherry"]
```

### 如何进行选择

| 场景 | 最佳选择 | 原因 |
| --- | --- | --- |
| 单次遍历所有分组 | `GroupBy` | 惰性求值可节省内存 |
| 重复访问特定键 | `ToLookup` | 即时求值可避免重复计算 |
| 键可能不存在 | `ToLookup` | 返回空序列，而无需过滤 |
| 与其他 LINQ 运算符链式调用 | `GroupBy` | 在管道中保持延迟执行 |

### 你的任务

编写一个方法，展示 `ToLookup` 在重复访问键时的优势。
给定一个单词数组和一个目标长度，使用 `ToLookup` 按长度对单词进行分组，然后访问该目标长度的分组**两次**，并将两次访问的结果拼接成一个结果数组。

这证明了 `ToLookup` 允许安全地重复访问同一个键，而无需重新计算源序列。

如果没有单词匹配给定的长度，结果应为一个空数组（因为 `ToLookup` 对于不存在的键会返回空序列）。

### 方法签名

```csharp
public static string[] MultipleAccess(string[] words, int length)
```

### 预期结果

```css
MultipleAccess(["cat", "dog", "elephant", "rat"], 3) -> ["cat", "dog", "rat", "cat", "dog", "rat"]
MultipleAccess(["hi", "go"], 2) -> ["hi", "go", "hi", "go"]
MultipleAccess(["apple", "berry"], 3) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] MultipleAccess(string[] words, int length)
    {
        // 按长度立即分组
        var byLength = words.ToLookup(w => w.Length);

        // 访问同一个键两次并拼接，缺失的键得到空序列
        return byLength[length].Concat(byLength[length]).ToArray();
    }
}
```
