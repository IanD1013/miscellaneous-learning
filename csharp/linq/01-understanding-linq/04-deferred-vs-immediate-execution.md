### LINQ 中的延迟执行与立即执行

LINQ 操作符根据其实际**何时**执行分为两类。
理解这一区别对于编写正确、高效的 C# 代码至关重要，尤其是当处理随时间变化的数据源或关注性能时。

### 工作原理

当你调用像 `Where`、`Select` 或 `OrderBy` 这样的**延迟**操作符时，不会立即执行任何操作。
相反，这些操作符会构建一个关于要执行什么操作的描述。
只有当你**遍历**结果时（例如在 `foreach` 循环中或调用需要这些值的方法时），实际的计算才会发生。

像 `Count`、`ToList`、`Sum`、`First`、`ToArray` 和 `Any` 这样的**立即**操作符会强制查询立即运行。
它们会遍历整个序列（或序列中足够的部分）并返回一个具体的结果（一个数字、一个列表、单个元素），而不是另一个延迟查询。

可以把它想象成写食谱与做菜的区别。
延迟操作符负责写食谱；立即操作符则是真正下厨做菜。

### 语法

```csharp
// 延迟：此时还没有执行任何操作
var query = source.Where(x => x > 10).Select(x => x * 2);

// 立即：现在就执行，返回一个具体的值
int total = source.Sum();
List<int> results = source.Where(x => x > 10).ToList();
bool hasAny = source.Any(x => x < 0);
int howMany = source.Count(x => x == 5);
```

### 示例

```csharp
// 示例 1：延迟执行，查询此时还没有运行
int[] scores = { 85, 92, 67, 73, 95 };
var passing = scores.Where(s => s >= 70); // 这里什么都不会发生
// 只有在我们遍历时，过滤才会运行：
foreach (var s in passing)
    Console.WriteLine(s); // 85, 92, 73, 95

// 示例 2：使用 Sum 立即执行
double[] prices = { 4.99, 12.50, 3.25, 8.00 };
double total = prices.Sum(); // 立即执行 → 28.74

// 示例 3：使用 Count 和谓词立即执行
string[] cities = { "Paris", "London", "Rome", "Tokyo", "Berlin" };
int shortNames = cities.Count(c => c.Length <= 4); // 执行 → 2（Rome, Tokyo……等等，Tokyo 是 5）
// 实际上：Rome (4) → 只有 1 个城市的长度 <= 4
// 更正：Rome = 4 个字母 → Count 为 1

// 示例 4：先延迟再立即，链式调用
int[] nums = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
int countEvenAboveFive = nums
    .Where(n => n > 5)    // 延迟：定义过滤器
    .Count(n => n % 2 == 0); // 立即：强制执行 → 6, 8, 10 → 3
```

### 为什么这很重要

因为延迟查询在你每次遍历它们时都会重新执行，所以在多次遍历之间修改源数据可能会产生不同的结果。
像 `ToList()` 这样的立即操作符会捕获一个快照，而 `Count()` 则能立即给出答案，且不会在内存中保留任何中间集合。

### 常用参考

| 操作符 | 执行方式 | 返回值 |
| --- | --- | --- |
| `Where` | 延迟 | `IEnumerable<T>` |
| `Select` | 延迟 | `IEnumerable<T>` |
| `OrderBy` | 延迟 | `IOrderedEnumerable<T>` |
| `Count()` | 立即 | `int` |
| `Count(predicate)` | 立即 | `int` |
| `Sum()` | 立即 | 数值类型 |
| `ToList()` | 立即 | `List<T>` |
| `First()` | 立即 | `T` |
| `Any()` | 立即 | `bool` |

### 你的任务

编写一个方法，用于统计数组中有多少个单词的长度**严格大于**给定的最小长度。
使用接受 predicate 的立即 LINQ 操作符，在单个表达式中完成计数。

### 方法签名

```csharp
public static int CountLongerThan(string[] words, int minLength)
```

### 预期结果

```css
CountLongerThan(["a", "bb", "ccc", "dddd"], 2) → 2
CountLongerThan(["hello", "world"], 5) → 0
CountLongerThan(["cat", "elephant", "dog", "whale"], 3) → 2
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int CountLongerThan(string[] words, int minLength)
    {
        // 使用带谓词的 Count，立即统计长度严格大于 minLength 的单词
        return words.Count(w => w.Length > minLength);
    }
}
```
