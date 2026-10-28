### LINQ Average 运算符

`Average()` 计算数值序列的算术平均值，无论源序列包含 `int`、`long`、`float` 还是 `decimal` 值，它始终返回 `double`。
这使得它成为从集合中获取平均值的首选运算符，例如计算平均分、平均响应时间、平均订单总额以及类似的聚合操作。

需要记住的一个关键行为：在**空**序列上调用 `Average()` 会抛出 `InvalidOperationException`。
如果你的代码中可能出现空序列，则需要在调用 `Average()` 之前处理这种情况。

### 工作原理

`Average()` 对序列中的所有元素求和并除以元素个数。
与 `Sum()` 一样，它提供了两个重载：

1. **直接求平均值** - 适用于数值类型的序列（`IEnumerable<int>`、`IEnumerable<double>` 等）
2. **投影重载** - 接受一个选择器函数，从每个元素中提取数值，这样你就可以直接对某个属性求平均值，而无需先投影到单独的数值序列中。

### 语法

```csharp
// 直接方式：对数字序列求平均值
double mean = numbers.Average();

// 投影方式：对从每个元素计算出的值求平均值
double mean = collection.Average(item => item.SomeNumericProperty);
```

### 示例

```csharp
// 整数的平均值 - 注意结果始终是 double
int[] scores = { 85, 90, 78, 92 };
double avgScore = scores.Average(); // 86.25

// 投影：计算产品列表的平均价格
var products = new[] {
    new { Name = "Pen", Price = 1.50 },
    new { Name = "Notebook", Price = 4.99 },
    new { Name = "Eraser", Price = 0.75 }
};
double avgPrice = products.Average(p => p.Price); // 2.4133...

// 四舍五入到 2 位小数
double rounded = Math.Round(avgPrice, 2); // 2.41

// 小心空序列！
int[] empty = { };
// empty.Average(); // 抛出 InvalidOperationException！
```

### 常用参考

| 方法 / 特性 | 说明 | 返回类型 |
| --- | --- | --- |
| `sequence.Average()` | 数值元素的平均值 | `double` |
| `sequence.Average(selector)` | 投影数值的平均值 | `double` |
| `Math.Round(value, digits)` | 四舍五入到指定小数位数 | `double` |
| 空序列行为 | 抛出 `InvalidOperationException` | - |

### 你的任务

编写一个方法，接受一个单词数组并计算**平均单词长度**（每个单词的字符数）。
返回**保留 2 位小数**的结果。

如果数组为空，该方法应抛出 `InvalidOperationException`（这正是 `Average()` 在空序列上的默认行为，你无需为此添加特殊处理）。

### 方法签名

```csharp
public static double AverageWordLength(string[] words)
```

### 预期结果

```css
AverageWordLength(["cat", "dog", "bird"]) -> 3.33
AverageWordLength(["hello"]) -> 5.0
AverageWordLength(["a", "bb", "ccc", "dddd"]) -> 2.5
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static double AverageWordLength(string[] words)
    {
        // 使用带选择器的 Average 计算平均单词长度，并四舍五入到 2 位小数
        // 空数组时 Average() 会自动抛出 InvalidOperationException
        return Math.Round(words.Average(w => w.Length), 2);
    }
}
```
