### ElementAt 和 ElementAtOrDefault

在 C# 中处理序列时，你经常需要获取特定位置上的元素。
数组和列表支持使用 `[]` 直接进行索引，但 LINQ 查询的结果呢？
经过过滤或转换的序列是一个 `IEnumerable<T>`，它没有索引器。
这就是 `ElementAt` 和 `ElementAtOrDefault` 的用武之地。
它们允许你从**任何**可枚举序列中按从零开始的索引检索元素，而不仅限于具有内置索引器的集合。

### 工作原理

`ElementAt(index)` 会遍历序列，直到到达指定位置并返回该元素。
如果索引超出范围（为负数或超出了最后一个元素），它将**抛出 ArgumentOutOfRangeException**。

`ElementAtOrDefault(index)` 的行为完全相同，除了当索引超出范围时，它会返回该元素类型的**默认值**而不是抛出异常。
对于引用类型，该默认值为 `null`；对于数值类型，为 `0`；对于 `bool`，为 `false`。

这种区别非常重要：当索引*必须*有效时（并且如果不有效你希望立即报错失败），请使用 `ElementAt`；当索引超出范围是希望妥善处理的正常情况时，请使用 `ElementAtOrDefault`。

### 语法

```csharp
// 如果索引超出范围，抛出异常
T element = sequence.ElementAt(index);

// 如果索引超出范围，返回 default(T)
T element = sequence.ElementAtOrDefault(index);
```

### 示例

```csharp
// 示例 1：在过滤后的序列上使用 ElementAt
var names = new[] { "Alice", "Bob", "Charlie", "Diana" };
var longNames = names.Where(n => n.Length > 3); // "Alice", "Charlie", "Diana"
string second = longNames.ElementAt(1);          // "Charlie"

// 示例 2：使用超出范围的索引调用 ElementAtOrDefault
var scores = new[] { 90, 75, 88 };
var highScores = scores.Where(s => s > 85);       // 90, 88
int third = highScores.ElementAtOrDefault(2);      // 0（只有 2 个元素，索引 2 超出范围）

// 示例 3：ElementAt 在无效索引上抛出异常
var words = new[] { "hello", "world" };
// words.ElementAt(5); // ArgumentOutOfRangeException!
```

### 常见模式

一种常见的模式是将过滤与 `ElementAtOrDefault` 链接起来，以安全地选取第 N 个匹配的项：

```csharp
// 获取第 3 个正数，如果不足 3 个则返回 0
int result = values.Where(v => v > 0).ElementAtOrDefault(2);
```

这避免了仅仅为了通过索引获取元素而将整个过滤后的集合实例化为列表的开销。

### 实用参考

| 方法 | 遇到无效索引时的行为 | 返回类型 |
| --- | --- | --- |
| `ElementAt(int index)` | 抛出 `ArgumentOutOfRangeException` | `T` |
| `ElementAtOrDefault(int index)` | 返回 `default(T)` | `T` |

对于 `int`，`default(int)` 为 `0`。
对于 `string`，`default(string)` 为 `null`。

### 你的任务

编写一个方法，接收一个整数数组和一个索引 `k`。
过滤该数组以仅保留**偶数**，然后从该过滤后的序列中返回索引 `k`（从零开始）处的元素。
如果 `k` 超出范围（过大，或者不存在偶数），则返回 `0`。

### 方法签名

```csharp
public static int GetKthEven(int[] numbers, int k)
```

### 预期结果

```scss
GetKthEven([1, 2, 3, 4, 5, 6], 1) -> 4
GetKthEven([1, 3, 5, 7], 0) -> 0
GetKthEven([10, 20, 30], 2) -> 30
GetKthEven([2, 4, 6, 8], 5) -> 0
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int GetKthEven(int[] numbers, int k)
    {
        // 先过滤出偶数，再安全地取索引 k 处的元素，超出范围时返回 0
        return numbers.Where(n => n % 2 == 0).ElementAtOrDefault(k);
    }
}
```
