### 使用 Except 和 ExceptBy 计算差集

在许多实际场景中，你需要查找存在于一个集合中但不存在于另一个集合中的元素，比如找出本月未下单的客户，或者存在于本地但不存在于远程服务器上的文件。
LINQ 提供了 `Except` 和 `ExceptBy` 来简洁地计算这种**差集**。

### 工作原理

`Except` 比较两个序列，并返回存在于**第一个**序列中但**不**出现在**第二个**序列中的元素。
结果会自动进行**去重**，即使某个元素在第一个序列中多次出现，它在输出中也最多只出现一次。
第一个序列的原始顺序会得到保留。

`ExceptBy` 的工作原理类似，但允许你指定一个**键选择器**函数。
它不是比较整个元素，而是比较投影出的键。
这在处理复杂对象时非常实用。

### 语法

```csharp
// Except：直接比较元素
IEnumerable<T> result = first.Except(second);

// ExceptBy：按投影键进行比较
IEnumerable<T> result = first.ExceptBy(secondKeys, element => element.SomeProperty);
```

### 示例

```csharp
// 基础 Except：找出我们有售但竞争对手没有售卖的水果
string[] ourFruits = { "apple", "banana", "cherry", "date" };
string[] theirFruits = { "banana", "date", "fig" };

var unique = ourFruits.Except(theirFruits);
// 结果: ["apple", "cherry"]

// 第一个序列中的重复项会自动被移除
int[] scores = { 90, 85, 90, 70, 85, 60 };
int[] disqualified = { 85 };

var valid = scores.Except(disqualified);
// 结果: [90, 70, 60]  (每个元素仅出现一次，保留顺序)

// ExceptBy：排除所在部门 ID 出现在关闭列表中的员工
var employees = new[] {
    new { Name = "Alice", DeptId = 1 },
    new { Name = "Bob", DeptId = 2 },
    new { Name = "Carol", DeptId = 3 }
};
int[] closingDepts = { 2 };

var remaining = employees.ExceptBy(closingDepts, e => e.DeptId);
// 结果: [{ Name="Alice", DeptId=1 }, { Name="Carol", DeptId=3 }]
```

### 关键细节

| 行为 | 描述 |
| --- | --- |
| 去重 | 输出绝不包含重复项，即使第一个序列包含重复项 |
| 顺序 | 元素按其在第一个序列中首次出现的顺序排列 |
| 相等性 | 使用默认相等性比较器（或自定义的 `IEqualityComparer`） |
| 延迟执行 | 查询在你进行遍历或调用 `.ToArray()` / `.ToList()` 时才会执行 |

### 常见模式

- 当需要排序输出时，在 `Except` 后链式调用 `.OrderBy()`
- 链式调用 `.Count()` 来快速检查有多少项仅属于第一个集合
- 在按 ID、名称或任何单一属性比较对象时，配合 Lambda 表达式使用 `ExceptBy`

### 你的任务

编写一个名为 `Difference` 的方法，接受两个整数数组 `a` 和 `b`。
返回一个新数组，其中包含存在于 `a` 中但**不**存在于 `b` 中的元素，且**按升序排序**。

请记住，`Except` 会自动为你处理去重，但它**不会**对结果进行排序，你需要自行处理排序。

### 方法签名

```csharp
public static int[] Difference(int[] a, int[] b)
```

### 预期结果

```css
Difference([1, 2, 3, 4, 5], [2, 4])       -> [1, 3, 5]
Difference([10, 20, 30], [10, 20, 30])     -> []
Difference([5, 3, 1, 4, 2], [])            -> [1, 2, 3, 4, 5]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] Difference(int[] a, int[] b)
    {
        // 使用 Except 获取在 a 中但不在 b 中的元素（已去重），再按升序排序
        return a.Except(b).OrderBy(x => x).ToArray();
    }
}
```
