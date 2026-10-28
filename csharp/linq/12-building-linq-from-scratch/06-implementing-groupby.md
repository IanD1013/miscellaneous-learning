### 从零开始理解分组

LINQ 的 `GroupBy` 是 C# 中最强大的操作之一，但在底层，它做的事情你也可以自己实现：遍历集合并根据键将元素累加到对应的桶（bucket）中。
理解这种内部机制能让你更深入地了解分组是如何工作的，以及何时你可能需要比 `GroupBy` 更高的控制力，例如，当你在分组过程中需要执行副作用或构建自定义数据结构时。

### 分组的内部工作原理

想象你有一堆扑克牌，想要按花色将它们分成几组。
你会一次拿一张牌浏览这堆牌。
对于每张牌，你会检查是否已经为该花色创建了一堆牌。
如果是，就把它放到那一堆中。
如果不是，就新建一堆并把牌放进去。

这正是基于字典的分组所做的事情：

1. 创建一个空的 `Dictionary<TKey, List<TValue>>`
2. 遍历每个元素
3. 计算当前元素的键
4. 如果该键在字典中不存在，则添加该键并关联一个新的空列表
5. 将元素追加到该键对应的列表中

### 语法

```csharp
// 手动创建并填充字典
var groups = new Dictionary<string, List<int>>();

foreach (var item in collection)
{
    string key = ComputeKey(item);

    if (!groups.ContainsKey(key))
    {
        groups[key] = new List<int>();
    }

    groups[key].Add(item);
}
```

### 示例

```csharp
// 示例 1：按奇偶对数字分组
var numbers = new[] { 1, 2, 3, 4, 5, 6 };
var parityGroups = new Dictionary<string, List<int>>();

foreach (var n in numbers)
{
    string key = n % 2 == 0 ? "even" : "odd";
    if (!parityGroups.ContainsKey(key))
        parityGroups[key] = new List<int>();
    parityGroups[key].Add(n);
}
// parityGroups["odd"]  -> [1, 3, 5]
// parityGroups["even"] -> [2, 4, 6]

// 示例 2：按部门对员工分组
var employees = new[] { ("Alice", "Engineering"), ("Bob", "Sales"), ("Carol", "Engineering") };
var deptGroups = new Dictionary<string, List<string>>();

foreach (var (name, dept) in employees)
{
    if (!deptGroups.ContainsKey(dept))
        deptGroups[dept] = new List<string>();
    deptGroups[dept].Add(name);
}
// deptGroups["Engineering"] -> ["Alice", "Carol"]
// deptGroups["Sales"]       -> ["Bob"]

// 示例 3：将分组投影为摘要字符串
foreach (var key in deptGroups.Keys.OrderBy(k => k))
{
    Console.WriteLine($"{key}: {deptGroups[key].Count} employees");
}
// 输出：
// Engineering: 2 employees
// Sales: 1 employees
```

### 实用参考

| 方法 / 属性 | 说明 |
| --- | --- |
| `dict.ContainsKey(key)` | 如果键存在则返回 `true` |
| `dict[key] = value` | 设置或覆盖某个键的值 |
| `dict[key].Add(item)` | 追加到存储在该键下的列表中 |
| `dict.Keys` | 返回所有键的集合 |
| `char.ToLower(c)` | 将字符转换为小写 |
| `.OrderBy(k => k)` | 按升序对序列排序 |

### 你的任务

编写一个方法，按单词的**首字母**对单词数组进行分组（不区分大小写，使用小写形式作为键）。
通过遍历单词手动构建字典。
然后生成一个格式为 `"char: count"` 的摘要字符串列表，按字符字母顺序排序。

跳过输入中任何为空或为 `null` 的字符串。
如果输入数组为空（或仅包含空字符串），则返回一个空列表。

### 方法签名

```csharp
public static List<string> GroupByFirstChar(string[] words)
```

### 预期结果

```css
GroupByFirstChar(["apple", "banana", "avocado"]) -> ["a: 2", "b: 1"]
GroupByFirstChar(["Cat", "car", "Dog"]) -> ["c: 2", "d: 1"]
GroupByFirstChar([]) -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static List<string> GroupByFirstChar(string[] words)
    {
        // 键为小写首字母，值为该组的单词列表
        var groups = new Dictionary<char, List<string>>();

        foreach (var word in words)
        {
            // 跳过 null 或空字符串
            if (string.IsNullOrEmpty(word))
                continue;

            char key = char.ToLower(word[0]);

            // 键不存在时先关联一个新的空列表
            if (!groups.ContainsKey(key))
                groups[key] = new List<string>();

            groups[key].Add(word);
        }

        // 按字符字母顺序生成 "char: count" 格式的摘要
        var result = new List<string>();
        foreach (var key in groups.Keys.OrderBy(k => k))
        {
            result.Add($"{key}: {groups[key].Count}");
        }
        return result;
    }
}
```
