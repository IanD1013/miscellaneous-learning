### LINQ 管道总结：解析、验证、分组、聚合

现实世界中的数据管道很少只涉及单一转换。
生产环境的代码通常将解析、验证、分组和格式化串联成一个流畅的 LINQ 管道。
这个终极综合练习将把你学到的关于 LINQ 的所有知识整合到一个连贯的方法中。

### 工作原理

数据管道通过按序排列的阶段来处理原始输入。
每个阶段都会缩减、重构或丰富数据。
LINQ 的方法链让你能够将其表达为一个单一且可读性强的表达式：

1. **解析（Parse）** - 将原始字符串拆分或解构为结构化记录
2. **过滤（Filter）** - 丢弃格式错误或无效的条目
3. **投影（Project）** - 将数据重构为适合聚合的形式
4. **分组（Group）** - 按键对记录进行分区
5. **聚合（Aggregate）** - 计算每个组的汇总统计信息
6. **格式化（Format）** - 生成人类可读的输出

### 语法

```csharp
source
    .Select(raw => Parse(raw))          // 解析
    .Where(record => IsValid(record))   // 验证
    .GroupBy(record => record.Key)      // 分组
    .OrderBy(g => g.Key)                // 对分组排序
    .Select(g => FormatGroup(g))        // 聚合 + 格式化
    .ToArray();
```

### 示例

考虑格式为 `"Level:Timestamp:Duration"` 的日志条目：

```csharp
// 拆分并验证结构
var parts = "INFO:2024-01-15:120".Split(':');
// parts.Length == 3 → 结构有效

var badEntry = "ERROR_missing_colons";
var badParts = badEntry.Split(':');
// badParts.Length == 1 → 无效，丢弃

// 检查数值是否有效
int.TryParse("120", out int duration);  // true，duration = 120
int.TryParse("abc", out int fail);      // false → 丢弃
int.TryParse("-5", out int neg);        // true，但 neg < 0 → 可能丢弃

// 分组并格式化多个聚合值
var logs = new[] { "INFO:A:100", "INFO:B:200", "WARN:C:50" };
var summary = logs
    .Select(l => l.Split(':'))
    .Where(p => p.Length == 3 && int.TryParse(p[2], out _))
    .Select(p => new { Level = p[0], Duration = int.Parse(p[2]) })
    .GroupBy(x => x.Level)
    .OrderBy(g => g.Key)
    .Select(g => $"{g.Key}: Count={g.Count()}, Total={g.Sum(x => x.Duration)}")
    .ToArray();
// ["INFO: Count=2, Total=300", "WARN: Count=1, Total=50"]
```

### 格式化平均值

```csharp
// 使用 :F2 格式说明符得到恰好 2 位小数
double avg = 66.66666;
string formatted = $"{avg:F2}"; // "66.67"

// 对整数求平均前先转换为 double
group.Average(x => (double)x.Value); // 确保小数精度
```

### 实用参考

| 方法 / 特性 | 描述 |
| --- | --- |
| `string.Split(':')` | 按分隔符将字符串拆分为数组 |
| `int.TryParse(s, out int v)` | 安全地解析；如果无效则返回 false |
| `.GroupBy(x => x.Key)` | 对共享相同键的元素进行分组 |
| `.Count()` | 组中的元素数量 |
| `.Sum(x => x.Prop)` | 数值属性的总和 |
| `.Average(x => (double)x.Prop)` | 具有 double 精度的平均值 |
| `$"{value:F2}"` | 将 double 格式化为 2 位小数 |
| `.OrderBy(g => g.Key)` | 按字母顺序对组进行排序 |

### 你的任务

编写 `RunPipeline(string[] rawData)`，通过以下阶段处理原始字符串数组：

1. **解析**：每个有效记录的格式为 `"Category:Name:Value"`，恰好由冒号分隔的三个部分组成。
2. **验证**：仅保留 `Value` 为有效**正整数**（大于 0）的记录。丢弃不是恰好 3 个部分或值不是正整数的记录。
3. 按 `Category` **分组**。
4. **聚合**每个组：计算 `Count`、`Total`（值之和）和 `Avg`（值的平均数，格式化为 2 位小数）。
5. 将每个组**格式化**为：`"Category: Count=N, Total=N, Avg=N.NN"`
6. 按类别名称的字母顺序对结果进行**排序**。

将结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] RunPipeline(string[] rawData)
```

### 预期结果

```css
RunPipeline(["A:x:10", "B:y:20", "A:z:30", "B:w:-5", "A:q:20"])
  -> ["A: Count=3, Total=60, Avg=20.00", "B: Count=1, Total=20, Avg=20.00"]

RunPipeline(["X:a:5"])
  -> ["X: Count=1, Total=5, Avg=5.00"]

RunPipeline(["bad", "also:bad", "still:not:valid"])
  -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] RunPipeline(string[] rawData)
    {
        return rawData
            // 解析：按冒号拆分
            .Select(raw => raw.Split(':'))
            // 验证：恰好 3 个部分，且值是正整数
            .Where(p => p.Length == 3 && int.TryParse(p[2], out int v) && v > 0)
            // 投影：取出类别和值
            .Select(p => new { Category = p[0], Value = int.Parse(p[2]) })
            // 按类别分组，并按类别名称的字母顺序排序
            .GroupBy(x => x.Category)
            .OrderBy(g => g.Key)
            // 聚合并格式化：数量、总和、保留 2 位小数的平均值
            .Select(g => $"{g.Key}: Count={g.Count()}, Total={g.Sum(x => x.Value)}, Avg={g.Average(x => (double)x.Value):F2}")
            .ToArray();
    }
}
```
