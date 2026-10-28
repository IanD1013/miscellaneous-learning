### 组织复杂的 LINQ 转换

现实世界中的数据处理通常涉及多个步骤：解析原始输入、分类或丰富数据、分组以及最终格式化输出。
当你把所有这些串联成单个 LINQ 表达式时，结果可能会变成一堵没人愿意在六个月后去调试的代码墙。
关键技术是在逻辑边界处**将链式调用拆分为具名的中间变量**：每个变量名描述了该阶段*数据所代表的含义*。

### 为什么具名中间变量很重要

思考一下 15 行的方法链与拆分为四个命名清晰的步骤的相同逻辑之间的区别。
具名中间变量提供了：

- **自文档化代码** - 变量名会告诉读者此时的数据结构形式
- **更容易调试** - 你可以单独检查每个变量
- **逻辑边界** - 解析与分类分离，分类又与分组分离

因为 LINQ 使用延迟执行（deferred execution），所以将链式调用拆分为中间变量并不会导致额外的迭代。
查询仅在你物化它时才会运行（例如使用 `.ToArray()` 或 `.ToList()`）。

### 运作方式

识别出转换过程中的自然“阶段”。
典型的阶段包括：

1. **解析（Parse）** - 将原始字符串或输入转换为结构化对象
2. **丰富/分类（Enrich/Classify）** - 添加派生属性，如类别或计算值
3. **聚合（Aggregate）** - 分组、计数或汇总
4. **格式化（Format）** - 生成最终的输出结构

将每个阶段赋值给一个能够描述数据状态的变量。

### 语法

```csharp
// 阶段 1：将原始数据解析为类型化对象
var parsedOrders = rawLines
    .Select(line => line.Split(','))
    .Select(parts => new { Product = parts[0], Quantity = int.Parse(parts[1]) });

// 阶段 2：分类
var categorized = parsedOrders
    .Select(o => new { o.Product, o.Quantity, Size = o.Quantity > 100 ? "bulk" : "retail" });

// 阶段 3：聚合
var grouped = categorized
    .GroupBy(o => o.Size);

// 阶段 4：格式化
var result = grouped
    .Select(g => $"{g.Key}: {g.Count()} orders")
    .ToArray();
```

### 示例

```csharp
// 示例：处理来自 "Department-Salary" 字符串的员工薪资数据
var rawData = new[] { "Engineering-95000", "Marketing-72000", "Engineering-88000", "Marketing-65000" };

var parsed = rawData
    .Select(r => r.Split('-'))
    .Select(p => new { Dept = p[0], Salary = int.Parse(p[1]) });

var deptSummaries = parsed
    .GroupBy(e => e.Dept)
    .OrderBy(g => g.Key);

var report = deptSummaries
    .Select(g => $"{g.Key}: avg {g.Average(e => e.Salary):F0}")
    .ToArray();
// 结果: ["Engineering: avg 91500", "Marketing: avg 68500"]
```

```csharp
// 示例：对温度进行分类并分组
var readings = new[] { "Monday:32", "Tuesday:28", "Wednesday:35", "Thursday:22" };

var parsed = readings
    .Select(r => r.Split(':'))
    .Select(p => new { Day = p[0], Temp = int.Parse(p[1]) });

var classified = parsed
    .Select(r => new { r.Day, Category = r.Temp >= 30 ? "hot" : "cool" });

var grouped = classified
    .GroupBy(r => r.Category)
    .OrderBy(g => g.Key);

var output = grouped
    .Select(g => $"{g.Key}: {string.Join(", ", g.Select(r => r.Day).OrderBy(d => d))}")
    .ToArray();
// 结果: ["cool: Thursday,Tuesday", "hot: Monday,Wednesday"]
```

### 常见模式

| 模式 | 用例 |
| --- | --- |
| `.Select(line => line.Split(...))` | 解析带分隔符的字符串 |
| `.Select(x => new { ..., Category = condition ? "a" : "b" })` | 为数据添加分类 |
| `.GroupBy(x => x.Property)` | 从已分类的数据中创建分组 |
| `.Select(g => $"{g.Key}: {string.Join(...)}")` | 格式化分组后的结果 |
| `.OrderBy(g => g.Key)` | 对分组或元素进行排序 |

### 你的任务

编写一个方法，通过多步 LINQ 转换来处理 `"Name:Score"` 字符串数组。
你应该：

- **解析（Parse）** 每条记录为一个姓名和一个整数分数
- **分类（Classify）** 每个条目到对应的分数区间：分数 0–49 为 `"fail"`，50–79 为 `"pass"`，80–100 为 `"excellent"`
- **分组（Group）** 按区间对条目进行分组
- **格式化（Format）** 每个分组为 `"range: Name1,Name2"`，其中姓名按字母顺序排列，用逗号分隔且逗号两边没有空格
- **排序（Sort）** 最终输出按区间名称的字母顺序排序

在每个逻辑边界处使用具名中间变量来组织你的代码。

### 方法签名

```csharp
public static string[] TransformData(string[] records)
```

### 预期结果

```css
TransformData(["Alice:85", "Bob:55", "Carol:90", "Dave:45", "Eve:72"])
  -> ["excellent: Alice,Carol", "fail: Dave", "pass: Bob,Eve"]

TransformData(["Zara:100", "Yuki:0"])
  -> ["excellent: Zara", "fail: Yuki"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] TransformData(string[] records)
    {
        // 第 1 步：将记录解析为结构化数据
        var parsed = records
            .Select(r => r.Split(':'))
            .Select(p => new { Name = p[0], Score = int.Parse(p[1]) });

        // 第 2 步：按分数区间对每个条目分类
        var classified = parsed
            .Select(e => new
            {
                e.Name,
                Range = e.Score >= 80 ? "excellent" : e.Score >= 50 ? "pass" : "fail"
            });

        // 第 3 步：按区间分组，并按区间名称排序
        var grouped = classified
            .GroupBy(e => e.Range)
            .OrderBy(g => g.Key);

        // 第 4 步：把每个分组格式化为输出字符串，组内姓名按字母顺序排列
        var output = grouped
            .Select(g => $"{g.Key}: {string.Join(",", g.Select(e => e.Name).OrderBy(n => n))}");

        // 返回最终排好序的结果
        return output.ToArray();
    }
}
```
