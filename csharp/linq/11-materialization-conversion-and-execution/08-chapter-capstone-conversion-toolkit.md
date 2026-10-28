### 多阶段 LINQ 转换管道

现实世界中的数据处理很少只涉及单一操作。
你经常需要将多个转换链接在一起：去重、排序、重构为新的形态，最后投影为输出格式。
LINQ 提供了丰富的转换和投影方法，可以自然地组合成处理管道。

本练习将你学到的四个关键 LINQ 操作：`ToHashSet`、`OrderBy`、`ToDictionary` 和 `Select`，整合到一个紧密协作的管道中。

### 工作原理

可以将数据管道想象成一条流水线。
每个阶段接收上一阶段的输出并对其进行转换：

1. **`ToHashSet()`** - 将序列具体化为 `HashSet<T>`，它会自动消除重复元素。结果是一个包含唯一项的无序集合。
2. **`OrderBy()`** - 接收一个序列并根据你指定的键对其进行排序。由于 `HashSet` 不保证顺序，排序可以恢复可预测的序列。
3. **`ToDictionary()`** - 通过指定键选择器和值选择器，将序列转换为 `Dictionary<TKey, TValue>`。每个元素都会成为一个键值对。
4. **`Select()`** - 将每个元素投影为新形式。当应用于字典的键值对时，你可以将每个条目重塑为所需的任何格式。

### 语法

```csharp
// ToHashSet：消除重复元素
HashSet<T> unique = collection.ToHashSet();

// OrderBy：按键排序
IOrderedEnumerable<T> sorted = collection.OrderBy(item => item.SomeProperty);

// ToDictionary：构建键值映射
Dictionary<TKey, TValue> map = collection.ToDictionary(
    item => /* 键选择器 */,
    item => /* 值选择器 */
);

// Select：转换每个元素
IEnumerable<TResult> projected = collection.Select(item => /* 新形态 */);
```

### 示例

考虑一个可能存在重复项的产品代码列表，你需要一个已排序的摘要：

```csharp
// 阶段 1：移除重复的产品代码
string[] codes = { "X100", "A200", "X100", "B300", "A200" };
HashSet<string> uniqueCodes = codes.ToHashSet();
// 结果：{ "X100", "A200", "B300" }（无序）

// 阶段 2：按字母顺序排序
var sorted = uniqueCodes.OrderBy(c => c);
// 结果：["A200", "B300", "X100"]

// 阶段 3：构建将代码映射到其首字符的查找表
var lookup = sorted.ToDictionary(c => c, c => c[0]);
// 结果：{ "A200": 'A', "B300": 'B', "X100": 'X' }

// 阶段 4：投影为显示用的字符串
var display = lookup.Select(kvp => $"{kvp.Key} -> {kvp.Value}");
// 结果：["A200 -> A", "B300 -> B", "X100 -> X"]
```

另一个使用整数的示例：

```csharp
int[] scores = { 85, 92, 85, 78, 92, 60 };
var result = scores
    .ToHashSet()          // { 85, 92, 78, 60 }
    .OrderBy(s => s)      // [60, 78, 85, 92]
    .ToDictionary(s => s, s => s >= 80 ? "Pass" : "Fail")
    .Select(kvp => $"{kvp.Key}={kvp.Value}")
    .ToArray();
// 结果：["60=Fail", "78=Fail", "85=Pass", "92=Pass"]
```

### 常见模式

| 模式 | 作用 |
| --- | --- |
| `.ToHashSet()` 然后 `.OrderBy()` | 去重，然后恢复可预测的顺序 |
| `.ToDictionary(k, v)` | 从任何已排序/已过滤的集合中创建查找映射 |
| 在字典上调用 `.Select(kvp => ...)` | 将键值对重塑为字符串、对象等 |
| 链接所有四个方法 | 完整管道：去重 → 排序 → 映射 → 投影 |

请注意，当你遍历 `Dictionary`（或在其上调用 `.Select()`）时，每个元素都是具有 `.Key` 和 `.Value` 属性的 `KeyValuePair<TKey, TValue>`。

### 你的任务

编写一个方法，接收一个单词数组并通过一个四阶段管道处理它们：

1. 使用 `HashSet` 对单词进行**去重**
2. 按字母顺序对唯一的单词进行**排序**
3. **构建字典**，将每个单词映射到其字符长度
4. 将每个字典条目**投影**为 `"word:length"` 格式

将最终结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] ConversionPipeline(string[] words)
```

### 预期结果

```css
ConversionPipeline(["banana", "apple", "banana", "cherry", "apple"]) -> ["apple:5", "banana:6", "cherry:6"]
ConversionPipeline(["dog", "cat", "bird"]) -> ["bird:4", "cat:3", "dog:3"]
ConversionPipeline(["hello"]) -> ["hello:5"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static string[] ConversionPipeline(string[] words)
    {
        return words
            .ToHashSet()                              // 阶段 1：去重
            .OrderBy(w => w)                          // 阶段 2：按字母顺序排序
            .ToDictionary(w => w, w => w.Length)      // 阶段 3：单词 -> 长度
            .Select(kvp => $"{kvp.Key}:{kvp.Value}")  // 阶段 4：投影为 "word:length"
            .ToArray();
    }
}
```
