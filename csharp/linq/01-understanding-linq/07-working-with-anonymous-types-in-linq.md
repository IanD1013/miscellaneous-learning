### 使用匿名类型投影数据

在处理 LINQ 管道时，您经常需要将数据重塑为临时结构：合并字段、计算值或配对相关信息。
匿名类型允许您在不定义专用类的情况下动态创建这些中间结构。
它们在管道内部尤其有用，因为在该场景下，这些结构只需在几个步骤中使用，然后就会转换为最终输出。

### 工作原理

匿名类型是使用 `new { ... }` 语法创建的。
编译器在后台生成一个带有与您指定的属性相匹配的只读属性的类。
因为该类型没有可以在代码中引用的名称，所以匿名类型非常适合方法内的**中间步骤**，但它们不能直接从方法返回或跨方法边界传递。
在管道的末尾，您通常会将它们投影为字符串、具名类型或其他具体值。

### 语法

```csharp
// 创建一个匿名类型
var item = new { ProductName = "Widget", Price = 9.99 };
Console.WriteLine(item.ProductName); // "Widget"
Console.WriteLine(item.Price);       // 9.99

// 使用带索引参数的 Select
collection.Select((element, index) => /* 同时使用元素和索引 */)
```

提供索引参数的 `Select` 重载在需要将一个集合中的元素与另一个集合中相同位置的元素进行关联时特别有用。

### 示例

```csharp
// 示例 1：将产品投影为匿名类型，再转换为字符串
string[] products = { "Laptop", "Mouse", "Keyboard" };
double[] prices = { 999.99, 29.99, 79.99 };

var result = products
    .Select((product, i) => new { Product = product, Price = prices[i] })
    .Select(item => $"{item.Product}: ${item.Price}")
    .ToArray();
// result: ["Laptop: $999.99", "Mouse: $29.99", "Keyboard: $79.99"]

// 示例 2：使用中间匿名类型将城市与人口配对
string[] cities = { "Tokyo", "Paris" };
int[] populations = { 14000000, 2100000 };

var summaries = cities
    .Select((city, i) => new { City = city, Pop = populations[i] })
    .Select(c => $"{c.City} has {c.Pop} people")
    .ToArray();
// summaries: ["Tokyo has 14000000 people", "Paris has 2100000 people"]
```

请注意这种模式：第一个 `Select` 创建匿名类型以合并相关数据，第二个 `Select` 将其转换为最终输出格式。
您也可以在单个 `Select` 中完成此操作，但将步骤分开可以使意图更清晰，并展示匿名类型如何充当中间结构。

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `Select((item, index) => ...)` | 访问元素及其从零开始的索引 |
| `new { Prop1 = val1, Prop2 = val2 }` | 创建带有具名属性的匿名类型 |
| 链式调用两次 `.Select(...)` | 首先塑形，然后转换为最终输出 |
| 在末尾使用 `.ToArray()` | 将 LINQ 查询具体化为具体的数组 |

### 您的任务

编写一个方法，接收两个数组（一个是姓名数组，另一个是年龄数组），并将每个姓名与相应的年龄（位于相同索引处）配对。
使用带有索引的 `Select` 投影为匿名类型，然后将每个配对格式化为模式为 `"Name (Age)"` 的字符串。
以 `string[]` 形式返回结果。

### 方法签名

```csharp
public static string[] FormatPersons(string[] names, int[] ages)
```

### 预期结果

```css
FormatPersons(["Alice", "Bob"], [30, 25]) -> ["Alice (30)", "Bob (25)"]
FormatPersons(["Zara"], [1]) -> ["Zara (1)"]
FormatPersons([], []) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FormatPersons(string[] names, int[] ages)
    {
        return names
            .Select((name, i) => new { Name = name, Age = ages[i] }) // 按相同索引配对为匿名类型
            .Select(p => $"{p.Name} ({p.Age})")                      // 格式化为 "Name (Age)"
            .ToArray();
    }
}
```
