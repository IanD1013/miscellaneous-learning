### LINQ 管道综合实战

现实世界中的数据处理很少只涉及单一操作。
大多数任务都需要将多个转换链接在一起：过滤不相关的记录、重塑数据、去除重复项、对结果排序以及修剪输出。
LINQ 的 fluent API 使这一切变得非常自然，它允许你将多个操作符组合成一条清晰易读的管道，其中每个步骤的输出都会传递给下一个步骤。

### 工作原理

每个 LINQ 操作符都接收一个序列（`IEnumerable<T>`）并返回一个新序列。
因为它们都具有相同的签名，所以你可以将它们首尾相连地链式调用。
这些操作是延迟执行的，直到你将结果具体化（例如使用 `.ToArray()` 或 `.ToList()`）时才会真正执行。
链接操作符的**顺序**至关重要：在转换之前进行过滤可以减少需要处理的元素数量，而在去重之后进行排序可以避免不必要的比较。

### 语法

```csharp
var result = source
    .Where(item => condition)       // 只保留满足条件的元素
    .Select(item => transformation) // 转换每个元素
    .Distinct()                     // 移除重复值
    .OrderBy(item => sortKey)       // 按键升序排序
    .Skip(n)                        // 跳过前 n 个元素
    .ToArray();                     // 物化为数组
```

### 操作符参考

| 操作符 | 说明 | 示例 |
| --- | --- | --- |
| `Where` | 按谓词条件过滤元素 | `.Where(x => x.Length > 3)` |
| `Select` | 将每个元素投影为新形式 | `.Select(x => x.ToUpper())` |
| `Distinct` | 移除重复元素 | `.Distinct()` |
| `OrderBy` | 按键升序对元素进行排序 | `.OrderBy(x => x.Name)` |
| `Skip` | 跳过指定数量的元素 | `.Skip(5)` |

### 示例

考虑处理员工薪资列表的情况：

```csharp
double[] salaries = { 55000, 42000, -1, 72000, 42000, 88000, 0 };

// 移除无效条目，转换为月薪，去重，排序，跳过最低的 2 个
var result = salaries
    .Where(s => s > 0)
    .Select(s => s / 12.0)
    .Distinct()
    .OrderBy(s => s)
    .Skip(2)
    .ToArray();
// result: { 4583.33..., 6000.0, 7333.33... }
```

或者处理单词集合：

```csharp
string[] words = { "apple", "", "Banana", "apple", "cherry", "date" };

var result = words
    .Where(w => w.Length > 0)
    .Select(w => w.ToLower())
    .Distinct()
    .OrderBy(w => w)
    .Skip(1)
    .ToArray();
// result: { "banana", "cherry", "date" }
```

请注意每个步骤是如何逐步细化数据的。
这里的顺序是有意安排的：先进行过滤可以减少后续步骤必须处理的元素数量。

### 你的任务

编写一个方法，对整型数组构建一个五步 LINQ 管道：

1. **过滤（Filter）** - 仅保留正数（大于零）
2. **转换（Transform）** - 将剩余的每个数字乘以 2
3. **去重（Deduplicate）** - 移除转换后产生的任何重复值
4. **排序（Sort）** - 按升序排列结果
5. **修剪（Trim）** - 跳过排序结果中的前 2 个元素

将最终结果作为 `int[]` 返回。

### 方法签名

```csharp
public static int[] ProcessPipeline(int[] numbers)
```

### 预期结果

```scss
ProcessPipeline([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]) -> [6, 8, 10, 12, 18]
ProcessPipeline([1, 2, 3])                        -> [6]
ProcessPipeline([-5, -3, 0, 1])                   -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ProcessPipeline(int[] numbers)
    {
        return numbers
            .Where(n => n > 0)     // 过滤：只保留正数
            .Select(n => n * 2)    // 转换：乘以 2
            .Distinct()            // 去重
            .OrderBy(n => n)       // 排序：升序
            .Skip(2)               // 修剪：跳过前 2 个
            .ToArray();
    }
}
```
