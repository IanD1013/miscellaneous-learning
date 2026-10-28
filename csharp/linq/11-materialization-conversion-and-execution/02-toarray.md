### ToArray - 将 LINQ 结果具体化为数组

当你链式调用诸如 `Where`、`OrderBy` 或 `Select` 等 LINQ 方法时，其结果是一个 `IEnumerable<T>`，一个尚未求值的惰性序列。
要真正生成一个具体的集合，你需要**具体化**（materialize）它。
大多数开发者默认会使用 `ToList()`，但在具体化后不需要添加或删除元素时，`ToArray()` 通常是更好的选择。

### 为什么选择 ToArray 而不是 ToList？

`List<T>` 内部使用了一个数组，该数组可能会超出实际所需并具有**额外容量**。
当你调用 `ToList()` 时，生成的列表分配的内存可能会超过元素数量的实际需求。
相比之下，`ToArray()` 生成的 `T[]` 其**大小恰好**能够容纳所有元素，没有容量浪费。

在以下情况下使用 `ToArray()`：

- 结果是**只读**的 - 你稍后不会添加或删除元素
- 某个 API 或方法签名**需要一个数组**（`T[]`）
- 你希望对固定大小的结果获得微弱的**内存优势**
- 你正在将数据传递给能够从数组访问模式中受益的性能敏感代码

### 语法

```csharp
// 通用模式：以 ToArray() 结尾的 LINQ 链式调用
T[] result = source
    .SomeLinqMethod()
    .AnotherLinqMethod()
    .ToArray();
```

### 示例

```csharp
// 示例 1：过滤并具体化为数组
string[] words = { "apple", "ant", "banana", "avocado", "cherry" };
string[] aWords = words.Where(w => w.StartsWith("a")).ToArray();
// aWords 为 ["apple", "ant", "avocado"] - 一个 Length 为 3 的 string[]

// 示例 2：转换并具体化
double[] prices = { 19.99, 5.50, 42.00, 8.75 };
string[] labels = prices.Select(p => $"${p:F2}").ToArray();
// labels 为 ["$19.99", "$5.50", "$42.00", "$8.75"]

// 示例 3：排序、截取子集并具体化
int[] scores = { 72, 95, 88, 61, 100, 84 };
int[] bottom3 = scores.OrderBy(s => s).Take(3).ToArray();
// bottom3 为 [61, 72, 84] - 最低的三个分数
```

### 本练习中常用的 LINQ 方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `OrderByDescending(x => x)` | 将元素从最高到最低排序 | `nums.OrderByDescending(n => n)` |
| `OrderBy(x => x)` | 将元素从最低到最高排序 | `nums.OrderBy(n => n)` |
| `Take(count)` | 从序列中返回前 `count` 个元素 | `sequence.Take(5)` |
| `ToArray()` | 将序列具体化为 `T[]` 数组 | `sequence.ToArray()` |
| `ToList()` | 将序列具体化为 `List<T>` | `sequence.ToList()` |

### 你的任务

编写一个接受整数数组和数量 `n` 的方法，然后以 `int[]` 的形式返回**前 N 个最大值**。
返回的数组应包含恰好 `n` 个按从大到小排序的元素。

例如，给定分数 `[45, 92, 78, 100, 55]` 和 `n = 2`，你应该返回两个最高值：`[100, 92]`。

### 方法签名

```csharp
public static int[] GetTopN(int[] numbers, int n)
```

### 预期结果

```scss
GetTopN([3, 1, 4, 1, 5, 9, 2, 6], 3) -> [9, 6, 5]
GetTopN([10, 20, 30], 1) -> [30]
GetTopN([7, 7, 7, 7], 2) -> [7, 7]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] GetTopN(int[] numbers, int n)
    {
        // 从大到小排序，取前 n 个，并具体化为数组
        return numbers
            .OrderByDescending(x => x)
            .Take(n)
            .ToArray();
    }
}
```
