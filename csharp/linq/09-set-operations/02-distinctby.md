### DistinctBy - 根据派生键去重

在日常开发中，你经常需要从集合中移除重复项，但不是基于整个元素本身。
也许你有一个产品列表并希望每个类别只保留一个产品，或者有一个员工列表并希望每个部门只保留一名员工。
在 .NET 6 之前，实现这一点需要像 `GroupBy(...).Select(g => g.First())` 这样冗长的模式。
从 .NET 6 开始，LINQ 提供了 `DistinctBy`，它允许你指定一个**键选择器**（key selector）来控制什么才算作“重复项”。

### 运作原理

`DistinctBy` 遍历源序列并记录它已经遇到过的键值。
对于每个元素，它使用你的选择器函数计算键。
如果该键之前未曾见过，则将该元素输出。
如果该键*已经*出现过，则跳过该元素。
这意味着**对于每个唯一键，首次遇到的元素会被保留**，并且原始顺序保持不变。

### 语法

```csharp
IEnumerable<TSource> DistinctBy<TSource, TKey>(
    this IEnumerable<TSource> source,
    Func<TSource, TKey> keySelector
)
```

`keySelector` 是一个用于从每个元素中提取键的函数。
具有相同键的元素会被视为重复项，且只有第一个元素会被保留。

### 示例

```csharp
// 示例 1：每个年龄只保留一个人
var people = new[] { "Alice:30", "Bob:25", "Carol:30", "Dave:25", "Eve:40" };
var result = people.DistinctBy(p => p.Split(':')[1]);
// 结果：["Alice:30", "Bob:25", "Eve:40"]
// Carol 和 Dave 被丢弃，因为年龄 30 和 25 已经出现过。

// 示例 2：每个首字母只保留一种水果
var fruits = new[] { "apple", "avocado", "banana", "blueberry", "cherry" };
var unique = fruits.DistinctBy(f => f[0]);
// unique：["apple", "banana", "cherry"]
// "avocado" 与 "apple" 的首字母同为 'a'，"blueberry" 与 "banana" 的首字母同为 'b'

// 示例 3：与旧的 GroupBy 方式进行比较
// 旧方式（冗长）：
var oldWay = fruits.GroupBy(f => f[0]).Select(g => g.First());
// 新方式（简洁）：
var newWay = fruits.DistinctBy(f => f[0]);
// 两者产生相同的结果，但 DistinctBy 更简洁、更易读。
```

### 重要细节

- `DistinctBy` 会保留元素的**原始顺序**。
- 它始终为每个唯一键保留**第一个**元素。
- 键可以是支持相等性比较的任何类型（int、string、char 等）。
- 如果你需要实例化集合，别忘了调用 `.ToArray()` 或 `.ToList()`。

### 你的任务

编写一个方法，接收一个单词数组，并仅返回**每个唯一字符串长度所遇到的第一个单词**。
结果应保留输入数组中单词的原始顺序。

例如，给定 `["cat", "dog", "elephant", "ant", "bird"]`：

- `"cat"` 的长度为 3 → 首次出现长度 3，**保留它**
- `"dog"` 的长度为 3 → 已经出现过长度 3，跳过
- `"elephant"` 的长度为 8 → 首次出现长度 8，**保留它**
- `"ant"` 的长度为 3 → 已经出现过长度 3，跳过
- `"bird"` 的长度为 4 → 首次出现长度 4，**保留它**

结果：`["cat", "elephant", "bird"]`

### 方法签名

```csharp
public static string[] UniqueByLength(string[] words)
```

### 预期结果

```css
UniqueByLength(["cat", "dog", "elephant", "ant", "bird"]) -> ["cat", "elephant", "bird"]
UniqueByLength(["a", "bb", "c", "dd", "eee"]) -> ["a", "bb", "eee"]
UniqueByLength([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] UniqueByLength(string[] words)
    {
        // 以单词长度作为键去重，每个长度只保留首次出现的单词
        return words.DistinctBy(w => w.Length).ToArray();
    }
}
```
