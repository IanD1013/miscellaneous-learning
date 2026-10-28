### 嵌套 GroupBy 实现双层分组

在实际的数据处理中，您经常需要沿多个维度对数据进行分类。
例如，您可能先按部门对员工进行分组，然后在其各自部门内按资历级别进行分组。
LINQ 的 `GroupBy` 可以应用于多个层级以构建此类分层分组。

### 工作原理

第一次调用 `GroupBy` 会生成一个分组集合，其中每个分组都有一个 `Key` 并包含匹配的元素。
然后，您可以进一步处理每个外层分组，包括对该分组内的元素再次调用 `GroupBy`。
这创建了一个两层层级结构：外层分组和内层子分组。

关键点在于每个外层分组（`IGrouping<TKey, TElement>`）本身就是一个 `IEnumerable<TElement>`，因此您可以在其上使用任何 LINQ 方法，包括另一个 `GroupBy`。

### 语法

```csharp
// 外层分组
var outerGroups = items.GroupBy(item => outerKeySelector);

// 对每个外层分组进行内层分组处理
var results = outerGroups.Select(outerGroup =>
{
    var innerGroups = outerGroup.GroupBy(item => innerKeySelector);
    // 按需分析 innerGroups
    return someResult;
});
```

### 示例

假设您有一个包含部门和年级的学生列表：

```csharp
var students = new[] {
    new { Name = "Alice", Dept = "CS", Year = 1 },
    new { Name = "Bob", Dept = "CS", Year = 2 },
    new { Name = "Carol", Dept = "Math", Year = 1 },
    new { Name = "Dan", Dept = "CS", Year = 1 },
    new { Name = "Eve", Dept = "Math", Year = 2 }
};

// 外层：按部门分组
// 内层：在每个部门内按年级分组
var report = students
    .GroupBy(s => s.Dept)
    .OrderBy(g => g.Key)
    .Select(deptGroup =>
    {
        var byYear = deptGroup.GroupBy(s => s.Year);
        var year1Count = byYear
            .Where(yg => yg.Key == 1)
            .Select(yg => yg.Count())
            .FirstOrDefault();
        var year2Count = byYear
            .Where(yg => yg.Key == 2)
            .Select(yg => yg.Count())
            .FirstOrDefault();
        return $"{deptGroup.Key}: Y1={year1Count} Y2={year2Count}";
    })
    .ToArray();
// 结果：["CS: Y1=2 Y2=1", "Math: Y1=1 Y2=1"]
```

另一个示例：按区域对销售额进行分组，然后按销售额是否超过阈值进行分组：

```csharp
var sales = new[] {
    new { Region = "East", Amount = 500 },
    new { Region = "West", Amount = 150 },
    new { Region = "East", Amount = 50 },
    new { Region = "West", Amount = 800 }
};

var summary = sales
    .GroupBy(s => s.Region)
    .OrderBy(g => g.Key)
    .Select(regionGroup =>
    {
        var bySizeGroup = regionGroup.GroupBy(s => s.Amount >= 200 ? "large" : "small");
        int large = bySizeGroup.Where(g => g.Key == "large").Select(g => g.Count()).FirstOrDefault();
        int small = bySizeGroup.Where(g => g.Key == "small").Select(g => g.Count()).FirstOrDefault();
        return $"{regionGroup.Key}: large={large} small={small}";
    })
    .ToArray();
// 结果：["East: large=1 small=1", "West: large=1 small=1"]
```

### 实用参考

| 方法 | 描述 |
| --- | --- |
| `GroupBy(keySelector)` | 按键对元素进行分组，返回 `IEnumerable<IGrouping<TKey, TElement>>` |
| `IGrouping.Key` | 分组的键值 |
| `IGrouping` 本身 | 是一个 `IEnumerable<TElement>`，您可以对其进行进一步查询 |
| `FirstOrDefault()` | 返回第一个元素，若为空则返回默认值，可用于安全地从内层分组中提取数据 |
| `OrderBy(keySelector)` | 按字母/数字顺序对元素或分组进行排序 |

### 你的任务

编写一个方法，接收一个整数数组并执行双层分组：

1. **外层分组**：将每个数字分类为 `"even"` 或 `"odd"`（基于是否能被 2 整除）。
2. **内层分组**：在每个奇偶性分组内，统计有多少个数字是**正数**（严格大于零），有多少个数字是**负数**（小于等于零）。
3. **格式**：每个结果字符串的格式应为 `"parity: pos=N neg=N"`，其中 `parity` 为 `"even"` 或 `"odd"`，`N` 为计数。
4. **排序**：按奇偶性名称的字母顺序升序返回结果（因此 `"even"` 排在 `"odd"` 之前）。

注意：在本题计数中，零被视为偶数且被视为负数（非正数）。

### 方法签名

```csharp
public static string[] GroupByParityAndSign(int[] numbers)
```

### 预期结果

```scss
GroupByParityAndSign([1, -2, 3, -4, 5, -6]) -> ["even: pos=0 neg=3", "odd: pos=3 neg=0"]
GroupByParityAndSign([2, 4, -1, -3])         -> ["even: pos=2 neg=0", "odd: pos=0 neg=2"]
GroupByParityAndSign([0])                     -> ["even: pos=0 neg=1"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] GroupByParityAndSign(int[] numbers)
    {
        // 外层按奇偶性分组，内层按正负分组并统计数量
        return numbers
            .GroupBy(n => n % 2 == 0 ? "even" : "odd")
            .OrderBy(g => g.Key)
            .Select(parityGroup =>
            {
                var bySign = parityGroup.GroupBy(n => n > 0 ? "pos" : "neg");
                int pos = bySign.Where(g => g.Key == "pos").Select(g => g.Count()).FirstOrDefault();
                int neg = bySign.Where(g => g.Key == "neg").Select(g => g.Count()).FirstOrDefault();
                return $"{parityGroup.Key}: pos={pos} neg={neg}";
            })
            .ToArray();
    }
}
```
