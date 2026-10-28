### GroupBy 的结果选择器重载

当您使用 LINQ 的 `GroupBy` 时，通常会在其后链式调用 `.Select(...)` 将每个分组转换为最终结果，例如提取键、聚合值或构建汇总对象。
`GroupBy` 的**结果选择器重载**（result selector overload）允许您将该转换直接合并到分组调用本身中，从而编写出更简洁、更具声明性的代码。

其签名如下：

```csharp
GroupBy(keySelector, elementSelector, resultSelector)
```

这可以在一次调用中完成三件事：

1. **keySelector** - 决定每个元素属于哪个分组
2. **elementSelector** - 在每个元素进入分组前对其进行转换
3. **resultSelector** - 接收键和分组后的元素集合，并为每个分组生成单个结果值

### 工作原理

在没有结果选择器的情况下，`GroupBy` 返回 `IEnumerable<IGrouping<TKey, TElement>>`，通常您会链式调用 `.Select(...)` 来处理输出：

```csharp
// 两步写法
var result = items
    .GroupBy(x => x.Category, x => x.Price)
    .Select(g => new { Category = g.Key, Total = g.Sum() });
```

使用结果选择器重载，您可以将这两个步骤合并为一个：

```csharp
// 一步写法 - 效果相同，但更具声明性
var result = items
    .GroupBy(
        x => x.Category,
        x => x.Price,
        (category, prices) => new { Category = category, Total = prices.Sum() }
    );
```

两者产生完全相同的输出。
当您希望保持 LINQ 管道简洁时，结果选择器版本尤其有用。

### 语法

```csharp
source.GroupBy(
    element => /* 键表达式 */,
    element => /* 元素投影 */,
    (key, elements) => /* 每个分组的最终结果 */
)
```

第三个参数 `resultSelector` 是一个 `Func<TKey, IEnumerable<TElement>, TResult>`。
它接收：

- 当前分组的**键**（key）
- 该分组中投影元素的 **IEnumerable**

您可以对元素集合调用任何聚合方法（`.Sum()`、`.Count()`、`.Average()`、`.Min()`、`.Max()`）或任何转换操作。

### 示例

```csharp
// 示例 1：按首字母对单词分组，统计每组数量
var words = new[] { "apple", "avocado", "banana", "blueberry", "cherry" };
var counts = words.GroupBy(
    w => w[0],           // 键：首字符
    w => w,              // 元素：单词本身
    (letter, group) => $"{letter}: {group.Count()}"
);
// 结果：["a: 2", "b: 2", "c: 1"]

// 示例 2：按部门对员工分组，计算平均薪资
var employees = new[] {
    new { Name = "Li", Dept = "Eng", Salary = 95000 },
    new { Name = "Priya", Dept = "Eng", Salary = 105000 },
    new { Name = "Omar", Dept = "Sales", Salary = 72000 }
};
var summaries = employees.GroupBy(
    e => e.Dept,
    e => e.Salary,
    (dept, salaries) => $"{dept} avg: {salaries.Average():F0}"
);
// 结果：["Eng avg: 100000", "Sales avg: 72000"]

// 示例 3：按状态对订单分组，找出每种状态的最大总额
var orders = new[] {
    new { Status = "Shipped", Total = 120.50 },
    new { Status = "Pending", Total = 45.00 },
    new { Status = "Shipped", Total = 89.99 }
};
var maxPerStatus = orders.GroupBy(
    o => o.Status,
    o => o.Total,
    (status, totals) => $"{status}: {totals.Max()}"
);
// 结果：["Shipped: 120.5", "Pending: 45"]
```

### 你的任务

编写一个方法，按整数的**符号**（`"positive"`、`"negative"` 或 `"zero"`）进行分类，并计算每个分组的**总和**。
使用 `GroupBy` 的结果选择器重载为每个分组生成格式为 `"sign: sum"` 的字符串。
返回按**字母顺序**排序的结果。

例如，给定 `[1, -2, 3, -4, 0, 5]`：

- `"negative"` 分组包含 `[-2, -4]`，总和为 `-6`
- `"positive"` 分组包含 `[1, 3, 5]`，总和为 `9`
- `"zero"` 分组包含 `[0]`，总和为 `0`
- 按字母顺序排序：`["negative: -6", "positive: 9", "zero: 0"]`

### 方法签名

```csharp
public static string[] GroupSumBySign(int[] numbers)
```

### 预期结果

```scss
GroupSumBySign([1, -2, 3, -4, 0, 5]) -> ["negative: -6", "positive: 9", "zero: 0"]
GroupSumBySign([10, 20, 30])          -> ["positive: 60"]
GroupSumBySign([-1, -2, -3])          -> ["negative: -6"]
GroupSumBySign([0, 0])                -> ["zero: 0"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] GroupSumBySign(int[] numbers)
    {
        // 按符号分组，结果选择器直接生成 "sign: sum"，再按字母顺序排序
        return numbers
            .GroupBy(
                n => n > 0 ? "positive" : n < 0 ? "negative" : "zero",
                n => n,
                (sign, values) => $"{sign}: {values.Sum()}"
            )
            .OrderBy(s => s)
            .ToArray();
    }
}
```
