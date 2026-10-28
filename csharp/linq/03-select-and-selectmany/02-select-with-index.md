### Select 的索引重载

LINQ 的 `Select` 方法通常用于转换集合中的每个元素。
但如果你还需要知道每个元素在序列中的*位置*呢？
`Select` 的**索引重载**（indexed overload）可以同时为你提供元素及其从零开始的索引位置。
这在为条目编号、构建排名列表、根据位置创建格式化输出或将数据与位置元数据交错结合时非常有用。

### 工作原理

标准的 `Select` 接受一个带有一个参数的 Lambda 表达式，即当前元素。
而索引重载接受带有**两个**参数的 Lambda 表达式：元素及其索引。
第一个元素的索引从 `0` 开始，后续每个元素递增 1，就像数组索引一样。

### 语法

```csharp
// 标准 Select - 仅元素
collection.Select(element => transform(element))

// 带索引的 Select - 元素及其位置
collection.Select((element, index) => transform(element, index))
```

第二个参数始终是一个 `int`，表示该元素在源序列中从零开始的位置。

### 示例

```csharp
// 示例 1：创建一个带编号的城市列表
string[] cities = { "Tokyo", "London", "Sydney" };
var numbered = cities.Select((city, i) => $"#{i + 1} {city}").ToArray();
// 结果：["#1 Tokyo", "#2 London", "#3 Sydney"]

// 示例 2：标记处于偶数位置的分数
int[] scores = { 90, 85, 78, 92 };
var tagged = scores.Select((score, i) => i % 2 == 0 ? $"{score} (even pos)" : $"{score} (odd pos)").ToArray();
// 结果：["90 (even pos)", "85 (odd pos)", "78 (even pos)", "92 (odd pos)"]

// 示例 3：将每个数字乘以它的位置
int[] values = { 10, 20, 30, 40 };
var products = values.Select((val, i) => val * i).ToArray();
// 结果：[0, 20, 60, 120]
```

请注意，在每个示例中，索引如何带来了更多的转换可能性，而使用普通的 `foreach` 循环和手动计数器来实现这些转换往往会显得笨拙或冗长。

### 常见模式

| 模式 | Lambda 形式 | 使用场景 |
| --- | --- | --- |
| 编号 | `(el, i) => $"{i}: {el}"` | 显示带有位置的列表 |
| 按位置进行条件判断 | `(el, i) => i % 2 == 0 ? ... : ...` | 隔行交替样式 |
| 加权计算 | `(el, i) => el * (i + 1)` | 基于位置的加权 |
| 按位置过滤 | `.Where((el, i) => i < 3)` | 获取前 N 项（Where 也有索引重载！） |

### 你的任务

编写一个方法，接受一个单词数组，并返回一个新数组，其中每个单词都带有其从零开始的位置前缀，格式为 `"N: word"`。
冒号后面有一个空格。

例如，给定 `["red", "green", "blue"]`，结果应为 `["0: red", "1: green", "2: blue"]`。

### 方法签名

```csharp
public static string[] AddIndex(string[] words)
```

### 预期结果

```css
AddIndex(["apple", "banana", "cherry"]) -> ["0: apple", "1: banana", "2: cherry"]
AddIndex(["solo"]) -> ["0: solo"]
AddIndex([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] AddIndex(string[] words)
    {
        // 使用带索引的 Select，把位置作为前缀拼接到每个单词前面
        return words.Select((word, i) => $"{i}: {word}").ToArray();
    }
}
```
