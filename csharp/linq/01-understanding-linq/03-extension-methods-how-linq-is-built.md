### 扩展方法与 LINQ

每当你在 C# 中的集合上编写 `.Where(...)`、`.Select(...)` 或 `.OrderBy(...)` 时，你调用的都是**扩展方法**。
扩展方法允许你在不修改现有类型的情况下为其添加新方法。
LINQ（语言集成查询，Language Integrated Query）完全构建于这种机制之上。
了解扩展方法的工作原理，有助于你理解为什么 LINQ 体验如此自然，以及如何流畅地将操作链式调用结合在一起。

### 扩展方法的工作原理

扩展方法是 `static` 类中的 `static` 方法，其第一个参数带有 `this` 关键字前缀。
这第一个参数决定了该方法所“扩展”的类型。
编译器会重写该调用，使其看起来就像一个实例方法，即使它在本质上是静态的。

例如，`System.Linq.Enumerable` 是一个静态类，包含数百个静态方法，如 `Where`、`Select`、`OrderBy`、`Count` 和 `Sum`。
每个方法都扩展了 `IEnumerable<T>`，这意味着**任何**实现了 `IEnumerable<T>` 的集合（数组、列表、字典、哈希集合等）都可以访问所有的 LINQ 功能。

### 语法

```csharp
// 定义一个扩展方法
public static class StringExtensions
{
    public static string Shout(this string text)
    {
        return text.ToUpper() + "!!!";
    }
}

// 使用它：看起来就像一个实例方法
string greeting = "hello";
string result = greeting.Shout(); // "HELLO!!!"

// 在幕后，编译器会将其转换为：
string result = StringExtensions.Shout(greeting);
```

### 作为扩展方法的 LINQ

像 `Select`、`Where` 和 `OrderBy` 这样的 LINQ 方法遵循相同的模式。
它们定义在 `System.Linq.Enumerable` 中并扩展了 `IEnumerable<T>`：

```csharp
// Select 的简化签名：
public static IEnumerable<TResult> Select<TSource, TResult>(
    this IEnumerable<TSource> source,
    Func<TSource, TResult> selector)
```

因为每个 LINQ 方法都返回 `IEnumerable<T>`，所以你可以将它们**链式调用**：一个方法的输出将成为下一个方法的输入：

```csharp
// 链式调用：过滤 -> 转换 -> 排序
int[] prices = { 120, 45, 300, 80, 15 };

var affordable = prices
    .Where(p => p < 100)       // 保留 45, 80, 15
    .Select(p => p * 0.9)      // 应用 10% 折扣: 40.5, 72.0, 13.5
    .OrderBy(p => p)           // 升序排序: 13.5, 40.5, 72.0
    .ToArray();
```

### 示例

```csharp
// 将名称投影为其首字符
string[] cities = { "Tokyo", "Oslo", "Lima" };
char[] initials = cities.Select(c => c[0]).ToArray();
// initials: ['T', 'O', 'L']

// 将数字投影为其平方
int[] nums = { 2, 5, 9 };
int[] squares = nums.Select(n => n * n).ToArray();
// squares: [4, 25, 81]

// 将产品投影为一个计算值
double[] weights = { 1.5, 3.2, 0.8 };
bool[] heavy = weights.Select(w => w > 2.0).ToArray();
// heavy: [false, true, false]
```

注意其中的模式：`Select` 接收一个 lambda 表达式，用于描述从每个元素中**提取或计算什么**。
其结果是一个由转换后的值组成的新序列。
最后在末尾调用 `.ToArray()` 可以将该惰性序列具体化为一个具体的数组。

### 常用参考

| 方法 | 用途 | 返回值 |
| --- | --- | --- |
| `Select(x => ...)` | 转换每个元素 | `IEnumerable<TResult>` |
| `Where(x => ...)` | 过滤元素 | `IEnumerable<T>` |
| `OrderBy(x => ...)` | 升序排序 | `IOrderedEnumerable<T>` |
| `ToArray()` | 转换为数组 | `T[]` |
| `ToList()` | 转换为列表 | `List<T>` |

### 你的任务

编写一个方法，接收一个单词数组，并返回一个整数数组，其中每个整数对应单词的**长度**。

例如，给定 `["cat", "elephant", "ox"]`，结果应为 `[3, 8, 2]`，因为 "cat" 有 3 个字符，"elephant" 有 8 个字符，"ox" 有 2 个字符。

- 输出数组的元素数量必须与输入数组相同。
- 如果输入数组为空，则返回一个空数组。
- 保持原有顺序。

### 方法签名

```csharp
public static int[] GetWordLengths(string[] words)
```

### 预期结果

```css
GetWordLengths(["hello", "hi", "hey"]) -> [5, 2, 3]
GetWordLengths(["a"]) -> [1]
GetWordLengths([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] GetWordLengths(string[] words)
    {
        // 用 Select 把每个单词投影为它的长度
        return words.Select(w => w.Length).ToArray();
    }
}
```
