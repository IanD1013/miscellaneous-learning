### Where 运算符 - LINQ 的核心过滤器

过滤是编程中最常见的任务之一。
无论你是从数据库中提取活跃用户、从表单中筛选有效输入，还是从日志中提取相关记录，你都需要一种仅保留满足条件的元素的方法。
在 C# 中，LINQ 的 `Where` 运算符就是完成这项任务的首选工具。

### 工作原理

`Where` 会逐个遍历序列中的每个元素。
对于每个元素，它都会计算一个**谓词（predicate）**，即一个返回 `true` 或 `false` 的函数。
如果谓词返回 `true`，该元素就会包含在输出中。
如果返回 `false`，则会跳过该元素。
元素的原始顺序始终保持不变。

可以把它想象成门口的保安：排队中的每个元素都会根据规则接受检查，只有通过检查的元素才会被放行。

### 语法

```csharp
IEnumerable<T> result = source.Where(element => condition);
```

- `source` 是任何 `IEnumerable<T>`（数组、列表等）
- Lambda 表达式 `element => condition` 即为谓词
- 结果是一个延迟执行的序列，调用 `.ToArray()` 或 `.ToList()` 可将其具体化

### 示例

```csharp
// 过滤长度超过 3 个字符的字符串
string[] words = { "hi", "hello", "hey", "greetings" };
string[] longWords = words.Where(w => w.Length > 3).ToArray();
// longWords: ["hello", "greetings"]

// 从集合中过滤偶数
int[] values = { 10, 15, 20, 25, 30 };
int[] evens = values.Where(v => v % 2 == 0).ToArray();
// evens: [10, 20, 30]

// 过滤低于价格阈值的产品
double[] prices = { 5.99, 12.50, 3.25, 8.00 };
double[] affordable = prices.Where(p => p < 10.0).ToArray();
// affordable: [5.99, 3.25, 8.00]
```

请注意，输出始终保持元素在输入中出现的相同顺序。
`Where` 从不重新排列任何内容，它只决定哪些保留、哪些舍弃。

### 常见模式

| 模式 | 示例谓词 |
| --- | --- |
| 比较 | `x => x > 100` |
| 相等性 | `x => x == "active"` |
| 字符串检查 | `x => x.StartsWith("A")` |
| Null 防护 | `x => x != null` |
| 组合条件 | `x => x > 0 && x < 100` |

### 你的任务

编写一个方法，接收一个整数数组，并返回一个**仅包含正整数**（严格大于零的值）的新数组，同时保留它们的原始顺序。

- 零**不是**正数，应予以排除
- 负数应予以排除
- 如果没有正数元素，返回一个空数组
- 如果所有元素都是正数，则返回全部元素

### 方法签名

```csharp
public static int[] FilterPositives(int[] numbers)
```

### 预期结果

```scss
FilterPositives([-1, 2, -3, 4, -5]) -> [2, 4]
FilterPositives([0, 0, 0])          -> []
FilterPositives([7, 14, 21])        -> [7, 14, 21]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] FilterPositives(int[] numbers)
    {
        // 只保留严格大于零的元素
        return numbers.Where(n => n > 0).ToArray();
    }
}
```
