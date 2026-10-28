### LINQ Concat - 将序列追加在一起

在实际应用中，你经常需要将来自多个来源的数据合并到单个集合中。
也许你正在组合来自两个不同服务的搜索结果，或者合并两个日期范围内的交易记录。
LINQ 的 `Concat` 运算符为你提供了一种干净、声明式的方式来将一个序列追加到另一个序列之后。

### 工作原理

`Concat` 是一个**延迟执行**（deferred）运算符，它不会立即执行。
当你调用 `first.Concat(second)` 时，LINQ 会创建一个惰性包装器，该包装器将按原始顺序先依次产出 `first` 中的每个元素，然后再产出 `second` 中的每个元素。
不会移除、过滤或去重任何元素。
这是它与 `Union` 的关键区别，后者会消除重复项。

由于 `Concat` 保留包括重复项在内的所有元素，因此生成序列的长度始终等于两个输入序列长度的总和。

### 语法

```csharp
IEnumerable<T> result = firstSequence.Concat(secondSequence);
```

两个序列必须具有相同的元素类型 `T`。
结果是一个 `IEnumerable<T>`，可以进一步与其他 LINQ 运算符链式调用。

### 示例

```csharp
// 合并两个字符串集合
string[] morning = { "Alice", "Bob" };
string[] afternoon = { "Charlie", "Bob" };

var allVisitors = morning.Concat(afternoon);
// 结果：["Alice", "Bob", "Charlie", "Bob"]
// 注意 "Bob" 出现了两次，Concat 不会去重

// 对比会移除重复项的 Union：
var uniqueVisitors = morning.Union(afternoon);
// 结果：["Alice", "Bob", "Charlie"]
```

```csharp
// 将 Concat 与其他 LINQ 运算符链式调用
double[] q1Sales = { 150.0, 200.5, 175.0 };
double[] q2Sales = { 300.0, 125.0, 450.0 };

double totalRevenue = q1Sales.Concat(q2Sales).Sum();
// 结果：1400.5

double maxSale = q1Sales.Concat(q2Sales).Max();
// 结果：450.0
```

```csharp
// Concat 保留顺序：先是 'first' 的全部元素，然后是 'second' 的全部元素
int[] evens = { 2, 4, 6 };
int[] odds = { 1, 3, 5 };

var combined = evens.Concat(odds);
// 结果：[2, 4, 6, 1, 3, 5]
// 要获得排序后的结果，需要在 Concat 之后链式调用 OrderBy
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `a.Concat(b).ToList()` | 将两个序列合并为单个列表 |
| `a.Concat(b).Distinct()` | 合并并去除重复项 |
| `a.Concat(b).OrderBy(x => x)` | 合并并按升序排序 |
| `a.Concat(b).Where(...)` | 合并并筛选 |
| `a.Concat(b).Count()` | 统计合并后的元素数量 |

### 你的任务

编写一个方法，接收两个整数数组，使用 `Concat` 将它们组合在一起，将组合后的结果按升序排序，并返回排序后的数组。

该方法应该：

- 将 `b` 的所有元素追加到 `a` 的所有元素之后
- 将组合后的元素按升序排序
- 将结果作为 `int[]` 返回
- 保留重复项：如果某个值在两个数组中都出现，它应该在结果中出现两次

### 方法签名

```csharp
public static int[] ConcatSorted(int[] a, int[] b)
```

### 预期结果

```css
ConcatSorted([3, 1, 4], [2, 5, 0]) -> [0, 1, 2, 3, 4, 5]
ConcatSorted([5, 5], [5, 5]) -> [5, 5, 5, 5]
ConcatSorted([], [3, 1]) -> [1, 3]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ConcatSorted(int[] a, int[] b)
    {
        // 使用 Concat 合并（保留重复项），再按升序排序
        return a.Concat(b).OrderBy(x => x).ToArray();
    }
}
```
