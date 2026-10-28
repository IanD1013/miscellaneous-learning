### 在 LINQ 中基于复合键进行连接

在关系型数据中，单个字段往往不足以唯一标识一条记录。
**复合键**结合了两个或多个字段以构成唯一标识符，例如 `DepartmentCode` 与 `EmployeeId` 的组合，或者 `Region` 与 `ProductCode` 的组合。
当你需要基于多个匹配字段连接两个集合时，LINQ 的 `Join` 方法通过匿名类型键选择器来支持这一操作。

### 工作原理

LINQ 的 `Join` 方法接受四个参数：内部集合、外部键选择器、内部键选择器以及结果选择器。
在基于单个字段进行连接时，键选择器返回一个简单值。
对于复合键，每个键选择器返回一个包含共同组成该键的各字段的**匿名类型**。

关键要点：C# 在比较两个匿名类型是否相等时，会检查它们是否具有**相同顺序的相同属性名称**，以及每个对应的属性值是否相等。
这意味着 `new { X = 10, Y = 20 }` 等于另一个 `new { X = 10, Y = 20 }`，使得匿名类型非常适合用作复合连接键。

### 语法

```csharp
var result = outerCollection.Join(
    innerCollection,
    outer => new { KeyPart1 = outer.FieldA, KeyPart2 = outer.FieldB },
    inner => new { KeyPart1 = inner.FieldX, KeyPart2 = inner.FieldY },
    (outer, inner) => /* 结果选择器 */
);
```

**重要提示：** 两个匿名类型中的属性名称**必须完全匹配**。
如果外部键使用 `new { Dept = ..., Code = ... }`，内部键也必须使用 `new { Dept = ..., Code = ... }`，而不能是 `new { Department = ..., Code = ... }`。

### 示例

以按地区和产品代码将发货记录与仓库进行匹配为例：

```csharp
var shipments = new[]
{
    new { Region = "East", ProductCode = "A1", Quantity = 100 },
    new { Region = "West", ProductCode = "B2", Quantity = 200 },
    new { Region = "East", ProductCode = "B2", Quantity = 50 }
};

var warehouses = new[]
{
    new { Region = "East", ProductCode = "A1", Capacity = 500 },
    new { Region = "West", ProductCode = "B2", Capacity = 300 }
};

var matched = shipments.Join(
    warehouses,
    s => new { s.Region, s.ProductCode },
    w => new { w.Region, w.ProductCode },
    (s, w) => $"{s.Region}-{s.ProductCode}: {s.Quantity}/{w.Capacity}"
);
// 结果：["East-A1: 100/500", "West-B2: 200/300"]
// 注意：East-B2 没有匹配的仓库，因此被排除（内连接行为）
```

你也可以使用 `Zip` 从并行数组构建集合：

```csharp
string[] depts = { "HR", "ENG", "HR" };
int[] ids = { 1, 2, 3 };
var employees = depts.Zip(ids, (d, i) => new { Dept = d, Id = i });
// 生成：[{Dept:"HR", Id:1}, {Dept:"ENG", Id:2}, {Dept:"HR", Id:3}]
```

### 常见模式

- **并行数组转为对象：** 在连接前，使用 `Zip` 将多个数组合并为一个匿名对象序列。
- **属性名称对齐：** 当源字段具有不同名称时，显式命名匿名类型的属性，使两边匹配：`new { Key1 = outer.Name, Key2 = outer.Code }` 和 `new { Key1 = inner.Label, Key2 = inner.Ref }`。
- **仅返回匹配项：** `Join` 执行的是内连接，来自任一方的未匹配元素都将被排除。

### 你的任务

你将接收到两个以数组形式表示的并行集合：

1. **人员（People）：** 由 `firstNames` 和 `lastNames` 数组定义（长度相同，按索引配对）
2. **得分记录（Score records）：** 由 `matchFirsts`、`matchLasts` 和 `scores` 数组定义（长度相同，按索引配对）

在名字（first name）**和**姓氏（last name）均匹配（复合键）的情况下，将人员与得分记录进行连接。
为每个匹配对返回格式为 `"FirstName LastName: Score"` 的字符串数组，**按名字字母顺序升序排序**。

如果某个人没有匹配的得分记录，则不应出现在结果中。

### 方法签名

```csharp
public static string[] JoinOnComposite(string[] firstNames, string[] lastNames, string[] matchFirsts, string[] matchLasts, int[] scores)
```

### 预期结果

```css
JoinOnComposite(["Alice","Bob"], ["Smith","Jones"], ["Bob","Alice"], ["Jones","Smith"], [88,95])
  -> ["Alice Smith: 95", "Bob Jones: 88"]

JoinOnComposite(["Alice","Alice"], ["Smith","Jones"], ["Alice"], ["Jones"], [72])
  -> ["Alice Jones: 72"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] JoinOnComposite(string[] firstNames, string[] lastNames, string[] matchFirsts, string[] matchLasts, int[] scores)
    {
        // 用 Zip 把并行数组组合成人员和得分记录
        var people = firstNames.Zip(lastNames, (f, l) => new { First = f, Last = l });
        var records = matchFirsts
            .Zip(matchLasts, (f, l) => new { First = f, Last = l })
            .Zip(scores, (k, s) => new { k.First, k.Last, Score = s });

        // 以 (名字, 姓氏) 匿名类型作为复合键进行内连接，按名字排序
        return people
            .Join(
                records,
                p => new { p.First, p.Last },
                r => new { r.First, r.Last },
                (p, r) => new { p.First, p.Last, r.Score })
            .OrderBy(x => x.First)
            .Select(x => $"{x.First} {x.Last}: {x.Score}")
            .ToArray();
    }
}
```
