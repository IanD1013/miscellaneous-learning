### 使用 LINQ Select 投影到具名类中

当使用 LINQ 的 `Select` 转换数据时，你通常会使用匿名类型，例如 `new { X = 1, Y = 2 }` 这样的快速内联对象。
它们在单个方法内部非常方便，但存在一个重大限制：你**不能从方法中返回匿名类型**，也无法将其存储在其他代码可以使用的强类型集合中。
对于跨越方法边界的任何数据形态，你都需要一个**具名类**。

定义一个小型类来保存投影数据是 C# 中的常见模式，尤其是在 API、视图模型和数据管道中。

### 工作原理

`Select` 将序列中的每个元素转换为新的形式。
当新形式是具名类的实例时，你可以在 lambda 表达式中使用**对象初始值设定项语法**：

```csharp
collection.Select(item => new MyClass { Property1 = ..., Property2 = ... })
```

LINQ 还提供了 `Select` 的**带索引重载**，其中 lambda 表达式同时接收元素及其从零开始的索引：

```csharp
collection.Select((item, index) => /* 使用 item 和 index */)
```

当你需要将某个元素与另一个集合中处于相同位置的数据关联起来时，这非常有用。

### 语法

```csharp
// 具名类定义
public class Product
{
    public string Title { get; set; }
    public decimal Price { get; set; }
}

// 带索引的 Select - (element, index) 重载
var results = source.Select((element, i) => new Product
{
    Title = element,
    Price = prices[i]
});
```

### 示例

```csharp
// 示例 1：将城市名称和人口投影到具名类中
public class CityInfo
{
    public string City { get; set; }
    public int Population { get; set; }
}

string[] cities = { "Oslo", "Bergen" };
int[] pops = { 700000, 285000 };

CityInfo[] infos = cities
    .Select((city, i) => new CityInfo { City = city, Population = pops[i] })
    .ToArray();
// infos[0] => CityInfo { City = "Oslo", Population = 700000 }

// 示例 2：链式调用第二个 Select 来格式化投影出的对象
string[] labels = infos
    .Select(c => $"{c.City}: {c.Population} people")
    .ToArray();
// ["Oslo: 700000 people", "Bergen: 285000 people"]

// 示例 3：不使用具名类的带索引 Select（用于对比）
string[] numbered = cities
    .Select((city, i) => $"{i + 1}. {city}")
    .ToArray();
// ["1. Oslo", "2. Bergen"]
```

### 链式调用 Select

你可以链式调用多个 `Select` 来分离关注点。
第一个 `Select` 创建结构化对象，后续的 `Select` 则对其进行进一步的格式化或转换。
这样可以使每个步骤专注于单一职责。

### 你的任务

1. **定义一个类** `Person`（在 `Solution` 类外部），包含两个公共属性：

   - `string Name`
   - `int Age`
2. **实现** `CreatePersonSummaries` 方法，该方法接收长度相等的并行数组 `names` 和 `ages`。
   该方法应：

   - 使用**带索引的 `Select`** 将每个姓名-年龄对投影为一个 `Person` 实例。
   - 链式调用**第二个 `Select`**，将每个 `Person` 格式化为字符串 `"{Name} is {Age} years old"`。
   - 以 `string[]` 形式返回结果。

### 方法签名

```csharp
public static string[] CreatePersonSummaries(string[] names, int[] ages)
```

### 预期结果

```css
CreatePersonSummaries(["Alice", "Bob"], [30, 25])
  -> ["Alice is 30 years old", "Bob is 25 years old"]

CreatePersonSummaries(["Zara"], [1])
  -> ["Zara is 1 years old"]

CreatePersonSummaries([], [])
  -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Person
{
    // 姓名和年龄两个公共属性
    public string Name { get; set; }
    public int Age { get; set; }
}

public class Solution
{
    public static string[] CreatePersonSummaries(string[] names, int[] ages)
    {
        return names
            // 用带索引的 Select 把每个姓名-年龄对投影为 Person
            .Select((name, i) => new Person { Name = name, Age = ages[i] })
            // 第二个 Select 把每个 Person 格式化为字符串
            .Select(p => $"{p.Name} is {p.Age} years old")
            .ToArray();
    }
}
```
