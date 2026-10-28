### 带有元素选择器的 GroupBy

LINQ 的 `GroupBy` 有多个重载。
最常见的重载接受一个键选择器（key selector），但当你还需要在每个元素进入分组之前对其进行**转换**时，双参数重载可以省去单独的 `Select` 步骤，并使你的意图更加清晰明了。

使用 `GroupBy(keySelector, elementSelector)`，你将获得 `IEnumerable<IGrouping<TKey, TElement>>`，其中 `TElement` 是元素选择器返回的类型，而**不是**原始源类型。

### 工作原理

标准的单参数 `GroupBy` 在每个分组中存储原始项：

```csharp
var groups = items.GroupBy(x => x.Category);
// 每个分组包含原始的项对象
```

双参数重载允许你在**分组时**对每个项进行投影：

```csharp
var groups = items.GroupBy(
    x => x.Category,      // 键选择器
    x => x.Price           // 元素选择器 - 每个分组中只存放价格
);
// 现在每个分组包含的是 decimal 值，而不是完整的项对象
```

这意味着分组本身保存的是转换后的值。
你不需要在每个分组内部再进行后续的 `Select` 操作。

### 语法

```csharp
source.GroupBy(
    element => /* 键表达式 */,
    element => /* 投影后的元素表达式 */
)
```

两个 lambda 参数都接收相同的源元素，但它们扮演不同的角色：

- 第一个决定元素放入**哪个分组**。
- 第二个决定在该分组中存储**什么值**。

### 示例

```csharp
// 示例 1：按部门对员工分组，只保留他们的姓名
var roster = employees.GroupBy(
    e => e.Department,
    e => e.Name
);
// IGrouping<string, string> - 键是部门，元素是姓名

// 示例 2：按客户 ID 对订单分组，只保留总额
var totals = orders.GroupBy(
    o => o.CustomerId,
    o => o.Total
);
// IGrouping<int, decimal> - 键是客户 ID，元素是总额

// 示例 3：按符号对数字分组，存储它们的绝对值
int[] nums = { -3, 1, -7, 4, -1, 2 };
var grouped = nums.GroupBy(
    n => n >= 0 ? "positive" : "negative",
    n => Math.Abs(n)
);
// "negative" 分组包含：3, 7, 1
// "positive" 分组包含：1, 4, 2
```

### 常用参考

| 方法 / 属性 | 描述 |
| --- | --- |
| `GroupBy(keySelector, elementSelector)` | 在一个步骤中对元素进行分组和转换 |
| `IGrouping<TKey, TElement>.Key` | 分组的键 |
| `string.Join(separator, values)` | 使用分隔符连接元素 |
| `char.ToLower(c)` | 将字符转换为小写 |
| `string.ToUpper()` | 返回字符串的大写版本 |
| `OrderBy(keySelector)` | 按键对序列进行排序 |

### 你的任务

编写一个方法，接收一个单词数组并：

1. 按单词的首字母（小写）进行**分组**，以首字母作为键。
2. 通过元素选择器（`GroupBy` 的第二个参数）将每个单词**转换**为大写。
3. 将每个分组**格式化**为 `"k=[WORD1,WORD2]"`，即键后面跟 `=`，然后是方括号中用逗号分隔的大写单词，**不包含空格**。
4. 将格式化后的字符串作为 `string[]` 返回，并**按键排序**。

### 方法签名

```csharp
public static string[] GroupAndUpperCase(string[] words)
```

### 预期结果

```css
GroupAndUpperCase(["apple", "banana", "avocado"]) -> ["a=[APPLE,AVOCADO]", "b=[BANANA]"]
GroupAndUpperCase(["cat", "car", "dog"]) -> ["c=[CAT,CAR]", "d=[DOG]"]
GroupAndUpperCase(["zoo"]) -> ["z=[ZOO]"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] GroupAndUpperCase(string[] words)
    {
        // 以小写首字母为键分组，元素选择器把单词转为大写
        return words
            .GroupBy(w => char.ToLower(w[0]), w => w.ToUpper())
            .OrderBy(g => g.Key)
            .Select(g => $"{g.Key}=[{string.Join(",", g)}]")
            .ToArray();
    }
}
```
