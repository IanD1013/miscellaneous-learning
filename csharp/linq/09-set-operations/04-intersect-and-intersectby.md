### Intersect 和 IntersectBy

在处理两个集合时，你经常需要找出它们共同拥有的元素。
LINQ 提供了 `Intersect` 和 `IntersectBy` 来高效地解决这一问题。
它们属于集合操作，工作原理类似于数学中的集合交集概念，仅返回同时存在于**两个**序列中的元素。

### 工作原理

`Intersect` 使用元素的默认相等性直接比较元素。
它会生成一个**去重后**的结果，即使某个元素在两个序列中多次出现，它在输出中也只会出现一次。
结果中的元素顺序遵循第一个序列中的顺序。

当你想要基于**派生键**而不是整个对象进行交集操作时，`IntersectBy` 非常有用。
你提供一个键选择器函数，如果第一个序列中元素的键与从第二个序列中提取出的任何键相匹配，该元素就会被包含在结果中。

### 语法

```csharp
// Intersect：按值查找共同元素
IEnumerable<T> result = first.Intersect(second);

// IntersectBy：按派生键查找共同元素
IEnumerable<T> result = first.IntersectBy(secondKeys, element => element.SomeProperty);
```

### 示例

```csharp
// 示例 1：基本的字符串交集
string[] teamA = { "Alice", "Bob", "Charlie", "Diana" };
string[] teamB = { "Charlie", "Diana", "Eve", "Frank" };
var bothTeams = teamA.Intersect(teamB);
// 结果：["Charlie", "Diana"]

// 示例 2：重复项会被自动移除
int[] scores1 = { 90, 85, 90, 70, 85 };
int[] scores2 = { 85, 60, 90, 50 };
var shared = scores1.Intersect(scores2);
// 结果：[90, 85]，每个值只出现一次，顺序来自 scores1

// 示例 3：带有键选择器的 IntersectBy
var employees = new[] {
    new { Name = "Alice", Department = "Engineering" },
    new { Name = "Bob", Department = "Sales" },
    new { Name = "Charlie", Department = "Marketing" }
};
string[] activeDepartments = { "Engineering", "Marketing" };
var active = employees.IntersectBy(activeDepartments, e => e.Department);
// 结果：Alice (Engineering), Charlie (Marketing)
```

### 常用模式

| 模式 | 描述 |
| --- | --- |
| `a.Intersect(b)` | 两个序列中共同拥有的元素（已去重） |
| `a.IntersectBy(keys, x => x.Prop)` | 来自 `a` 且其键存在于 `keys` 中的元素 |
| `.OrderBy(x => x)` | 按升序对结果进行排序 |
| `.ToArray()` | 将结果具体化为数组 |

注意，`Intersect` 会保留**第一个**序列中的顺序，但如果你需要特定的排序顺序，则应显式应用 `OrderBy`。

### 你的任务

编写一个方法 `CommonElements`，接收两个整型数组，并返回一个仅包含同时出现在**两个**数组中的元素的新数组。
结果应**按升序排序**且不包含重复项。

例如，给定 `[1, 2, 3, 4, 5]` 和 `[3, 4, 5, 6, 7]`，共同元素是 `3`、`4` 和 `5`，因此结果为 `[3, 4, 5]`。

### 方法签名

```csharp
public static int[] CommonElements(int[] a, int[] b)
```

### 预期结果

```css
CommonElements([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) -> [3, 4, 5]
CommonElements([10, 20, 30], [40, 50, 60]) -> []
CommonElements([5, 5, 3, 3, 1], [3, 5, 7]) -> [3, 5]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] CommonElements(int[] a, int[] b)
    {
        // 使用 Intersect 获取去重后的共同元素，再按升序排序
        return a.Intersect(b).OrderBy(x => x).ToArray();
    }
}
```
