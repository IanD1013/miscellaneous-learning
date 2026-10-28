### Count 和 LongCount - 立即聚合操作符

LINQ 提供了两个强制对序列进行**立即求值**的计数操作符：`Count()` 和 `LongCount()`。
与构建查询管道的延迟操作符（如 `Where()` 或 `Select()`）不同，调用 `Count()` 会立即遍历整个序列并返回结果。
当需要知道集合的大小或有多少元素满足某个条件时，这是必不可少的，这在报表、验证和数据分析场景中非常常见。

### 工作原理

当不带参数调用 `Count()` 时，它会枚举每个元素并将总数作为 `int` 返回。
当传入一个**谓词**（predicate，即返回 `bool` 的 lambda 表达式）时，它会枚举每个元素，但只统计谓词返回 `true` 的元素。
在这两种情况下，整个序列都会被立即遍历，不存在延迟求值。

`LongCount()` 的工作方式完全相同，但返回 `long` 而不是 `int`。
当处理可能包含超过 `int.MaxValue`（2,147,483,647）个元素的序列时（例如从数据流中读取数十亿行），这非常重要。

### 语法

```csharp
// 统计所有元素
int total = source.Count();

// 统计满足条件的元素
int matching = source.Count(element => condition);

// 对非常大的序列使用 LongCount
long bigTotal = source.LongCount();
long bigMatching = source.LongCount(element => condition);
```

### 示例

```csharp
// 统计列表中的所有单词
string[] words = { "apple", "banana", "cherry", "date" };
int totalWords = words.Count();  // 4

// 统计长度超过 5 个字符的单词
int longWords = words.Count(w => w.Length > 5);
// "banana"（6）和 "cherry"（6）匹配 → 2

// 统计某个范围内的偶数
int evens = Enumerable.Range(1, 100).Count(n => n % 2 == 0);
// 50

// 在一个生成的大序列上使用 LongCount
long hugeCount = Enumerable.Range(0, int.MaxValue).LongCount();
// 2147483647（long 类型）
```

### 立即执行 vs. 延迟执行

| 操作符 | 执行方式 | 返回类型 | 作用 |
| --- | --- | --- | --- |
| `Where(predicate)` | 延迟执行 | `IEnumerable<T>` | 惰性过滤元素 |
| `Count()` | 立即执行 | `int` | 立即统计所有元素 |
| `Count(predicate)` | 立即执行 | `int` | 立即统计匹配的元素 |
| `LongCount()` | 立即执行 | `long` | 统计所有元素（适用于大序列） |
| `LongCount(predicate)` | 立即执行 | `long` | 统计匹配的元素（适用于大序列） |

由于 `Count()` 是立即执行的，在无限序列或开销极大的序列上调用它会一直阻塞，直到枚举完成。
在对大型数据集进行计数时，请注意性能问题。

### 你的任务

编写一个方法，接收一个整数数组和一个阈值，然后返回数组中**严格大于**该阈值的数字个数。
使用带有谓词的 `Count` 操作符，在单个表达式中完成此任务。

### 方法签名

```csharp
public static int CountByCondition(int[] numbers, int threshold)
```

### 预期结果

```scss
CountByCondition([1, 5, 3, 8, 2, 9], 4) → 3
CountByCondition([10, 20, 30], 25) → 1
CountByCondition([1, 2, 3], 10) → 0
CountByCondition([], 5) → 0
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int CountByCondition(int[] numbers, int threshold)
    {
        // 使用带谓词的 Count 统计严格大于阈值的元素个数
        return numbers.Count(n => n > threshold);
    }
}
```
