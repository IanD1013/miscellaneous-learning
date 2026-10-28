### 使用 `Contains` 进行成员资格测试

编程中最常见的任务之一就是检查集合中是否包含某个特定元素。
LINQ 的 `Contains` 方法提供了一种简洁且富有表现力的方式来执行此成员资格测试。
除了简单的相等性检查外，`Contains` 还支持自定义比较逻辑，这使得它在默认相等性规则不符合需求的情况下非常强大。

### 工作原理

默认情况下，`Contains(value)` 使用该类型的默认相等性比较器。
对于字符串，这意味着**精确、区分大小写**的匹配。
因此 `"Hello"` 和 `"hello"` 会被视为不同的值。

但是，`Contains` 还有第二个重载：`Contains(value, comparer)`。
它接受一个 `IEqualityComparer<T>`，用于定义判断是否“相等”的自定义规则。
这对于字符串特别有用，因为你可能需要进行不区分大小写的匹配、区分区域文化的比较或其他特殊行为。

### 语法

```csharp
// 默认相等性（对字符串区分大小写）
bool found = collection.Contains(value);

// 使用比较器的自定义相等性
bool found = collection.Contains(value, comparer);
```

### 示例

```csharp
// 示例 1：默认的 Contains - 区分大小写
var colors = new[] { "Red", "Green", "Blue" };
bool hasRed = colors.Contains("Red");    // true
bool hasred = colors.Contains("red");    // false - 大小写不匹配！

// 示例 2：使用 StringComparer 进行不区分大小写的匹配
var cities = new[] { "Paris", "London", "Tokyo" };
bool hasTokyo = cities.Contains("tokyo", StringComparer.OrdinalIgnoreCase); // true
bool hasBerlin = cities.Contains("BERLIN", StringComparer.OrdinalIgnoreCase); // false - 不在列表中

// 示例 3：对整数使用 Contains（默认比较器即可正常工作）
var numbers = new[] { 10, 20, 30, 40 };
bool has20 = numbers.Contains(20);  // true
bool has25 = numbers.Contains(25);  // false
```

### 常用的字符串比较器

| 比较器 | 描述 |
| --- | --- |
| `StringComparer.Ordinal` | 逐字节比较（区分大小写） |
| `StringComparer.OrdinalIgnoreCase` | 逐字节比较（忽略大小写） |
| `StringComparer.CurrentCulture` | 区域感知，区分大小写 |
| `StringComparer.CurrentCultureIgnoreCase` | 区域感知，忽略大小写 |
| `StringComparer.InvariantCultureIgnoreCase` | 区域不变（Invariant culture），忽略大小写 |

对于大多数非语言学相关的比较（标识符、代码、关键字），推荐使用 `OrdinalIgnoreCase`，因为它快速且结果可预测。

### 你的任务

编写一个方法，检查给定的目标单词是否存在于单词数组中，**无论字母大小写如何**。
比较时应将 `"Apple"`、`"APPLE"` 和 `"apple"` 视为相同的单词。

如果找到了目标单词（不区分大小写），则返回 `true`，否则返回 `false`。

### 方法签名

```csharp
public static bool ContainsIgnoreCase(string[] words, string target)
```

### 预期结果

```graphql
ContainsIgnoreCase(["Apple", "Banana", "Cherry"], "apple") -> True
ContainsIgnoreCase(["Apple", "Banana", "Cherry"], "BANANA") -> True
ContainsIgnoreCase(["Apple", "Banana", "Cherry"], "Grape") -> False
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static bool ContainsIgnoreCase(string[] words, string target)
    {
        // 使用 OrdinalIgnoreCase 比较器进行不区分大小写的成员资格测试
        return words.Contains(target, StringComparer.OrdinalIgnoreCase);
    }
}
```
