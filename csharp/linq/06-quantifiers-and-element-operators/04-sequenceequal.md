### 使用 SequenceEqual 比较序列

在 C# 中处理集合时，你经常需要判断两个序列是否包含完全相同的元素且顺序完全一致。
`==` 运算符在此处不起作用，它检查的是数组的引用相等性，而不是内容。
LINQ 专门提供了 `SequenceEqual` 来对两个序列进行逐元素比较。

### 工作原理

`SequenceEqual` 会同时遍历两个序列，比较每对对应的元素。
**仅当**满足以下条件时，它才会返回 `true`：

1. 两个序列具有**相同数量的元素**
2. 第一个序列中位置 `i` 的每个元素都**等于**第二个序列中位置 `i` 的元素

如果任一条件不满足（长度不同或在任何位置出现不匹配），该方法会短路并返回 `false`。

### 语法

```csharp
// 基本用法 - 使用默认的相等性比较器
bool result = firstSequence.SequenceEqual(secondSequence);

// 使用自定义比较器
bool result = firstSequence.SequenceEqual(secondSequence, customComparer);
```

`SequenceEqual` 适用于任何 `IEnumerable<T>`，因此你可以将数组、列表、查询结果或任何其他可枚举类型相互进行比较。

### 示例

```csharp
// 比较两个字符串列表
var colors1 = new List<string> { "red", "green", "blue" };
var colors2 = new List<string> { "red", "green", "blue" };
colors1.SequenceEqual(colors2); // true - 元素相同，顺序相同

// 顺序很重要！
var colors3 = new List<string> { "blue", "green", "red" };
colors1.SequenceEqual(colors3); // false - 元素相同，顺序不同

// 长度很重要！
var short1 = new[] { 10, 20 };
var long1 = new[] { 10, 20, 30 };
short1.SequenceEqual(long1); // false - 长度不同

// 两个空序列被视为相等
var empty1 = Array.Empty<double>();
var empty2 = new double[] { };
empty1.SequenceEqual(empty2); // true

// 比较不同的集合类型也能正常工作
var array = new[] { 'a', 'b', 'c' };
var list = new List<char> { 'a', 'b', 'c' };
array.SequenceEqual(list); // true - 逐元素相等
```

### 常见场景

| 场景 | 结果 |
| --- | --- |
| 元素相同，顺序相同 | `true` |
| 元素相同，顺序不同 | `false` |
| 长度不同 | `false` |
| 两者均为空 | `true` |
| 一个为空，另一个不为空 | `false` |
| 各自包含单个匹配元素 | `true` |

### 你的任务

编写一个方法，接收两个整数数组，并返回它们是否包含**相同顺序的相同元素**。
使用 LINQ 的 `SequenceEqual` 来执行比较。

### 方法签名

```csharp
public static bool AreSameSequence(int[] a, int[] b)
```

### 预期结果

```css
AreSameSequence([1, 2, 3], [1, 2, 3])       -> True
AreSameSequence([1, 2, 3], [3, 2, 1])       -> False
AreSameSequence([5], [5])                     -> True
AreSameSequence([], [])                       -> True
AreSameSequence([1, 2], [1, 2, 3])           -> False
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static bool AreSameSequence(int[] a, int[] b)
    {
        // 逐元素比较两个数组，长度和顺序都必须一致
        return a.SequenceEqual(b);
    }
}
```
