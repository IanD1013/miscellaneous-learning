### 使用 OrderBy 和 OrderByDescending 进行排序

排序数据是编程中最常见的操作之一。
无论是在展示搜索结果、对分数进行排名，还是在组织记录，你都需要可靠的方法来按特定顺序排列元素。
LINQ 为此提供了两个优雅的操作符：用于升序排序的 `OrderBy` 和用于降序排序的 `OrderByDescending`。

### 工作原理

`OrderBy` 和 `OrderByDescending` 都接受一个**键选择器**（key selector），即一个从每个元素中提取用于排序的值的函数。
它们返回一个 `IOrderedEnumerable<T>`，这是一个已排序的序列，并保留了使用 `ThenBy` 或 `ThenByDescending` 添加次要排序条件的能力。

原始序列永远不会被修改。
相反，它会生成一个新的已排序序列。
这符合 LINQ 创建新序列而不是更改现有序列的理念。

### 语法

```csharp
// 升序
source.OrderBy(element => keySelector)

// 降序
source.OrderByDescending(element => keySelector)

// 链式添加次要排序
source.OrderBy(e => primaryKey).ThenBy(e => secondaryKey)
```

键选择器是一个 lambda 表达式，用于告诉 LINQ 依据*什么*进行排序。
对于整数或字符串等简单类型，通常只需返回元素本身。
对于复杂对象，则选择某个属性。

### 示例

```csharp
// 按字母顺序对字符串排序
string[] fruits = { "Banana", "Apple", "Cherry" };
var sorted = fruits.OrderBy(f => f);
// 结果：["Apple", "Banana", "Cherry"]

// 按长度对字符串排序，最长的在前
var byLength = fruits.OrderByDescending(f => f.Length);
// 结果：["Banana", "Cherry", "Apple"]

// 按属性对对象排序
var employees = new[] {
    new { Name = "Sara", Age = 30 },
    new { Name = "Tom", Age = 25 },
    new { Name = "Lena", Age = 35 }
};
var byAge = employees.OrderBy(e => e.Age);
// 结果：Tom (25), Sara (30), Lena (35)

// 多级排序
var byAgeAndName = employees
    .OrderBy(e => e.Age)
    .ThenBy(e => e.Name);
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `.OrderBy(x => x)` | 按元素自身的值排序 |
| `.OrderBy(x => x.Property)` | 按特定属性排序 |
| `.OrderByDescending(x => x)` | 按降序/逆序排序 |
| `.OrderBy(...).ThenBy(...)` | 主要排序 + 次要排序 |
| `.OrderBy(...).ToArray()` | 将排序后的结果具体化为数组 |

请记住，`OrderBy` 和 `OrderByDescending` 采用延迟执行（deferred execution）：排序操作直到你迭代或具体化结果（例如使用 `.ToArray()` 或 `.ToList()`）时才会发生。

### 你的任务

编写一个方法，该方法接受一个整数数组和一个布尔标志。
当标志为 `false` 时，返回按**升序**排列的数字。
当标志为 `true` 时，返回按**降序**排列的数字。
将结果作为 `int[]` 返回。

### 方法签名

```csharp
public static int[] SortNumbers(int[] numbers, bool descending)
```

### 预期结果

```scss
SortNumbers([3, 1, 4, 1, 5, 9], false)  -> [1, 1, 3, 4, 5, 9]
SortNumbers([3, 1, 4, 1, 5, 9], true)   -> [9, 5, 4, 3, 1, 1]
SortNumbers([42], false)                 -> [42]
SortNumbers([], true)                    -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] SortNumbers(int[] numbers, bool descending)
    {
        // 根据标志选择降序或升序排序
        if (descending)
        {
            return numbers.OrderByDescending(n => n).ToArray();
        }

        return numbers.OrderBy(n => n).ToArray();
    }
}
```
