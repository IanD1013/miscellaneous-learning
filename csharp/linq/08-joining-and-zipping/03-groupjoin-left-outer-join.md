### GroupJoin - LINQ 中的左外连接 (Left Outer Joins)

在关系型数据库中，**左外连接**（left outer join）会返回左表中的每一行以及右表中匹配的行。
当没有匹配项时，右侧将返回 `NULL`。
LINQ 的 `GroupJoin` 方法为你提供了相同的能力：它会保留 **outer**（外层）序列中的每一个元素，并将来自 **inner**（内层）序列的匹配元素分组为一个集合，如果没有匹配项，该集合可能为空。

这与 `Join` 不同，后者仅返回两边都存在匹配项的元素（内连接）。
每当你需要保留“父”记录（即使它们没有相关的“子”记录）时，`GroupJoin` 都至关重要。

### 工作原理

`GroupJoin` 会遍历外层序列。
对于每个外层元素，它会在内层序列中查找所有匹配的元素（基于键是否相等），并将它们作为 `IEnumerable<T>` 传递给你的结果选择器。
如果没有匹配的内层元素，该集合仅为空，外层元素绝不会被丢弃。

其签名如下：

```csharp
outer.GroupJoin(inner, outerKeySelector, innerKeySelector, resultSelector)
```

- **outer** - 其元素全部被保留的序列
- **inner** - 用于进行匹配的序列
- **outerKeySelector** - 从每个外层元素中提取连接键
- **innerKeySelector** - 从每个内层元素中提取连接键
- **resultSelector** - `(outerElement, matchingInnerElements) => ...` - 生成输出结果

### 语法

```csharp
// 通用模式
var result = outerCollection.GroupJoin(
    innerCollection,
    outer => outer.Key,
    inner => inner.Key,
    (outerItem, innerGroup) => /* 将 outerItem 与 innerGroup 结合 */
);
```

### 示例

假设你有类别和产品，并且你希望列出每个类别，即使它没有任何产品：

```csharp
var categories = new[] { "Books", "Electronics", "Toys" };
var products = new[] {
    new { Name = "Laptop", Category = "Electronics" },
    new { Name = "Phone", Category = "Electronics" },
    new { Name = "Novel", Category = "Books" }
};

var report = categories.GroupJoin(
    products,
    cat => cat,
    prod => prod.Category,
    (cat, prods) =>
    {
        var count = prods.Count();
        return $"{cat}: {count} product(s)";
    });

// 结果：
// "Books: 1 product(s)"
// "Electronics: 2 product(s)"
// "Toys: 0 product(s)"        <-- 即使没有产品，Toys 也会被保留
```

请注意，即使没有产品，“Toys”仍然以计数 0 显示。
而常规的 `Join` 则会将其完全丢弃。

另一种模式是在 `SelectMany` 内部使用 `DefaultIfEmpty`，将结果展平为真正的左外连接（每个组合一行）：

```csharp
var flat = categories.GroupJoin(
    products,
    cat => cat,
    prod => prod.Category,
    (cat, prods) => new { cat, prods })
    .SelectMany(
        x => x.prods.DefaultIfEmpty(),
        (x, prod) => $"{x.cat} -> {prod?.Name ?? "(none)"}");

// "Books -> Novel"
// "Electronics -> Laptop"
// "Electronics -> Phone"
// "Toys -> (none)"
```

### 实用参考

| 方法 / 概念 | 描述 |
| --- | --- |
| `GroupJoin(...)` | 按键关联外层和内层元素；内层匹配项被分组为一个集合 |
| `DefaultIfEmpty()` | 如果集合为空，则返回一个默认元素 |
| `string.Join(sep, values)` | 使用分隔符连接元素 |
| `Zip(other, selector)` | 按位置配对来自两个序列的元素 |
| `OrderBy(keySelector)` | 按给定的键对元素进行升序排序 |

### 你的任务

编写一个接收三个数组的方法：

1. **departments** - 部门名称列表（外层序列）
2. **empDepts** - 每个员工所属的部门
3. **empNames** - 每个员工的姓名（与 `empDepts` 索引相同）

对于每个部门，生成格式为 `"Department: EmployeeList"` 的字符串。
如果某个部门有员工，请列出他们的姓名并用逗号分隔（逗号周围不要有空格）。
如果某个部门没有员工，请使用 `"No employees"` 作为员工列表。

返回按完整输出字符串按字母顺序排序的结果。

### 方法签名

```csharp
public static string[] DepartmentEmployees(string[] departments, string[] empDepts, string[] empNames)
```

### 预期结果

```css
DepartmentEmployees(["HR","IT","Finance"], ["IT","IT","HR"], ["Alice","Bob","Carol"])
  -> ["Finance: No employees", "HR: Carol", "IT: Alice,Bob"]

DepartmentEmployees(["Sales"], [], [])
  -> ["Sales: No employees"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] DepartmentEmployees(string[] departments, string[] empDepts, string[] empNames)
    {
        // 用 Zip 把员工的部门和姓名配对
        var employees = empDepts.Zip(empNames, (d, n) => new { Dept = d, Name = n });

        // GroupJoin 保留每个部门，没有员工时输出 "No employees"
        return departments
            .GroupJoin(
                employees,
                d => d,
                e => e.Dept,
                (d, emps) => emps.Any()
                    ? $"{d}: {string.Join(",", emps.Select(e => e.Name))}"
                    : $"{d}: No employees")
            .OrderBy(s => s)
            .ToArray();
    }
}
```
