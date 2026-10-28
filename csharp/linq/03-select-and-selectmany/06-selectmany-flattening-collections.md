### SelectMany - 扁平化嵌套序列

在 C# 中处理集合时，你经常会遇到序列中的每个元素自身都包含一个子集合的情况。
例如，部门列表中的每个部门可能包含一个员工列表，或者订单列表中的每个订单可能包含一个明细项列表。
`SelectMany` 是一个 LINQ 方法，它将每个元素投影到一个集合中，然后将所有这些子集合**扁平化**合并为一个单一连续的序列。

### 工作原理

可以这样理解 `Select` 与 `SelectMany` 的区别：

- **`Select`** 将每个元素转换为某种内容：如果该“内容”是一个集合，你最终会得到一个*集合的集合*（嵌套结构）。
- **`SelectMany`** 执行相同的转换，但随后会*解包*每个内部集合，将所有元素合并为一个扁平序列。

如果不使用 LINQ，你需要使用嵌套的 `foreach` 循环来实现此功能，将项累加到一个单一输出列表中。
而 `SelectMany` 只需一次调用即可完成所有这些操作。

### 语法

```csharp
// 通用模式：
IEnumerable<TResult> result = source.SelectMany(element => /* 返回 IEnumerable<TResult> 的表达式 */);
```

传递给 `SelectMany` 的 lambda 表达式接收来自外部序列的一个元素，并且必须返回一个 `IEnumerable<T>`（数组、列表或任何序列）。
`SelectMany` 会遍历每个返回的序列，并将每个项生成到单个扁平输出中。

### 示例

```csharp
// 示例 1：扁平化一组整数数组
int[][] grid = { new[] {1, 2}, new[] {3, 4, 5}, new[] {6} };
int[] flat = grid.SelectMany(row => row).ToArray();
// flat => [1, 2, 3, 4, 5, 6]

// 示例 2：获取一组名字中的所有字符
string[] names = { "Ada", "Bo" };
char[] allChars = names.SelectMany(name => name.ToCharArray()).ToArray();
// allChars => ['A', 'd', 'a', 'B', 'o']

// 示例 3：从博客文章中提取标签
var posts = new[]
{
    new { Title = "LINQ Tips", Tags = new[] { "csharp", "linq" } },
    new { Title = "EF Core", Tags = new[] { "csharp", "database" } }
};
string[] allTags = posts.SelectMany(p => p.Tags).ToArray();
// allTags => ["csharp", "linq", "csharp", "database"]
```

请注意在每个示例中，内部集合（行、字符、标签）是如何被*合并*为一个扁平序列的。

### 实用参考

| 方法 / 特性 | 描述 | 返回值 |
| --- | --- | --- |
| `SelectMany(func)` | 将每个元素投影到一个序列，然后扁平化 | `IEnumerable<T>` |
| `Select(func)` | 将每个元素投影到一个单独的值 | `IEnumerable<T>`（可以是嵌套的） |
| `string.Split(char)` | 将字符串拆分为子字符串数组 | `string[]` |
| `.ToArray()` | 将 LINQ 查询具体化为一个数组 | `T[]` |

### 你的任务

编写一个方法，接收一个句子（字符串）数组，并返回一个包含来自所有句子的每个单独单词的**单个扁平数组**，同时保持原有顺序。
每个句子中的单词由单个空格分隔。

### 方法签名

```csharp
public static string[] FlattenSentences(string[] sentences)
```

### 预期结果

```css
FlattenSentences(["hello world", "foo bar baz"]) -> ["hello", "world", "foo", "bar", "baz"]
FlattenSentences(["one"]) -> ["one"]
FlattenSentences([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FlattenSentences(string[] sentences)
    {
        // 把每个句子按空格拆分为单词数组，再用 SelectMany 扁平化为一个序列
        return sentences.SelectMany(s => s.Split(' ')).ToArray();
    }
}
```
