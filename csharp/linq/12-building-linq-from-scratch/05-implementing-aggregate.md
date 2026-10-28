### 理解 Fold / Reduce

在函数式编程中，**fold**（也称为 **reduce**）是集合上最基础的操作之一。
它通过重复应用组合函数，将一系列值合并为一个结果。
在 C# 中，LINQ 以 `Aggregate` 的形式提供了该功能，但对于任何从事数据转换、自定义管道或需要关注 LINQ 开销的性能敏感型代码的开发者来说，理解其底层机制都是至关重要的。

### 工作原理

fold 操作包含三个要素：

1. **种子值**（也称为初始累加器） - 处理任何元素之前的起始点。
2. **累加器变量** - 在遍历集合的过程中保存当前计算的结果。
3. **组合操作** - 一个接收当前累加器和下一个元素作为参数并生成新累加器值的函数。

遍历每个元素并每次更新累加器。
当处理完所有元素后，累加器中保存的就是最终结果。

你可以把它想象成滚下山的雪球：它以特定大小（种子）开始，遇到的每个元素都会被压入其中（组合步骤），直到到达山底得到完全累积的结果。

### 语法

```csharp
// 手动 fold/reduce 的通用模式
ResultType accumulator = seedValue;
for (int i = 0; i < collection.Length; i++)
{
    accumulator = CombineFunction(accumulator, collection[i]);
}
// 此时 accumulator 保存最终结果
```

关键决策在于：

- 种子应该是什么类型和值？
- 使用什么操作将累加器与下一个元素组合？

### 示例

```csharp
// 示例 1：整数求和
// 种子：0（加法的单位元）
int[] scores = { 88, 92, 75, 100 };
int total = 0;
for (int i = 0; i < scores.Length; i++)
{
    total = total + scores[i]; // 通过加法组合
}
// total == 355

// 示例 2：查找最大值
// 种子：第一个元素（如果数组可能为空，则使用 int.MinValue）
double[] temps = { 22.5, 18.3, 31.7, 27.0 };
double maxTemp = temps[0];
for (int i = 1; i < temps.Length; i++)
{
    maxTemp = temps[i] > maxTemp ? temps[i] : maxTemp;
}
// maxTemp == 31.7

// 示例 3：使用分隔符拼接字符串
string[] words = { "fold", "is", "powerful" };
sring sentence = words[0];
for (int i = 1; i < words.Length; i++)
{
    sentence = sentence + " " + words[i];
}
// sentence == "fold is powerful"
```

请注意，**种子值** 会根据操作的不同而发生变化：加法为 `0`，最大值为第一个元素，拼接字符串为第一个单词。
通常的选择是组合操作的**单位元**（identity element）：即能使另一个操作数保持不变的值，例如加法的 `0` 和乘法的 `1`。
当某个操作没有方便的单位元时（如最大值），或者单位元会导致不想要的结果时（例如拼接字符串时出现前导分隔符），可以以第一个元素作为种子，并对其余元素进行 fold 操作。

### 常见模式

| 操作 | 种子 | 组合步骤 |
| --- | --- | --- |
| 求和 | `0` | `acc + element` |
| 乘积 | `1` | `acc * element` |
| 统计匹配项 | `0` | `acc + (condition ? 1 : 0)` |
| 字符串连接 | `""` 或第一个元素 | `acc + separator + element` |
| 逻辑与 | `true` | `acc && condition(element)` |
| 逻辑或 | `false` | `acc \|\| condition(element)` |

### 需要考虑的边界情况

- **空集合**：当没有元素时，fold 应该返回什么？答案是种子值本身，因为没有执行任何组合步骤。
- **单元素**：结果应该是该单个元素与种子组合后的值。
- **溢出**：当组合较大的数字时，请考虑累加器类型是否能够容纳该结果。

### 从 MultiplyAll 到 Aggregate

你的循环本质上就是 `Aggregate` 内部所做的事情，只不过操作被固定为乘法。
LINQ 的版本则将种子和组合步骤作为参数传入：

```csharp
public static TAccumulate Aggregate<TSource, TAccumulate>(
    this IEnumerable<TSource> source,
    TAccumulate seed,
    Func<TAccumulate, TSource, TAccumulate> func)
```

将硬编码的 `*` 替换为对 `func` 的调用，你就得到了通用版本。
`this` 关键字使其成为一个扩展方法，你将在课程 Writing Your Own Extension Method Operator 中亲自编写它。

### 你的任务

编写一个方法，使用手动累加器循环计算整数数组中所有元素的**乘积**（product）。
不要使用任何 LINQ 方法，自行实现 fold 逻辑。

**规则：**

- 如果数组为空，返回 `1`（乘法的单位元）。
- 使用 `long` 累加器，而不仅仅是 `long` 返回类型。在 `int` 内部进行乘法运算会在结果转换之前发生溢出，因此 `MultiplyAll([100000, 100000])` 必须返回 `10000000000`。
- 负数应通过乘法自然处理。
- 数组中的零意味着整个乘积为零。

### 方法签名

```csharp
public static long MultiplyAll(int[] numbers)
```

### 预期结果

```scss
MultiplyAll([1, 2, 3, 4, 5]) -> 120
MultiplyAll([10, 20, 30]) -> 6000
MultiplyAll([]) -> 1
MultiplyAll([7]) -> 7
MultiplyAll([3, 0, 5]) -> 0
MultiplyAll([100000, 100000]) -> 10000000000
```

### 解答

```csharp
using System;

public class Solution
{
    public static long MultiplyAll(int[] numbers)
    {
        // 种子为 1（乘法的单位元），使用 long 累加器避免 int 溢出
        long product = 1;
        for (int i = 0; i < numbers.Length; i++)
        {
            // 组合步骤：累加器乘以下一个元素（int 会先提升为 long）
            product = product * numbers[i];
        }
        return product;
    }
}
```
