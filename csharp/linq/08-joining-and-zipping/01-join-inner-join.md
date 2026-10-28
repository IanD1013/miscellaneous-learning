### LINQ Join - 两个序列之间的内连接（Inner Joins）

在实际应用中，相关联的数据通常存放在不同的集合中。
例如，客户列表可能存在一个数组中，而他们的订单总额存在另一个数组中，并通过共享的客户 ID 进行关联。
LINQ 的 `Join` 方法允许你通过匹配公共键来组合这些集合，就像 SQL 中的 `INNER JOIN` 一样。
只有在**两个**序列中都具有匹配键的元素对才会出现在结果中。

### 工作原理

`Join` 接受四个参数：

1. **inner** - 要进行连接的第二个序列
2. **outerKeySelector** - 用于从*外部*（第一个）序列的每个元素中提取连接键的函数
3. **innerKeySelector** - 用于从*内部*（第二个）序列的每个元素中提取连接键的函数
4. **resultSelector** - 用于将匹配的外部元素和内部元素组合成结果的函数

该方法使用相等性比较键。
对于外部序列中的每个元素，它会在内部序列中查找具有相同键的所有元素，并为每个匹配项生成一个结果。
在另一侧没有匹配项的元素将被完全**排除**。

### 语法

```csharp
outerSequence.Join(
    innerSequence,
    outer => outer.KeyProperty,   // 外部元素的键
    inner => inner.KeyProperty,   // 内部元素的键
    (outer, inner) => new { ... } // 组合匹配的元素对
)
```

### 示例

假设你有按部门 ID 关联的部门和员工：

```csharp
var departments = new[] {
    new { DeptId = 1, DeptName = "Engineering" },
    new { DeptId = 2, DeptName = "Marketing" },
    new { DeptId = 3, DeptName = "Finance" }
};

var employees = new[] {
    new { Name = "Yuki", DeptId = 1 },
    new { Name = "Raj", DeptId = 2 },
    new { Name = "Lena", DeptId = 1 },
    new { Name = "Omar", DeptId = 4 }  // DeptId 4 没有匹配的部门！
};

var result = departments.Join(
    employees,
    dept => dept.DeptId,
    emp => emp.DeptId,
    (dept, emp) => $"{emp.Name} works in {dept.DeptName}"
);

// 结果：
// "Yuki works in Engineering"
// "Raj works in Marketing"
// "Lena works in Engineering"
// 注意：Omar 被排除 - 没有 Id 为 4 的部门
// 注意：Finance 被排除 - 部门 3 中没有员工
```

另一个使用简单数组和共享索引的示例：

```csharp
var cities = new[] { "Tokyo", "Paris", "Lima" };
var cityKeys = new[] { 10, 20, 30 };
var temps = new[] { 22, 18 };
var tempKeys = new[] { 20, 10 };

// 通过匹配键将城市与温度配对
var cityTemps = cities.Zip(cityKeys, (c, k) => new { City = c, Key = k });
var tempRecords = temps.Zip(tempKeys, (t, k) => new { Temp = t, Key = k });

var joined = cityTemps.Join(
    tempRecords,
    c => c.Key,
    t => t.Key,
    (c, t) => $"{c.City}: {t.Temp}°C"
);
// 结果："Tokyo: 18°C", "Paris: 22°C"
// Lima（键 30）没有匹配的温度 - 被排除
```

### 常见模式

- **并行数组**：当数据存储在通过索引或 ID 关联的独立数组中时，`Zip` 可以将每个元素与其键进行配对，然后通过 `Join` 在不同集合之间进行匹配。
- **Join 后的链式调用**：你可以在 `Join` 之后链式调用 `.OrderBy()`、`.Select()`、`.Where()` 和 `.ToArray()`，以对结果进行排序、转换、筛选或物化。
- **未匹配的元素会被丢弃**：与 `GroupJoin` 或左连接不同，`Join` 会静默排除在另一侧没有匹配项的元素。

### 你的任务

给定两个表示人员的并行数组和两个表示分数的并行数组：

- `names` 和 `nameIds`：每个人的姓名与其 ID 配对
- `scoreIds` 和 `scores`：每个分数与其所属人员的 ID 配对

根据匹配的 ID 连接这两个数据集，将每个匹配对格式化为 `"Name: Score"`，并将结果作为**按姓名升序字母排序**的 `string[]` 返回。

如果某个姓名没有匹配的分数（或者某个分数没有匹配的姓名），该元素不应出现在输出中。

### 方法签名

```csharp
public static string[] JoinNamesScores(string[] names, int[] nameIds, int[] scoreIds, int[] scores)
```

### 预期结果

```css
JoinNamesScores(["Alice", "Bob", "Carol"], [1, 2, 3], [2, 3, 1], [90, 85, 95])
  -> ["Alice: 95", "Bob: 90", "Carol: 85"]

JoinNamesScores(["Zara", "Milo"], [10, 20], [20], [100])
  -> ["Milo: 100"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] JoinNamesScores(string[] names, int[] nameIds, int[] scoreIds, int[] scores)
    {
        // 用 Zip 把并行数组配对成对象
        var people = names.Zip(nameIds, (n, id) => new { Name = n, Id = id });
        var scoreRecords = scoreIds.Zip(scores, (id, s) => new { Id = id, Score = s });

        // 按 ID 内连接，按姓名排序后格式化
        return people
            .Join(scoreRecords, p => p.Id, s => s.Id, (p, s) => new { p.Name, s.Score })
            .OrderBy(x => x.Name)
            .Select(x => $"{x.Name}: {x.Score}")
            .ToArray();
    }
}
```
