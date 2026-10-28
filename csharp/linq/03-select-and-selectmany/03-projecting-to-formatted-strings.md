### 使用 Select 和索引投影配对数据

在实际应用程序中，相关数据通常存储在按位置对应的不同集合中。
例如，你可能有一个员工姓名数组和另一个员工薪资数组，或者一个城市名称列表和另一个城市人口列表。
LINQ 的 `Select` 方法提供了一个包含每个元素**索引**的重载，使你能够访问第二个集合中相同位置的元素，从而逐个元素地有效合并两个并行数组。

这是在学习 `Zip`（它能更优雅地完成相同操作）之前你会遇到的一个常见且实用的模式。
理解带索引的 `Select` 为思考逐元素转换打下了坚实的基础。

### 工作原理

标准的 `Select` 转换序列中的每个元素：

```csharp
collection.Select(element => /* 转换元素 */)
```

但 `Select` 还有一个重载，它会在传入每个元素的同时传入**从零开始的索引**：

```csharp
collection.Select((element, index) => /* 同时使用元素和索引 */)
```

有了索引，你就可以使用 `secondArray[index]` 在第二个数组中查找对应的值，并以任意你喜欢的方式组合这两部分数据。

### 语法

```csharp
// Select 的索引重载
var result = sourceArray.Select((item, i) => /* 使用 item 和 i 的表达式 */);
```

Lambda 表达式接收两个参数：

- `item` - 来自源集合的当前元素
- `i` - 该元素从零开始的位置索引

### 示例

```csharp
// 示例 1：将学生姓名与其分数组合
string[] students = { "Alice", "Bob", "Charlie" };
int[] scores = { 92, 85, 78 };

var report = students.Select((name, i) => $"{name} scored {scores[i]}").ToArray();
// ["Alice scored 92", "Bob scored 85", "Charlie scored 78"]

// 示例 2：为列表中的每一项编号
string[] colors = { "Red", "Green", "Blue" };

var numbered = colors.Select((color, i) => $"{i + 1}. {color}").ToArray();
// ["1. Red", "2. Green", "3. Blue"]

// 示例 3：根据数量和单价计算总价
int[] quantities = { 3, 1, 5 };
double[] unitPrices = { 12.50, 45.00, 3.75 };

var totals = quantities.Select((qty, i) => qty * unitPrices[i]).ToArray();
// [37.5, 45.0, 18.75]
```

### 字符串格式化提示

在格式化货币值时，`F2` 格式说明符可确保精确保留两位小数：

```csharp
double price = 3.5;
string formatted = $"${price:F2}";  // "$3.50"

double whole = 10.0;
string formatted2 = $"${whole:F2}"; // "$10.00"
```

### 你的任务

编写一个方法，接收两个并行数组：`names`（产品名称）和 `prices`（产品价格），并返回一个新的 `string[]`，其中每个元素按以下格式组合名称和价格：

```bash
Name: $X.XX
```

价格必须始终显示精确的两位小数。
第一个名称与第一个价格配对，第二个名称与第二个价格配对，依此类推。

### 方法签名

```csharp
public static string[] FormatProducts(string[] names, double[] prices)
```

### 预期结果

```css
FormatProducts(["Apple", "Banana"], [1.5, 0.75]) -> ["Apple: $1.50", "Banana: $0.75"]
FormatProducts(["Widget"], [9.99])                -> ["Widget: $9.99"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FormatProducts(string[] names, double[] prices)
    {
        // 用带索引的 Select 取出同一位置的价格，先用 Math.Round 舍入到两位，再用 F2 补足两位小数
        return names.Select((name, i) => $"{name}: ${Math.Round(prices[i], 2):F2}").ToArray();
    }
}
```
