### 使用 LINQ 构建多阶段数据处理管道

在实际应用程序中，原始数据很少会以方便的格式呈现。
一个典型的数据处理管道通常包含几个连续阶段：**解析**原始输入、**清理和验证**记录、按业务相关键进行**分组**、在每个组内**聚合**值，以及**格式化**最终输出。
LINQ 的可组合查询操作符允许你将整个管道表达为单一、可读的转换链，无需中间变量或手动编写循环。

### 工作原理

可以把每个 LINQ 操作符看作工厂流水线上的一个阶段。
原材料（字符串）从一端进入。
每个工位（操作符）在将数据传递到下一工位之前对其进行转换、过滤或重塑。
其精妙之处在于每个阶段都是独立且可测试的：

1. **解析（Parse）** - 将原始字符串分解为结构化片段（`Split`、匿名类型）
2. **验证（Validate）** - 过滤格式错误的条目（`Where`）
3. **分组（Group）** - 按复合键将项目分桶（带有匿名键的 `GroupBy`）
4. **聚合（Aggregate）** - 计算每个分组的汇总信息（`Sum`、`Count`、`Average`）
5. **格式化（Format）** - 将结果转换为所需的输出形式（使用字符串插值的 `Select`）
6. **排序（Order）** - 确定性排序（`OrderBy`）

### 语法

```csharp
// 将字符串拆分成多个部分
string[] parts = "key:value:number".Split(':');

// 按复合键（多个字段）分组
var grouped = items.GroupBy(x => new { x.Category, x.SubCategory });

// 访问分组键的属性并进行聚合
var results = grouped.Select(g => new {
    Label = g.Key.Category,
    Total = g.Sum(x => x.Value)
});
```

### 示例

假设要处理格式为 `"Severity:Module:ResponseTimeMs"` 的服务器日志条目：

```csharp
// 示例 1：解析日志条目，按严重级别分组并计数
string[] logs = { "ERROR:Auth:250", "WARN:Auth:100", "ERROR:Auth:300", "INFO:DB:50" };

var summary = logs
    .Select(log => log.Split(':'))
    .Where(parts => parts.Length == 3)
    .Select(parts => new { Severity = parts[0], Module = parts[1], Ms = int.Parse(parts[2]) })
    .GroupBy(x => x.Severity)
    .Select(g => $"{g.Key}: {g.Count()} entries")
    .OrderBy(s => s)
    .ToArray();
// 结果：["ERROR: 2 entries", "INFO: 1 entries", "WARN: 1 entries"]

// 示例 2：按两个字段分组并求和
var moduleAvg = logs
    .Select(log => log.Split(':'))
    .Select(p => new { Severity = p[0], Module = p[1], Ms = int.Parse(p[2]) })
    .GroupBy(x => new { x.Severity, x.Module })
    .Select(g => $"{g.Key.Severity}-{g.Key.Module}: {g.Sum(x => x.Ms)}ms")
    .OrderBy(s => s)
    .ToArray();
// 结果：["ERROR-Auth: 550ms", "INFO-DB: 50ms", "WARN-Auth: 100ms"]
```

### 常见模式

| 模式 | 操作符 | 目的 |
| --- | --- | --- |
| 解析与验证 | `Select` + `Where` | 将字符串转换为结构化数据，剔除无效行 |
| 复合分组 | `GroupBy(x => new { ... })` | 同时按多个字段进行分组 |
| 分组聚合 | `g.Sum()`, `g.Average()`, `g.Count()` | 计算每个分组的指标 |
| 安全解析 | `int.TryParse(str, out _)` | 检查字符串是否为有效数字且不抛出异常 |
| 去除首尾空格 | `str.Trim()` | 处理原始数据中不一致的空格 |

### 你的任务

编写一个方法来处理销售记录数组。
每条记录都是一个以冒号分隔的字符串，格式为 `"Region:Product:Amount"`，其中 Amount 为整数。

你的管道应该：

- **跳过**任何为 null、空字符串、仅包含空白字符或格式错误（分段数量不正确、金额非数字）的记录
- **去除**地区（region）和产品（product）名称的首尾空格
- 按地区和产品的组合进行**分组**
- **求和**每个组内的金额
- 将每个结果**格式化**为 `"Region-Product: Total"`
- 按格式化后的字符串进行字母升序**排序**
- 以 `string[]` 形式返回结果

### 方法签名

```csharp
public static string[] ProcessSalesData(string[] records)
```

### 预期结果

```css
ProcessSalesData(["North:Widget:100", "South:Gadget:200", "North:Widget:150", "South:Widget:300"])
  -> ["North-Widget: 250", "South-Gadget: 200", "South-Widget: 300"]

ProcessSalesData(["East:Bolt:50"])
  -> ["East-Bolt: 50"]

ProcessSalesData([])
  -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] ProcessSalesData(string[] records)
    {
        return records
            // 跳过 null、空字符串和仅包含空白字符的记录
            .Where(r => !string.IsNullOrWhiteSpace(r))
            // 解析：按冒号拆分
            .Select(r => r.Split(':'))
            // 验证：必须恰好 3 段，且金额是整数
            .Where(p => p.Length == 3 && int.TryParse(p[2], out _))
            // 投影：去除地区和产品名称的首尾空格
            .Select(p => new { Region = p[0].Trim(), Product = p[1].Trim(), Amount = int.Parse(p[2]) })
            // 按地区和产品的组合分组
            .GroupBy(x => new { x.Region, x.Product })
            // 对每组金额求和并格式化
            .Select(g => $"{g.Key.Region}-{g.Key.Product}: {g.Sum(x => x.Amount)}")
            // 按格式化后的字符串升序排序
            .OrderBy(s => s)
            .ToArray();
    }
}
```
