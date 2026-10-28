### 从头实现 SelectMany

LINQ 的 `SelectMany` 是 C# 中最强大的投影操作符之一。
它接收一个元素序列，将每个元素投影为一个子集合，然后将所有这些子集合**展平**（flatten）为一个连续的单一序列。
理解其内部工作原理可以加深你对迭代器、延迟执行（deferred execution）以及 `yield return` 语句的理解。

在实际代码中，你会经常遇到展平操作：包含多个订单的客户列表、包含文件的目录列表，或者包含句子的段落列表。
`SelectMany` 可以处理所有这些情况，但了解如何自行构建它能够揭示其底层优雅的运行机制。

### 展平的工作原理

展平需要**两个嵌套的迭代器**：

1. **外层迭代器**：遍历源序列中的每个元素。
2. **内层迭代器**：遍历由该元素生成的子集合中的每个项目。

核心要点在于，**内层**循环中的 `yield return` 会一次向展平的输出中产出一个项目。
因为 `yield return` 使该方法成为一个迭代器，所以整个操作都是**延迟计算**（lazily evaluated）的：项目是按需生成的，而不是一次性全部生成。

### 语法

```csharp
public static IEnumerable<TResult> MyFlatten<TSource, TResult>(
    IEnumerable<TSource> source,
    Func<TSource, IEnumerable<TResult>> selector)
{
    foreach (TSource outer in source)
    {
        foreach (TResult inner in selector(outer))
        {
            yield return inner;
        }
    }
}
```

注意其结构：`yield return` 出现在**内层** `foreach` 中，而不是外层。
外层循环的每次迭代都会生成一个子集合，而内层循环则深入其中，逐个产出每个元素。

### 示例

考虑一个整数数组列表，你希望将其展平为单个整数流：

```csharp
// 展平嵌套的整数数组
public static IEnumerable<int> FlattenNumbers(int[][] groups)
{
    foreach (int[] group in groups)
    {
        foreach (int number in group)
        {
            yield return number;
        }
    }
}

// 用法：
int[][] data = { new[] {1, 2}, new[] {3}, new[] {4, 5, 6} };
foreach (int n in FlattenNumbers(data))
    Console.Write(n + " ");
// 输出：1 2 3 4 5 6
```

或者从字符串列表中展平字符：

```csharp
public static IEnumerable<char> FlattenChars(string[] words)
{
    foreach (string word in words)
    {
        foreach (char ch in word)
        {
            yield return ch;
        }
    }
}

// FlattenChars(["hi", "bye"]) 产出：'h', 'i', 'b', 'y', 'e'
```

### 为什么 yield return 很重要

- 如果没有 `yield return`，你需要创建一个 `List<T>`，向其中添加项目，然后返回整个列表，这会失去延迟执行的优势。
- 使用 `yield return`，该方法将成为一个**状态机**：它在每次 yield 后暂停，并在使用者请求下一个项目时恢复执行。
- 这意味着展平包含一百万个元素的序列时，不需要创建一个包含一百万个元素的中间列表。

### 常见陷阱

| 错误 | 原因 |
| --- | --- |
| 仅在外层循环中使用 `yield return` | 你产出的将是整个子集合，而不是单个项目 |
| 返回 `List<T>` | 失去延迟计算特性；分配不必要的内存 |
| 忘记遍历子集合 | 内层元素永远不会被产出 |

### 你的任务

编写一个名为 `FlattenWords` 的方法，它接收一个句子（字符串）数组。
对于每个句子，按空格将其拆分为单独的单词，然后逐个 yield 每个单词。
结果应该是一个按顺序包含所有句子中所有单词的扁平序列。

使用带有 `yield return` 的**嵌套 `foreach` 循环**，不要使用 LINQ 的 `SelectMany`。

### 方法签名

```csharp
public static IEnumerable<string> FlattenWords(string[] sentences)
```

### 预期结果

```css
FlattenWords(["a b", "c d e"]) -> ["a", "b", "c", "d", "e"]
FlattenWords(["hello world"]) -> ["hello", "world"]
FlattenWords([]) -> []
FlattenWords(["single"]) -> ["single"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static IEnumerable<string> FlattenWords(string[] sentences)
    {
        // 外层循环：遍历每个句子
        foreach (string sentence in sentences)
        {
            // 内层循环：按空格拆分后逐个产出单词
            foreach (string word in sentence.Split(' '))
            {
                yield return word;
            }
        }
    }
}
```
