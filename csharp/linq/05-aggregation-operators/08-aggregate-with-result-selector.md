### 带有结果选择器（Result Selector）的 LINQ Aggregate

LINQ 的 `Aggregate` 方法是 C# 中类似于 fold 或 reduce 的操作：它遍历一个序列，逐步构建单个累加值。
**三参数重载** `Aggregate(seed, func, resultSelector)` 增加了一个强大的最终步骤：在所有元素都被折叠累加到累加器之后，**结果选择器（result selector）** 会将该累加器转换为完全不同的类型或形式。
这样就无需在聚合后执行单独的转换步骤。

### 工作原理

这三个参数各自承担不同的职责：

1. **种子（Seed）** - 累加器的初始值（可以是任何类型，而不仅限于元素类型）。
2. **函数（Func）** - 一个函数 `(accumulator, element) => newAccumulator`，每个元素调用一次。
3. **结果选择器（Result Selector）** - 一个函数 `accumulator => finalResult`，在处理完所有元素后调用一次。

因为 seed 可以与元素类型不同，所以你可以累加到元组（tuples）、匿名对象或自定义类型中。
然后结果选择器将该中间状态重塑为你所需的输出。

### 语法

```csharp
sequence.Aggregate(
    seed,                          // TAccumulate - 起始值
    (acc, element) => newAcc,      // Func<TAccumulate, TSource, TAccumulate>
    acc => finalResult             // Func<TAccumulate, TResult>
);
```

### 示例

```csharp
// 示例 1：查找最长的单词，并以字符串形式返回其长度
string[] words = { "apple", "banana", "fig" };
string result = words.Aggregate(
    "",
    (longest, word) => word.Length > longest.Length ? word : longest,
    longest => $"Longest has {longest.Length} letters"
);
// 结果："Longest has 6 letters"

// 示例 2：累加为一个元组 (Min, Max)，然后格式化它
int[] temps = { 72, 85, 63, 91, 78 };
string range = temps.Aggregate(
    (Min: int.MaxValue, Max: int.MinValue),
    (acc, t) => (Min: Math.Min(acc.Min, t), Max: Math.Max(acc.Max, t)),
    acc => $"Range: {acc.Min}-{acc.Max}"
);
// range："Range: 63-91"

// 示例 3：统计元音和辅音的数量，然后生成比例字符串
string text = "hello";
string ratio = text.Aggregate(
    (Vowels: 0, Consonants: 0),
    (acc, ch) => "aeiou".Contains(ch)
        ? (Vowels: acc.Vowels + 1, acc.Consonants)
        : (acc.Vowels, Consonants: acc.Consonants + 1),
    acc => $"{acc.Vowels}V:{acc.Consonants}C"
);
// ratio："2V:3C"
```

### 为什么使用三参数形式？

如果没有结果选择器，你需要链式调用一个额外的步骤：

```csharp
// 不使用结果选择器 - 两个步骤
var intermediate = items.Aggregate(seed, accumulate);
var final = Transform(intermediate);

// 使用结果选择器 - 一个简洁的表达式
var final = items.Aggregate(seed, accumulate, transform);
```

三参数形式使整个处理流水线保持为单个表达式，这在方法链中或将结果直接传递给其他方法时特别有用。

### 你的任务

编写一个方法，接收一个整数数组，并使用**三参数 `Aggregate`** 同时计算元素的总和与数量，然后将结果格式化为字符串。

- 使用**元组 `(Sum, Count)`** 作为 seed 和累加器类型。
- **累加器函数（accumulator function）** 应该同时更新当前的累加总和与元素计数。
- **结果选择器（result selector）** 应该生成精确格式为 `"Sum: N, Avg: M"` 的字符串，其中 `N` 为总和，`M` 为**整数平均值**（整数除法，向零截断）。

### 方法签名

```csharp
public static string GetStats(int[] numbers)
```

### 预期结果

```rust
GetStats([1, 2, 3, 4, 5])     -> "Sum: 15, Avg: 3"
GetStats([10, 20, 30])         -> "Sum: 60, Avg: 20"
GetStats([7])                  -> "Sum: 7, Avg: 7"
GetStats([1, 2])               -> "Sum: 3, Avg: 1"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string GetStats(int[] numbers)
    {
        return numbers.Aggregate(
            // 种子：元组 (Sum, Count)，初始均为 0
            (Sum: 0, Count: 0),
            // 累加器函数：同时更新总和与计数
            (acc, n) => (Sum: acc.Sum + n, Count: acc.Count + 1),
            // 结果选择器：使用整数除法计算平均值并格式化
            acc => $"Sum: {acc.Sum}, Avg: {acc.Sum / acc.Count}"
        );
    }
}
```
