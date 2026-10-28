### LINQ 中的带种子 Aggregate

LINQ 的 `Aggregate` 方法通过对所有元素应用一个函数，将一个序列缩减为单个值。
基本重载 `Aggregate(func)` 使用第一个元素作为初始累加器，但当你需要累加器从特定值开始时（例如从 100 开始的累计总和，或者构建以标签开头的字符串），这就无法满足需求了。
**带种子重载** `Aggregate(seed, func)` 通过允许你提供一个显式的初始值解决了这个问题。

### 工作原理

当你调用 `Aggregate(seed, func)` 时，该方法将累加器初始化为 `seed`，然后遍历集合中的每个元素。
对于每个元素，它调用 `func(accumulator, currentElement)` 并将结果存储为新的累加器值。
在处理完所有元素后，返回最终的累加器值。

至关重要的是，即使集合为空，也会使用种子值，在这种情况下，将直接返回种子本身。
这与不带种子的重载不同，后者在空序列上会抛出 `InvalidOperationException`。

### 语法

```csharp
// 通用语法
collection.Aggregate(seed, (accumulator, element) => /* 组合逻辑 */);
```

`seed` 的类型决定了累加器的类型（以及返回值类型），该类型可以与元素类型不同。

### 示例

```csharp
// 从偏移量 1000 开始对数字求和
int[] scores = { 10, 20, 30 };
int total = scores.Aggregate(1000, (acc, s) => acc + s);
// total = 1060

// 根据列名构建 CSV 表头行
string[] columns = { "Name", "Age", "City" };
string header = columns.Aggregate("CSV:", (acc, col) => acc + "," + col);
// header = "CSV:,Name,Age,City"

// 从某个偏移量开始，统计满足条件的项
int[] values = { 3, 7, 2, 9, 1 };
int countAboveFive = values.Aggregate(0, (acc, v) => v > 5 ? acc + 1 : acc);
// countAboveFive = 2

// 以缩放因子作为种子进行乘法运算
int[] factors = { 2, 3, 4 };
int product = factors.Aggregate(10, (acc, f) => acc * f);
// product = 240 (10 * 2 * 3 * 4)
```

### 带种子与不带种子对比

| 重载 | 空集合 | 累加器起始值 | 返回类型 |
| --- | --- | --- | --- |
| `Aggregate(func)` | 抛出异常 | 第一个元素 | 与元素类型相同 |
| `Aggregate(seed, func)` | 返回 seed | seed 值 | 与 seed 类型相同 |

带种子的版本更安全、更灵活。
种子充当你操作的**恒等值**。

### 你的任务

编写一个方法，接收一个单词数组，并将它们拼接为一个单独的字符串，并以 `"Sentence:"` 为前缀。
每个单词与前缀之间（以及单词与单词之间）都应由一个空格分隔。

例如，给定 `["The", "quick", "fox"]`，结果应为 `"Sentence: The quick fox"`。

如果数组为空，结果应仅为 `"Sentence:"`（只有前缀，末尾没有空格）。

### 方法签名

```csharp
public static string BuildSentence(string[] words)
```

### 预期结果

```rust
BuildSentence(["Hello", "World", "Foo"]) -> "Sentence: Hello World Foo"
BuildSentence(["CSharp"]) -> "Sentence: CSharp"
BuildSentence([]) -> "Sentence:"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string BuildSentence(string[] words)
    {
        // 以 "Sentence:" 作为种子，每个单词前加一个空格后拼接
        // 空数组时直接返回种子 "Sentence:"
        return words.Aggregate("Sentence:", (acc, w) => acc + " " + w);
    }
}
```
