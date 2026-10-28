### 使用 `ToHashSet()` 物化为 HashSet

在 C# 中处理集合时，你经常需要检查某个值是否存在。
在 `List<T>` 或数组中搜索需要逐个扫描每个元素，这是一个 O(n) 操作。
如果你要执行许多此类查找，这很快就会成为瓶颈。
`HashSet<T>` 通过其 `Contains` 方法提供平均时间复杂度为 O(1) 的成员资格检查来解决此问题，从而使重复查找的速度大幅提升。

LINQ 提供了 `ToHashSet()`，只需单次调用即可将任意 `IEnumerable<T>` 物化为 `HashSet<T>`。
这种转换的一个关键副效应是**自动去重**：因为根据定义，集合（Set）不能包含重复元素，所以在构造期间任何重复的值都会被静默丢弃。

### 工作原理

当你在一个序列上调用 `ToHashSet()` 时，LINQ 会遍历每个元素并将其添加到新的 `HashSet<T>` 中。
哈希集在内部使用哈希机制，因此添加每个元素以及后续检查成员资格的平均运行时间均为 O(1)。
如果某个元素已经存在于集合中，它会被直接跳过：没有错误，也不会有重复项。
生成的 `HashSet<T>` 具有 `Count` 属性，该属性指示其中包含多少个非重复元素。

### 语法

```csharp
// 将任意 IEnumerable<T> 转换为 HashSet<T>
HashSet<T> set = source.ToHashSet();

// 可选：提供自定义的相等比较器
HashSet<string> caseInsensitive = names.ToHashSet(StringComparer.OrdinalIgnoreCase);
```

### 示例

```csharp
// 示例 1：对城市名称列表去重
string[] cities = { "Paris", "London", "Paris", "Tokyo", "London" };
HashSet<string> uniqueCities = cities.ToHashSet();
// uniqueCities 包含：{ "Paris", "London", "Tokyo" }
// uniqueCities.Count 为 3

// 示例 2：在大型数据集上进行快速成员资格检查
int[] purchasedProductIds = GetAllPurchaseHistory(); // 可能有数百万条
HashSet<int> purchasedSet = purchasedProductIds.ToHashSet();

// 现在每次 Contains 检查都是 O(1)，而不是 O(n)
bool hasBoughtWidget = purchasedSet.Contains(42); // 极快

// 示例 3：比较 ToHashSet 与 Distinct
double[] readings = { 3.14, 2.71, 3.14, 1.41, 2.71 };
// Distinct() 返回 IEnumerable<double> - 惰性的，每次都会重新求值
// ToHashSet() 返回 HashSet<double> - 已物化，O(1) 查找
HashSet<double> uniqueReadings = readings.ToHashSet();
// uniqueReadings.Count 为 3
```

### 为什么选择 ToHashSet 而不是 Distinct？

| 方法 | 返回类型 | 是否已物化？ | O(1) Contains？ |
| --- | --- | --- | --- |
| `Distinct()` | `IEnumerable<T>` | 否（延迟执行） | 否 |
| `Distinct().ToList()` | `List<T>` | 是 | 否（O(n) 扫描） |
| `ToHashSet()` | `HashSet<T>` | 是 | 是 |

如果你只需要遍历一次非重复值，`Distinct()` 就足够了。
但如果你需要非重复元素的**数量**或计划进行**重复查找**，`ToHashSet()` 则是合适的工具。

### 你的任务

编写一个方法，接收一个整数数组，并返回该数组中**唯一**（非重复）值的数量。
使用 `ToHashSet()` 将数组转换为 `HashSet<int>`，然后返回该集合中的元素数量。

### 方法签名

```csharp
public static int CountUnique(int[] numbers)
```

### 预期结果

```scss
CountUnique([1, 2, 1, 3, 2, 4, 3]) -> 4
CountUnique([5, 5, 5, 5]) -> 1
CountUnique([]) -> 0
```

### 解答

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

public class Solution
{
    public static int CountUnique(int[] numbers)
    {
        // 物化为 HashSet<int>，重复值会被自动去除
        HashSet<int> unique = numbers.ToHashSet();

        // 返回非重复元素的数量
        return unique.Count;
    }
}
```
