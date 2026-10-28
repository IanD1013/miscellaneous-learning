### 使用 LINQ 进行排序和格式化：OrderByDescending、ThenBy 和 Select

在实际应用程序中，你经常需要获取原始数据，根据多个条件进行排序，然后以人类可读的格式展示它。
LINQ 提供了一条强大的方法链：`OrderByDescending`、`ThenBy` 和 `Select`，让你可以用单个、可读性高的管道来表达复杂的排序和转换逻辑。

### 工作原理

LINQ 排序是分层进行的。
`OrderByDescending` 确立了**主要**排序：它根据你指定的键将元素从高到低排列。
当多个元素具有相同的主键值时，`ThenBy` 作为**次要**排序介入以打破平局，将这些平局元素按照第二个键升序排列。
最后，`Select` 将每个排序后的元素**投影**为一个新形式，通常是一个格式化的字符串或不同的对象。

可以把它想象成整理一副扑克牌：首先按花色（主要排序），然后在每个花色内按点数（次要排序），最后写出每张牌的描述。

### 语法

```csharp
collection
    .OrderByDescending(item => item.PrimaryKey)   // 按主键降序排序
    .ThenBy(item => item.SecondaryKey)             // 平局时按次键升序排序
    .Select(item => /* 转换为新形式 */) // 投影为结果
    .ToArray();                                     // 具体化为数组
```

### 示例

```csharp
// 示例 1：按薪资降序对员工排序，薪资相同时按姓名升序
var employees = new[] {
    new { Name = "Dana", Salary = 75000 },
    new { Name = "Alex", Salary = 85000 },
    new { Name = "Casey", Salary = 75000 }
};

var sorted = employees
    .OrderByDescending(e => e.Salary)
    .ThenBy(e => e.Name)
    .Select(e => $"{e.Name}: {e.Salary:C}")
    .ToArray();
// 结果：["Alex: $85,000.00", "Casey: $75,000.00", "Dana: $75,000.00"]

// 示例 2：使用带索引的 Select 配对并行数组
string[] cities = { "Paris", "Tokyo", "London" };
int[] populations = { 2161, 13960, 8982 };

var paired = cities
    .Select((city, i) => new { City = city, Pop = populations[i] })
    .OrderByDescending(c => c.Pop)
    .Select(c => $"{c.City} ({c.Pop}K)")
    .ToArray();
// 结果：["Tokyo (13960K)", "London (8982K)", "Paris (2161K)"]

// 示例 3：带数字格式化的字符串插值
double price = 3.5;
string formatted = $"${price:F2}";  // "$3.50" - F2 表示保留 2 位小数
```

### 组合并行数组

当你的数据分布在按索引对应的多个数组中时，你可以使用带**索引重载**的 `Select` 来将它们组合起来：

```csharp
string[] labels = { "A", "B", "C" };
int[] values = { 30, 10, 20 };

var combined = labels
    .Select((label, idx) => new { Label = label, Value = values[idx] })
    .OrderBy(x => x.Value)
    .ToArray();
// 先按索引组合，再按值排序
```

### 实用参考

| 方法 | 描述 |
| --- | --- |
| `OrderByDescending(x => key)` | 按键值将元素从高到低排序 |
| `ThenBy(x => key)` | 平局元素的次要升序排序 |
| `ThenByDescending(x => key)` | 平局元素的次要降序排序 |
| `Select((x, i) => ...)` | 投影每个元素（带有可选索引） |
| `$"{value:F2}"` | 将数字格式化为精确保留 2 位小数 |

### 你的任务

编写一个方法，接收三个并行数组：`names`、`prices` 和 `quantities`，其中每个索引代表一个产品。
将它们组合起来，按**价格降序**（最高价格优先）排序，平局时按**名称升序**（按字母顺序）排序，并将每个产品格式化为：

```php
Name ($X.XX, Qty: N)
```

将结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] SortProducts(string[] names, double[] prices, int[] quantities)
```

### 预期结果

```css
SortProducts(["Apple", "Banana", "Cherry"], [1.5, 1.5, 2.0], [10, 20, 5])
  -> ["Cherry ($2.00, Qty: 5)", "Apple ($1.50, Qty: 10)", "Banana ($1.50, Qty: 20)"]

SortProducts(["Pen"], [0.99], [100])
  -> ["Pen ($0.99, Qty: 100)"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] SortProducts(string[] names, double[] prices, int[] quantities)
    {
        return names
            // 用带索引的 Select 把三个并行数组组合成一个产品对象
            .Select((name, i) => new { Name = name, Price = prices[i], Qty = quantities[i] })
            .OrderByDescending(p => p.Price)   // 主排序：价格降序
            .ThenBy(p => p.Name)               // 次要排序：名称升序
            // 先用 Math.Round 舍入到两位，再用 F2 补足两位小数
            .Select(p => $"{p.Name} (${Math.Round(p.Price, 2):F2}, Qty: {p.Qty})")
            .ToArray();
    }
}
```
