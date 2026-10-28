### LINQ 聚合方法：完整的工具包

在分析数据集合时，你通常需要同时回答几个问题：有多少个元素？
总和是多少？
极值是多少？
典型值是多少？
LINQ 提供了五个核心聚合方法：`Count`、`Sum`、`Min`、`Max` 和 `Average`，每个方法只需一次调用即可回答这些问题。
在实际应用程序中，你可以使用它们来构建仪表盘、生成报表或验证数据集。

### 它们的工作原理

每个聚合方法都会遍历一个序列并将其缩减为单个值：

- **Count()** 返回元素的数量
- **Sum()** 将所有元素相加
- **Min()** 查找最小的元素
- **Max()** 查找最大的元素
- **Average()** 计算算术平均值（始终返回 `double`）

只要引入了 `System.Linq`，所有这五个方法都适用于任何 `IEnumerable<T>`。
如果在空序列上调用，它们会抛出 `InvalidOperationException`（`Count` 除外，它返回 0）。

### 语法

```csharp
int[] data = { ... };

int count   = data.Count();
int sum     = data.Sum();
int min     = data.Min();
int max     = data.Max();
double avg  = data.Average();  // 注意：即使对于 int 数组也返回 double
```

### 示例

```csharp
// 一周的温度读数
int[] temps = { 72, 68, 75, 80, 77, 65, 70 };

int readings = temps.Count();    // 7
int totalHeat = temps.Sum();     // 507
int coldest = temps.Min();       // 65
int hottest = temps.Max();       // 80
double meanTemp = temps.Average(); // 72.42857142857143

// 班级的考试成绩
int[] scores = { 88, 92, 76, 95, 81 };
Console.WriteLine($"Class average: {scores.Average():F2}"); // "Class average: 86.40"
Console.WriteLine($"Top score: {scores.Max()}");            // "Top score: 95"
```

### 格式化数值输出

在显示 `double` 值时，使用格式说明符来控制小数位数：

```csharp
double value = 3.14159;
Console.WriteLine($"{value:F2}");  // "3.14" - 定点数，2 位小数
Console.WriteLine($"{value:F0}");  // "3"    - 定点数，0 位小数
```

`F2` 格式说明符会四舍五入到恰好两位小数，并始终显示两位小数位（例如 `3.00`，而不是 `3`）。

### 字符串插值复习

你可以直接在插值字符串中嵌入表达式和格式说明符：

```csharp
double avg = 86.4;
string report = $"Average: {avg:F2}"; // "Average: 86.40"
```

### 你的任务

编写一个方法，接收一个整数数组并计算全部五个聚合值，以单个格式化字符串的形式返回它们。

输出格式必须严格为：

```yaml
Count: N, Sum: N, Min: N, Max: N, Avg: N.NN
```

其中 `N.NN` 是四舍五入到恰好两位小数的平均值。

### 方法签名

```csharp
public static string Analyze(int[] numbers)
```

### 预期结果

```rust
Analyze([1, 2, 3, 4, 5])       -> "Count: 5, Sum: 15, Min: 1, Max: 5, Avg: 3.00"
Analyze([10])                   -> "Count: 1, Sum: 10, Min: 10, Max: 10, Avg: 10.00"
Analyze([-3, 0, 3])             -> "Count: 3, Sum: 0, Min: -3, Max: 3, Avg: 0.00"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string Analyze(int[] numbers)
    {
        // 分别调用五个聚合方法，平均值用 F2 格式保留两位小数
        return $"Count: {numbers.Count()}, Sum: {numbers.Sum()}, Min: {numbers.Min()}, Max: {numbers.Max()}, Avg: {numbers.Average():F2}";
    }
}
```
