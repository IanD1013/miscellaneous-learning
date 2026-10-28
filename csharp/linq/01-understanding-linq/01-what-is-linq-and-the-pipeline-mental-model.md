### LINQ：数据管道

LINQ（Language Integrated Query，语言集成查询）是 C# 中的一组功能，允许你直接在 C# 代码中使用清晰、易读的语法来查询和转换集合。
你无需编写繁琐的手动循环来进行搜索、过滤和重塑数据，而是可以将意图表达为**操作链（chain of operations）**。
每个操作接收一个输入序列，对其进行处理，并输出一个新的序列。
这种链式调用使得 LINQ 的使用体验就像一个**管道（pipeline）**。

### 管道的工作原理

想象水流经一系列连接在一起的水管。
每根水管只做一件事：这一根过滤杂质，另一根添加矿物质，再下一根调节水温。
数据流经 LINQ 管道的方式完全相同。
你从一个集合（数组、列表或任何 `IEnumerable<T>`）开始，连接一个或多个**操作符（operators）**，最终在末端得到一个转换后的序列。

关键要点：**LINQ 操作符不会修改原始集合。
** 它们会生成一个全新的序列。
这意味着你可以安全地链式调用操作，而无需担心产生副作用。

### `Where` 操作符 - 你的第一个过滤器

`Where` 是最基础的 LINQ 操作符之一。
它充当**过滤器（filter）**：检查序列中的每个元素，应用一个条件（称为**谓词（predicate）**），并仅放行满足该条件的元素。
不匹配的元素将直接从输出中丢弃。

谓词是一个小型函数（通常是 lambda 表达式），它接收一个元素并返回 `true` 或 `false`。

### 语法

```csharp
// 通用模式
sequence.Where(element => condition)

// Where 返回 IEnumerable<T>，因此通常需要将其转换回数组或列表
sequence.Where(element => condition).ToArray()
sequence.Where(element => condition).ToList()
```

### 示例

```csharp
// 过滤以 'A' 开头的字符串
string[] names = { "Alice", "Bob", "Anna", "Charlie" };
string[] aNames = names.Where(name => name.StartsWith("A")).ToArray();
// 结果: ["Alice", "Anna"]

// 过滤高于阈值的价格
double[] prices = { 5.99, 12.50, 3.25, 8.00, 15.75 };
double[] expensive = prices.Where(p => p > 10.0).ToArray();
// 结果: [12.50, 15.75]

// 从集合中过滤掉负数
int[] temps = { -5, 12, -3, 0, 8, -1, 20 };
int[] nonNegative = temps.Where(t => t >= 0).ToArray();
// 结果: [12, 0, 8, 20]
```

请注意，在每个示例中，原始数组均保持不变。
`Where` 会创建一个仅包含匹配元素并保留其原始顺序的全新序列。

### 实用参考

| 概念 | 说明 | 示例 |
| --- | --- | --- |
| `Where` | 根据谓词过滤元素 | `nums.Where(x => x > 0)` |
| `%` (求模/取余) | 返回除法的余数 | `7 % 2` 等于 `1` |
| `.ToArray()` | 将 `IEnumerable<T>` 转换为数组 | `seq.Where(...).ToArray()` |
| Lambda `=>` | 定义内联函数 | `x => x > 5` |

### 你的任务

编写一个方法，接收一个整数数组，并返回一个**新数组**，其中仅包含输入中的**偶数**，且保持其原始顺序。

请记住：

- 偶数是指能够被 2 整除且没有余数的数字。
- 返回结果应该是一个 `int[]` 数组。
- 如果没有偶数，返回一个空数组。
- 如果输入数组为空，返回一个空数组。

### 方法签名

```csharp
public static int[] GetEvens(int[] numbers)
```

### 预期结果

```scss
GetEvens([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]
GetEvens([7, 11, 13]) -> []
GetEvens([0, 2, 4]) -> [0, 2, 4]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] GetEvens(int[] numbers)
    {
        // 用 Where 只保留偶数，再转换回数组
        return numbers.Where(n => n % 2 == 0).ToArray();
    }
}
```
