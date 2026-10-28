### LINQ Zip 运算符

处理两个相关的序列时，你经常需要将它们逐元素组合起来：将一个序列的第一个元素与另一个序列的第一个元素配对，第二个与第二个配对，依此类推。
这正是 `Zip` 运算符的作用。
它的命名来源于拉链（zipper）：两排独立的链齿交错咬合成对。

### 工作原理

`Zip` 同时遍历两个序列，并将相同索引处的元素进行配对。
你需要提供一个 **result selector**（结果选择器），即一个定义每对元素应如何组合的函数。
至关重要的是，只要**任一**序列的元素耗尽，`Zip` 就会立即停止。
如果一个序列有 5 个元素，而另一个序列有 3 个元素，你将刚好得到 3 个结果。
长度不匹配时不会抛出任何异常。

### 语法

```csharp
IEnumerable<TResult> Zip<TFirst, TSecond, TResult>(
    IEnumerable<TSecond> second,
    Func<TFirst, TSecond, TResult> resultSelector
)
```

你在第一个序列上调用 `Zip`，传入第二个序列，并提供一个 lambda 表达式，该表达式接收来自每个序列的一个元素并返回组合后的结果。

### 示例

```csharp
// 将姓名和分数组合成格式化字符串
string[] names = { "Alice", "Bob", "Carol" };
int[] scores = { 92, 87, 95 };

var results = names.Zip(scores, (name, score) => $"{name}: {score}");
// 结果：["Alice: 92", "Bob: 87", "Carol: 95"]

// 将对应的价格与数量相乘
double[] prices = { 10.0, 25.5, 8.0 };
int[] quantities = { 3, 1, 5 };

var totals = prices.Zip(quantities, (p, q) => p * q);
// 结果：[30.0, 25.5, 40.0]

// 长度不匹配 - Zip 在较短的序列处停止
int[] letters = { 1, 2, 3, 4, 5 };
int[] digits = { 10, 20 };

var paired = letters.Zip(digits, (l, d) => l + d);
// 结果：[11, 22] - 只有 2 个结果，而不是 5 个
```

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 组合为元组 | `a.Zip(b, (x, y) => (x, y))` |
| 计算差值 | `a.Zip(b, (x, y) => x - y)` |
| 构建格式化输出 | `a.Zip(b, (x, y) => $"{x}={y}")` |
| 比较元素 | `a.Zip(b, (x, y) => x > y)` |

### 你的任务

编写一个方法，接收两个整型数组并返回一个新的整型数组，其中每个元素是两个输入数组中对应元素的**和**。
如果数组的长度不同，结果应该只包含与较短数组相同数量的元素。

### 方法签名

```csharp
public static int[] ZipToSum(int[] a, int[] b)
```

### 预期结果

```css
ZipToSum([1, 2, 3], [4, 5, 6])       -> [5, 7, 9]
ZipToSum([10, 20], [1, 2, 3])         -> [11, 22]
ZipToSum([], [1, 2, 3])               -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ZipToSum(int[] a, int[] b)
    {
        // 按位置配对并求和，Zip 会在较短的数组处停止
        return a.Zip(b, (x, y) => x + y).ToArray();
    }
}
```
