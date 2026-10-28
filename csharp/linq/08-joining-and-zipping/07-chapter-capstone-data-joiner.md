### 在 LINQ 中结合使用 Join、GroupBy 和 Sum

真实世界中的数据很少存在于单个集合中。
你通常需要将相关的数据集**连接**（join）在一起，按共享的键对合并后的结果进行**分组（group）**，然后对每个组内的值进行**聚合（aggregate）**。
这个综合练习将三个核心的 LINQ 操作整合到一个工作流中，这种数据管道常用于生成报表、仪表板或汇总数据。

### 工作原理

该管道包含三个阶段：

1. **Join** - `Join` 根据匹配的键配对来自两个序列的元素，类似于 SQL 中的 INNER JOIN。只有在两个序列中都具有匹配键的元素才会出现在输出中。
2. **GroupBy** - 连接之后，你可以按共同的属性对配对的结果进行分组，从而将相关记录收集在一起。
3. **Sum** - 在每个组内，你可以使用 `Sum` 计算聚合值（在本例中为总和）。

### 语法

```csharp
// Join：配对外部和内部中键匹配的元素
outer.Join(inner,
    outerElement => outerElement.Key,   // 外部的键选择器
    innerElement => innerElement.Key,   // 内部的键选择器
    (outerEl, innerEl) => new { ... })  // 结果选择器

// GroupBy：按键对元素进行分组
sequence.GroupBy(element => element.SomeProperty)

// Sum：计算每个组内的总和
group.Sum(element => element.NumericProperty)
```

### 示例

```csharp
// 示例 1：将部门与员工连接
string[] departments = { "Engineering", "Sales" };
var employees = new[] {
    new { Dept = "Engineering", Name = "Ada", Salary = 95000.0 },
    new { Dept = "Sales", Name = "Bob", Salary = 72000.0 },
    new { Dept = "Engineering", Name = "Carol", Salary = 102000.0 }
};

var joined = departments.Join(employees,
    d => d,
    e => e.Dept,
    (d, e) => new { Department = d, e.Salary });
// 结果：Engineering/95000, Sales/72000, Engineering/102000

// 示例 2：连接后进行分组和求和
var summary = joined
    .GroupBy(x => x.Department)
    .Select(g => new { Dept = g.Key, TotalSalary = g.Sum(x => x.Salary) })
    .OrderBy(x => x.Dept);
// 结果：Engineering -> 197000, Sales -> 72000

// 示例 3：格式化输出
var lines = summary.Select(x => $"{x.Dept}: ${x.TotalSalary:F2}");
// 结果：["Engineering: $197000.00", "Sales: $72000.00"]
```

### 常见模式

| 操作 | 目的 | 关键要点 |
| --- | --- | --- |
| `Join` | 按键合并两个序列 | 仅包含匹配的键（内连接） |
| `GroupBy` | 收集相关项 | 返回带有 `.Key` 的 `IGrouping<TKey, TElement>` |
| `Sum` | 聚合数值 | 通过 `g.Sum(...)` 作用于每个组 |
| `OrderBy` | 对结果排序 | 在分组后应用以获得确定性输出 |
| `$"{value:F2}"` | 格式化 double 值 | 精确显示 2 位小数 |

### 你的任务

你将获得四个表示产品目录的并行数组：

- `categories` - 有效分类名称的列表（例如 `["Electronics", "Books"]`）
- `itemCategories` - 每个物品所属的分类（与 `itemNames` 和 `itemPrices` 并行）
- `itemNames` - 每个物品的名称
- `itemPrices` - 每个物品的价格

编写一个方法：

1. 将物品**连接**（Join）到有效分类中（仅当物品的分类存在于 `categories` 中时才应出现）
2. 按分类名称对连接后的结果进行**分组（Group）**
3. 对每个组内的价格进行**求和（Sum）**
4. 返回格式化为 `"CategoryName: Total=$X.XX"` 的字符串数组，并按分类名称**按字母顺序排序**

没有匹配物品的分类**不应**出现在输出中（这是内连接后进行分组的默认行为）。

### 方法签名

```csharp
public static string[] JoinAndSummarize(string[] categories, string[] itemCategories, string[] itemNames, double[] itemPrices)
```

### 预期结果

```css
JoinAndSummarize(["A", "B"], ["A", "B", "A", "B"], ["a1", "b1", "a2", "b2"], [1.0, 2.0, 3.0, 4.0])
  -> ["A: Total=$4.00", "B: Total=$6.00"]

JoinAndSummarize(["X"], ["X", "Y", "X"], ["x1", "y1", "x2"], [10.5, 20.0, 5.5])
  -> ["X: Total=$16.00"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] JoinAndSummarize(string[] categories, string[] itemCategories, string[] itemNames, double[] itemPrices)
    {
        // 用 Zip 把物品的分类、名称和价格组合成对象
        var items = itemCategories
            .Zip(itemNames, (c, n) => new { Category = c, Name = n })
            .Zip(itemPrices, (x, p) => new { x.Category, x.Name, Price = p });

        // 内连接到有效分类，按分类分组求和，按分类名称排序后格式化
        return categories
            .Join(items, c => c, i => i.Category, (c, i) => new { Category = c, i.Price })
            .GroupBy(x => x.Category)
            .OrderBy(g => g.Key)
            .Select(g => $"{g.Key}: Total=${g.Sum(x => x.Price):F2}")
            .ToArray();
    }
}
```
