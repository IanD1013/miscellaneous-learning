### LINQ 中的查询语法与方法语法

C# 提供了两种编写 LINQ 查询的方式：**查询语法**（query syntax）和**方法语法（method syntax）**。
它们表面看起来非常不同，但 C# 编译器在编译前会将查询语法转换为方法语法。
这意味着它们生成的 IL 代码完全相同，查询语法纯粹是一种**语法糖**。

理解这两种形式都很重要，但大多数 C# 开发者和代码库更青睐**方法语法**，因为它更简洁、组合起来更自然，并且能让你使用全部的 LINQ 操作符（其中许多操作符没有对应的查询语法）。

### 运作原理

当你使用 `from ... where ... select` 关键字编写查询时，编译器在后台会将其重写为方法调用链。

例如，这两个语句在编译后是**完全相同**的：

```csharp
// 查询语法
var result = from n in numbers
             where n > 10
             select n;

// 方法语法（编译器实际生成的代码）
var result = numbers.Where(n => n > 10);
```

`where` 关键字映射到 `.Where()` 方法。
`select` 关键字映射到 `.Select()`。
当 `select` 子句只是原样返回元素（例如 `select n`）时，编译器会完全省略 `.Select()` 调用，因为它是多余的。

### 语法

```csharp
// 方法语法过滤的通用模式
source.Where(element => condition)
```

`.Where()` 方法接受一个 **Lambda 表达式**：这是一个小型内联函数，它接收每个元素并返回 `true` 或 `false`。
Lambda 返回 `true` 的元素会被包含在结果中。

### 示例

```csharp
// 过滤大于 50 的数字
int[] scores = { 85, 42, 91, 37, 68 };
var passing = scores.Where(s => s > 50);  // [85, 91, 68]

// 过滤以元音开头的字符串
string[] cities = { "Austin", "Boston", "Orlando", "Denver" };
var vowelCities = cities.Where(c => "AEIOU".Contains(c[0]));  // ["Austin", "Orlando"]

// 使用多个条件过滤
int[] ages = { 12, 25, 17, 30, 15, 42 };
var adults = ages.Where(a => a >= 18 && a < 40);  // [25, 30]
```

注意方法语法读起来像一条自然的链条：“获取此集合，按此条件进行过滤。”
每次 `.Where()` 调用都会保留元素的原始顺序。

### 两种语法之间的转换

以下是直观的对比：

| 查询语法 | 方法语法 |
| --- | --- |
| `from p in products where p.Price < 20 select p` | `products.Where(p => p.Price < 20)` |
| `from s in students where s.Grade == "A" select s` | `students.Where(s => s.Grade == "A")` |
| `from x in items where x != null select x` | `items.Where(x => x != null)` |

### 返回数组

像 `.Where()` 这样的 LINQ 方法返回的是 `IEnumerable<T>`，这是一个惰性序列。
如果你需要一个具体的数组，请在调用链末尾调用 `.ToArray()`。

```csharp
string[] fruits = { "apple", "fig", "banana", "kiwi" };
string[] longFruits = fruits.Where(f => f.Length > 3).ToArray();
// longFruits 为 ["apple", "banana", "kiwi"]
```

### 你的任务

编写一个方法来过滤单词数组，仅返回长度**至少**为 `minLength` 的单词。
使用**方法语法**（而非查询语法）。
结果应保留元素的原始顺序，并作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] FilterByMinLength(string[] words, int minLength)
```

### 预期结果

```css
FilterByMinLength(["cat", "butterfly", "dog", "elephant"], 4) -> ["butterfly", "elephant"]
FilterByMinLength(["hi", "hello", "hey"], 3) -> ["hello", "hey"]
FilterByMinLength(["a", "bb", "ccc"], 5) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FilterByMinLength(string[] words, int minLength)
    {
        // 方法语法：保留长度至少为 minLength 的单词
        return words.Where(w => w.Length >= minLength).ToArray();
    }
}
```
