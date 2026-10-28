### `Cast<T>` vs `OfType<T>` - 非泛型序列上的类型转换

在 C# 中，你经常会遇到像 `ArrayList` 这样的非泛型集合，或者返回 `object[]` 的方法。
当你需要从这些异构序列中处理特定类型时，LINQ 提供了两个操作符：`Cast<T>` 和 `OfType<T>`。
理解它们之间的区别至关重要：其中一个会在遇到混合类型数据时使程序崩溃，而另一个则能优雅地处理。

### 它们的工作原理

**`Cast<T>()`** 会尝试将序列中的*每一个元素*都转换为类型 `T`。
哪怕只有一个元素无法转换，它也会抛出 `InvalidCastException`。
当你*确切知道*所有元素都是类型 `T` 时（例如，遍历一个只填充了整数的遗留 `ArrayList`），这是正确的选择。

**`OfType<T>()`** 会检查每个元素，并*静默跳过*任何不是类型 `T` 的元素。
只有通过类型检查的元素才会包含在结果序列中。
当集合包含混合类型，并且你只想提取你关心的那些类型时，这是正确的选择。

### 语法

```csharp
// Cast<T> - 每个元素都必须能转换为 T
IEnumerable<T> result = nonGenericSequence.Cast<T>();

// OfType<T> - 只保留类型为 T 的元素
IEnumerable<T> result = nonGenericSequence.OfType<T>();
```

两者都是 `IEnumerable`（而非 `IEnumerable<T>`）的扩展方法，这就是为什么它们在处理非泛型集合时至关重要。

### 示例

```csharp
// 示例 1：当所有元素都匹配时，Cast<T> 可以正常工作
object[] prices = { 9.99, 14.50, 3.25 };
double[] allPrices = prices.Cast<double>().ToArray();
// 结果：[9.99, 14.50, 3.25] - 所有元素都是 double，没有问题

// 示例 2：当类型混合时，Cast<T> 会抛出异常
object[] mixed = { 10, "oops", 30 };
// mixed.Cast<int>().ToArray(); // 崩溃！在 "oops" 上抛出 InvalidCastException

// 示例 3：OfType<T> 安全地过滤混合集合
object[] inventory = { 10, "keyboard", 25.5, "mouse", false };
int[] numbers = inventory.OfType<int>().ToArray();
// 结果：[10] - 只有真正的 int 元素，double 和其他类型都被跳过

// 示例 4：OfType<T> 与更多 LINQ 组合使用
object[] data = { 1, 2.5, 3, 4.7, 5 };
int sum = data.OfType<int>().Where(n => n > 2).Sum();
// 结果：8（只有 3 + 5，因为 2.5 和 4.7 是 double，不是 int）
```

### 常见模式

| 场景 | 使用 | 原因 |
| --- | --- | --- |
| 类型已知的遗留 `ArrayList` | `Cast<T>()` | 保证所有元素均为 `T` |
| 包含混合类型的 `object[]` | `OfType<T>()` | 安全地忽略不兼容的元素 |
| 在 `OfType<T>()` 之后 | 链式调用 `.Select()`、`.Where()` 等 | 结果为 `IEnumerable<T>`，完全兼容 LINQ |

### 核心要点

`OfType<T>()` 本质上是过滤*和*类型转换的结合。
它首先检查 `element is T`，如果为 true，则产出（yield）转换后的结果。
这意味着输出保留了匹配元素的原始相对顺序。

### 你的任务

编写一个方法，接收包含字符串、整数、布尔值以及可能存在的其他类型的混合 `object[]`。
你的方法应该从数组中提取**仅为字符串的元素**，计算**每个字符串的长度**，并将这些长度作为 `int[]` 返回。
这些长度在结果中的相对顺序必须与字符串在输入数组中出现的相对顺序相同。

### 方法签名

```csharp
public static int[] SafeGetLengths(object[] items)
```

### 预期结果

```css
SafeGetLengths(["hello", 42, "world", true, "hi"]) -> [5, 5, 2]
SafeGetLengths([1, 2, 3]) -> []
SafeGetLengths(["cat", "dog"]) -> [3, 3]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] SafeGetLengths(object[] items)
    {
        // OfType<string>() 只保留字符串元素（会跳过 null 和其他类型），并保持原有顺序
        return items
            .OfType<string>()
            .Select(s => s.Length)
            .ToArray();
    }
}
```
