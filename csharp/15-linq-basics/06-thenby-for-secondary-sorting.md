### 使用 ThenBy 进行次级排序

`ThenBy()` 在 `OrderBy()` 之后添加次级排序条件。
当多个元素在主排序键上具有相同的值时，`ThenBy()` 会使用次级排序键来决定它们的顺序。

### 基本用法

```csharp
// 先按年龄排序，再按名字排序
var sorted = people
    .OrderBy(p => p.Age)
    .ThenBy(p => p.Name)
    .ToList();

// 先按部门排序，再按薪资降序排序
var employees = staff
    .OrderBy(e => e.Department)
    .ThenByDescending(e => e.Salary)
    .ToList();
```

### OrderBy 与 ThenBy

- `OrderBy()` - 确立主排序规则（最先使用）
- `ThenBy()` - 添加次级、三级等排序规则（在 OrderBy 之后使用）
- 你可以链式调用多个 `ThenBy()` 来实现更复杂的排序

```csharp
// 多级排序
var result = items
    .OrderBy(x => x.Category)      // 主排序
    .ThenBy(x => x.Subcategory)    // 次级排序
    .ThenBy(x => x.Name)           // 三级排序
    .ToList();
```

### 降序变体

| 方法 | 描述 |
| --- | --- |
| `OrderBy()` | 主排序，升序 |
| `OrderByDescending()` | 主排序，降序 |
| `ThenBy()` | 次级排序，升序 |
| `ThenByDescending()` | 次级排序，降序 |

### 你的任务

给定一个 "FirstName LastName" 格式的全名列表，首先按姓氏（Last Name）的字母顺序排序，若姓氏相同，则按名字（First Name）排序。

### 方法签名

```csharp
public static List<string> SortByLastNameThenFirstName(List<string> fullNames)
```

### 预期结果

```
["John Smith", "Jane Doe", "Bob Smith"] -> ["Jane Doe", "Bob Smith", "John Smith"]
["Alice Brown", "Charlie Brown"] -> ["Alice Brown", "Charlie Brown"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static List<string> SortByLastNameThenFirstName(List<string> fullNames)
    {
        // 先按姓氏（空格后的部分）排序，再按名字（空格前的部分）排序
        return fullNames
            .OrderBy(name => name.Split(' ')[1])
            .ThenBy(name => name.Split(' ')[0])
            .ToList();
    }
}
```
