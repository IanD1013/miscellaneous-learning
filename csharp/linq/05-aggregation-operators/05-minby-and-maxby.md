### MinBy 和 MaxBy - 返回元素本身，而非仅仅是值

从 .NET 6 (C# 10) 开始，LINQ 引入了两个强大的方法：`MinBy` 和 `MaxBy`。
在这些方法出现之前，开发者通常需要编写繁琐的多步代码来解决一个简单的问题：*“哪个元素具有某个属性的最小值（或最大值）？”*
这两个方法只需一次调用就能优雅地解决该问题。

### 关键区别：Min 与 MinBy

假设你有一个对象集合，并希望根据某个属性找到最小值。
较早的 `Min(selector)` 方法返回的是**投影值**本身，即你投影到的数字、日期或字符串。
相比之下，`MinBy(keySelector)` 返回的是集合中的**原始元素**，该元素的投影键值最小。

例如，如果你有一个员工列表，想要找到工资最低的员工：

- `employees.Min(e => e.Salary)` → 返回工资数额（一个 `decimal`）
- `employees.MinBy(e => e.Salary)` → 返回具有该工资的**员工对象**

同样的区别也适用于 `Max` 与 `MaxBy`。

### 语法

```csharp
// 返回最小的投影值（VALUE）
TResult Min<TSource, TResult>(Func<TSource, TResult> selector);

// 返回投影键最小的那个元素（ELEMENT）
TSource MinBy<TSource, TKey>(Func<TSource, TKey> keySelector);

// Max 与 MaxBy 遵循相同的模式
TSource MaxBy<TSource, TKey>(Func<TSource, TKey> keySelector);
```

### 示例

```csharp
// 示例 1：查找最便宜的产品（而不仅仅是它的价格）
var products = new[] {
    new { Name = "Laptop", Price = 999.99 },
    new { Name = "Mouse", Price = 24.99 },
    new { Name = "Monitor", Price = 349.99 }
};

var cheapestPrice = products.Min(p => p.Price);   // 24.99（仅仅是数字）
var cheapestProduct = products.MinBy(p => p.Price); // { Name = "Mouse", Price = 24.99 }

// 示例 2：查找列表中最早的日期
var dates = new[] { "2024-03-15", "2021-07-01", "2023-11-20" };
var earliest = dates.MinBy(d => DateTime.Parse(d)); // "2021-07-01"（字符串，而不是 DateTime）

// 示例 3：查找名称最长的城市
var cities = new[] { "Tokyo", "San Francisco", "Rome", "Rio de Janeiro" };
var longestName = cities.MaxBy(c => c.Length); // "Rio de Janeiro"
```

### 平局处理规则

当多个元素具有相同的最小（或最大）键值时，`MinBy` 和 `MaxBy` 会返回序列中遇到的**第一个**此类元素。
这是确定且可预测的：集合的迭代顺序决定了平局时的胜出者。

### 你的任务

编写一个方法，接收一个单词数组，并返回字符数最少的**单词**（而不是其长度！）。
如果有多个单词具有相同的最短长度，则返回数组中首先出现的那个单词。

### 方法签名

```csharp
public static string GetShortestWord(string[] words)
```

### 预期结果

```rust
GetShortestWord(["elephant", "cat", "butterfly"]) -> "cat"
GetShortestWord(["hi", "hello", "hey"]) -> "hi"
GetShortestWord(["a"]) -> "a"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string GetShortestWord(string[] words)
    {
        // MinBy 返回长度最小的单词本身，平局时返回第一个出现的单词
        return words.MinBy(w => w.Length);
    }
}
```
