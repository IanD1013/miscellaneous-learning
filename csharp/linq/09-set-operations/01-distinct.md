### 使用 LINQ 的 Distinct 操作符去除重复项

在处理集合时，你经常会遇到需要消除的重复值，例如来自多个数据源的用户 ID、重复的日志条目或内容上的多余标签。
LINQ 专门为此目的提供了 `Distinct()` 操作符：它会过滤序列，使每个元素仅出现一次。

### 工作原理

`Distinct()` 是一个**延迟执行、流式处理**的操作符。
这意味着它不会预先处理整个集合。
相反，它在内部跟踪已经产出的元素。
当它遍历源序列时，会检查每个元素：

- 如果该元素之前没有出现过，它会**产出**（yield）该元素并将其记住。
- 如果该元素已经出现过，它会**跳过**（skip）该元素。

由于这种行为，`Distinct()` 会自然地**保留首次出现的顺序**。
值第一次出现的位置就是它在输出中的位置。
后续所有重复出现的值都会被静默丢弃。

默认情况下，`Distinct()` 对元素类型使用**默认相等比较器**。
对于像 `int`、`double` 和 `string` 这样的值类型，这意味着标准的值相等性比较。
对于自定义对象，你需要重写 `Equals` 和 `GetHashCode`，或者提供自定义的 `IEqualityComparer<T>`，不过那是另一个话题了。

### 语法

```csharp
// 基本用法：返回去除重复项后的 IEnumerable<T>
IEnumerable<T> unique = source.Distinct();

// 使用自定义比较器（进阶）
IEnumerable<T> unique = source.Distinct(comparer);
```

由于 `Distinct()` 返回 `IEnumerable<T>`，你通常会将其与 `.ToArray()`、`.ToList()` 或其他 LINQ 操作符链式调用。

### 示例

```csharp
// 去除重复的城市名称
string[] cities = { "Paris", "London", "Paris", "Berlin", "London", "Tokyo" };
string[] uniqueCities = cities.Distinct().ToArray();
// 结果：["Paris", "London", "Berlin", "Tokyo"]
// 注意：首次出现的顺序得到保留

// 去除评分系统中的重复分数
double[] scores = { 95.5, 87.0, 95.5, 92.0, 87.0, 87.0, 100.0 };
double[] uniqueScores = scores.Distinct().ToArray();
// 结果：[95.5, 87.0, 92.0, 100.0]

// 适用于任何 IEnumerable<T>，包括 List<T>
var statusCodes = new List<int> { 200, 404, 200, 500, 404, 301 };
var uniqueStatuses = statusCodes.Distinct().ToList();
// 结果：[200, 404, 500, 301]
```

### 常见模式

`Distinct()` 可以很好地与管道中的其他 LINQ 操作符配合使用：

```csharp
// 先过滤，再去重
var result = items.Where(x => x > 0).Distinct();

// 先去重，再排序
var sorted = items.Distinct().OrderBy(x => x);

// 统计唯一元素的数量
int uniqueCount = items.Distinct().Count();
```

### 你的任务

编写一个方法，接收一个整数数组，并返回一个仅包含**唯一值**的新数组，同时保留它们在输入中**首次出现的顺序**。

- 如果输入不包含重复项，则输出应与输入一致。
- 如果输入为空，则返回空数组。
- 如果所有元素都相同，则返回仅包含该单个元素的数组。

### 方法签名

```csharp
public static int[] UniqueValues(int[] numbers)
```

### 预期结果

```scss
UniqueValues([1, 2, 1, 3, 2, 4]) -> [1, 2, 3, 4]
UniqueValues([5, 5, 5, 5]) -> [5]
UniqueValues([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] UniqueValues(int[] numbers)
    {
        // 使用 Distinct 去除重复项，并保留首次出现的顺序
        return numbers.Distinct().ToArray();
    }
}
```
