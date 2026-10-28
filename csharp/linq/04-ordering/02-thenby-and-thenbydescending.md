### 使用 ThenBy 和 ThenByDescending 进行多级排序

在实际应用中，仅按单一条件对数据进行排序往往是不够的。
想象一下对员工列表进行排序：你可能希望先按部门排序，然后在每个部门内部按姓氏排序。
LINQ 的 `ThenBy` 和 `ThenByDescending` 方法允许你定义次级（以及第三级，甚至更多级）排序键，以完美应对这类场景。

### 工作原理

当你调用 `OrderBy` 或 `OrderByDescending` 时，LINQ 会返回一个名为 `IOrderedEnumerable<T>` 的特殊类型。
该类型，且**仅**有该类型，公开了 `ThenBy` 和 `ThenByDescending` 方法。
这就是为什么你不能在普通的 `IEnumerable<T>` 或直接在集合上调用 `ThenBy`。
链式调用始终以 `OrderBy` 或 `OrderByDescending` 开始，然后你可以根据需要附加任意多个 `ThenBy` / `ThenByDescending` 调用。

次级排序键仅在两个元素具有相同的主排序键值时才会生效。
如果每个主键都是唯一的，次级排序将不会产生可见的效果。

### 语法

```csharp
// 主排序，然后次级排序
collection
    .OrderBy(item => primaryKey)
    .ThenBy(item => secondaryKey)

// 主排序降序，然后次级排序升序
collection
    .OrderByDescending(item => primaryKey)
    .ThenBy(item => secondaryKey)

// 可以链式调用多个次级排序
collection
    .OrderBy(item => firstKey)
    .ThenBy(item => secondKey)
    .ThenByDescending(item => thirdKey)
```

### 示例

```csharp
// 示例 1：按年龄对人员排序，年龄相同时再按姓名排序
var people = new[] { ("Zara", 30), ("Alice", 25), ("Bob", 30), ("Clara", 25) };

var sorted = people
    .OrderBy(p => p.Item2)   // 年龄升序：25, 25, 30, 30
    .ThenBy(p => p.Item1);   // 同一年龄内按姓名升序
// 结果：(Alice, 25), (Clara, 25), (Bob, 30), (Zara, 30)

// 示例 2：按类别升序、再按价格降序对产品排序
var products = new[] { ("Widget", "Tools", 15.0), ("Bolt", "Tools", 3.0), ("Paint", "Art", 12.0) };

var sorted2 = products
    .OrderBy(p => p.Item2)          // 类别：Art, Tools, Tools
    .ThenByDescending(p => p.Item3); // 同一类别内按价格降序
// 结果：(Paint, Art, 12.0), (Widget, Tools, 15.0), (Bolt, Tools, 3.0)

// 示例 3：三级排序 - 年，然后月，然后日
var dates = new[] { (2024, 3, 15), (2024, 1, 20), (2023, 12, 1), (2024, 1, 5) };

var sorted3 = dates
    .OrderBy(d => d.Item1)
    .ThenBy(d => d.Item2)
    .ThenBy(d => d.Item3);
// 结果：(2023,12,1), (2024,1,5), (2024,1,20), (2024,3,15)
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `.OrderBy(x => keyA).ThenBy(x => keyB)` | 均为升序 |
| `.OrderByDescending(x => keyA).ThenBy(x => keyB)` | 主排序降序，次级排序升序 |
| `.OrderBy(x => keyA).ThenByDescending(x => keyB)` | 主排序升序，次级排序降序 |
| `.OrderBy(...).ThenBy(...).ThenBy(...)` | 三级排序（全部升序） |

请记住：`ThenBy` 只能跟在 `OrderBy`、`OrderByDescending` 或另一个 `ThenBy`/`ThenByDescending` 之后。
如果你尝试在普通的 `IEnumerable` 上调用它，将无法通过编译。

### 你的任务

编写一个方法，接收一个单词数组，并按两个条件对其进行排序：

1. **主排序**：单词长度，升序（较短的单词排在前面）
2. **次级排序**：字母顺序，升序（用于长度相同的单词）

将排序后的结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] SortByLengthThenAlpha(string[] words)
```

### 预期结果

```css
SortByLengthThenAlpha(["banana", "cat", "apple", "dog", "fig"]) -> ["cat", "dog", "fig", "apple", "banana"]
SortByLengthThenAlpha(["be", "at", "I", "go"]) -> ["I", "at", "be", "go"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] SortByLengthThenAlpha(string[] words)
    {
        return words
            .OrderBy(w => w.Length)   // 主排序：长度升序
            .ThenBy(w => w)           // 次级排序：长度相同时按字母顺序升序
            .ToArray();
    }
}
```
