### Aggregate 操作符 - 通用折叠操作

在 LINQ 中，你可能已经用过 `Sum()`、`Min()`、`Max()` 和 `Count()` 来将集合归约（reduce）为一个单一值。
但如果你需要进行一种没有内置方法的归约操作怎么办？
这就是 `Aggregate` 大显身手的地方。
它是**通用的折叠操作（fold）**，是所有那些特化方法所基于的基础操作。
任何时候你需要将序列中的每个元素组合成一个累加结果，`Aggregate` 都是首选工具。

### 工作原理

`Aggregate` 逐个遍历序列中的元素，同时维护一个**累加器（accumulator）**：一个在每一步都会更新的运行结果。
最简单的重载 `Aggregate(func)` 将**第一个元素**作为初始累加器值，然后将你的组合函数应用于累加器和每个后续元素。

把它想象成一个从山上滚下来的雪球：雪球以第一个元素开始，它遇到的每个新元素都会通过你的函数被压缩进去。
在最后一个元素之后，你就得到了最终的雪球，即你的结果。

因为每个元素都恰好被访问**一次**，所以 `Aggregate` 的运行时间为 **O(N)**，其中 N 是序列中元素的数量。

### 语法

```csharp
// 最简单的重载：第一个元素成为初始累加器
TSource result = source.Aggregate((accumulator, currentElement) => combinedValue);

// 带有显式种子值的重载
TAccumulate result = source.Aggregate(seed, (accumulator, currentElement) => combinedValue);
```

Lambda 表达式接收两个参数：

- **accumulator** - 截至目前的运行结果
- **currentElement** - 序列中的下一个元素

它返回新的累加器值，该值将传递到下一次迭代中。

### 示例

```csharp
// 示例 1：使用分隔符拼接字符串
string[] words = { "Hello", "beautiful", "world" };
string sentence = words.Aggregate((acc, w) => acc + " " + w);
// acc 初始为 "Hello"
// 第 1 步："Hello" + " " + "beautiful" => "Hello beautiful"
// 第 2 步："Hello beautiful" + " " + "world" => "Hello beautiful world"

// 示例 2：查找最长的字符串
string[] names = { "Ada", "Grace", "Margaret", "Kay" };
string longest = names.Aggregate((acc, name) => name.Length > acc.Length ? name : acc);
// 结果："Margaret"

// 示例 3：对数字求和（重新实现 Sum()）
int[] scores = { 10, 20, 30, 40 };
int total = scores.Aggregate((acc, s) => acc + s);
// acc 初始为 10
// 第 1 步：10 + 20 = 30
// 第 2 步：30 + 30 = 60
// 第 3 步：60 + 40 = 100
```

请注意每个示例如何使用不同的组合操作（连接使用 `+`，比较使用三元运算符，加法使用 `+`）。
`Aggregate` 的强大之处在于**由你来定义操作**。

### 常见模式

| 模式 | Lambda | 作用 |
| --- | --- | --- |
| Sum | `(acc, x) => acc + x` | 将所有元素相加 |
| Min | `(acc, x) => x < acc ? x : acc` | 找出最小值 |
| Max | `(acc, x) => x > acc ? x : acc` | 找出最大值 |
| Concat | `(acc, s) => acc + s` | 拼接字符串 |
| **???** | `(acc, x) => acc * x` | 你来告诉我！ |

### 你的任务

编写一个方法，使用 `Aggregate` 计算整数数组中所有元素的**乘积（product）**。
乘积就是将所有元素相乘得到的结果，就像 `Sum` 将它们全部相加一样，你的方法将它们全部相乘。

例如：

- `[2, 3, 4]` 的乘积是 `2 × 3 × 4 = 24`
- `[5, 5]` 的乘积是 `5 × 5 = 25`
- 仅包含单个元素的数组应返回该元素本身

你**必须**使用 `Aggregate`，不允许使用手动循环。

### 方法签名

```csharp
public static int Product(int[] numbers)
```

### 预期结果

```scss
Product([1, 2, 3, 4, 5]) -> 120
Product([10, 20, 30]) -> 6000
Product([7]) -> 7
Product([2, 2, 2, 2]) -> 16
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int Product(int[] numbers)
    {
        // 以第一个元素作为初始累加器，依次与后续元素相乘
        return numbers.Aggregate((acc, n) => acc * n);
    }
}
```
