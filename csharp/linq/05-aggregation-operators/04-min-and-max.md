### Min 和 Max 聚合操作符

LINQ 提供了 `Min()` 和 `Max()` 来查找序列中的最小值和最大值。
这些是聚合操作符（aggregation operators），它们将一个集合归约为单个值。
在处理数值数据时，你会经常用到它们：查找价格极值、温度界限、日期范围等等。

### 它们的工作原理

`Min()` 扫描序列中的每个元素并返回最小值。
`Max()` 则相反，它返回最大值。
两者都会遍历整个集合一次，因此它们的时间复杂度为 O(n)。

**重要提示：** 如果序列为空，`Min()` 和 `Max()` 都会抛出 `InvalidOperationException`。
因为不存在“空序列的最小值”，你至少需要一个元素。

### 语法

```csharp
// 不带选择器 - 直接作用于数值序列
int smallest = sequence.Min();
int largest = sequence.Max();

// 带有投影选择器 - 从每个元素中提取一个值
double cheapest = products.Min(p => p.Price);
double mostExpensive = products.Max(p => p.Price);
```

无参数重载适用于 `int`、`double`、`decimal`、`float`、`long` 以及它们各自的可空版本的序列。
选择器重载适用于任何序列：你提供一个 lambda 表达式来告诉 LINQ 比较哪个数值属性。

### 示例

```csharp
// 在简单数值集合中查找极值
double[] temperatures = { 72.1, 68.5, 81.3, 59.9, 74.0 };
double coldest = temperatures.Min();   // 59.9
double hottest = temperatures.Max();   // 81.3

// 在对象上使用选择器
var employees = new[] {
    new { Name = "Ava", Salary = 62000 },
    new { Name = "Ben", Salary = 78000 },
    new { Name = "Cora", Salary = 55000 }
};
int lowestSalary = employees.Min(e => e.Salary);   // 55000
int highestSalary = employees.Max(e => e.Salary);  // 78000

// 结合使用 Min 和 Max 来查找极差（spread）
int[] scores = { 88, 92, 75, 100, 63 };
int spread = scores.Max() - scores.Min();  // 100 - 63 = 37
```

### 常用模式

| 模式 | 示例 | 结果 |
| --- | --- | --- |
| 最小元素 | `nums.Min()` | 单个值 |
| 最大元素 | `nums.Max()` | 单个值 |
| 投影最小值 | `items.Min(x => x.Value)` | 单个投影值 |
| 投影最大值 | `items.Max(x => x.Value)` | 单个投影值 |
| 范围（极差） | `nums.Max() - nums.Min()` | 差值 |

### 你的任务

编写一个方法来计算整数数组的**极差（range）**。
极差定义为数组中最大值与最小值之间的差值。

例如，给定 `[3, 1, 4, 1, 5, 9, 2, 6]`，最大值是 `9`，最小值是 `1`，因此极差为 `9 - 1 = 8`。

你可以假设数组中始终包含至少一个元素。

### 方法签名

```csharp
public static int GetRange(int[] numbers)
```

### 预期结果

```scss
GetRange([3, 1, 4, 1, 5, 9, 2, 6]) -> 8
GetRange([5]) -> 0
GetRange([10, 20]) -> 10
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int GetRange(int[] numbers)
    {
        // 极差 = 最大值 - 最小值
        return numbers.Max() - numbers.Min();
    }
}
```
