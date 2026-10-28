### 使用 `OfType<T>` 按类型筛选

在 C# 中，集合有时会包含不同类型的元素。
例如一个 `object[]` 数组可能会将整数、字符串、布尔值和浮点数混合在一起。
当你需要仅提取特定类型的元素，并安全地忽略其他所有元素时，`OfType<T>` 就是最完美的工具。

### 工作原理

`OfType<T>` 是一个 LINQ 方法，它会遍历序列并对每个元素执行类型检查。
如果某个元素是类型 `T` 的实例（相当于使用 `is` 关键字），它就会被包含在输出中。
如果不是，则会被静默跳过：不会抛出异常，也不会报错。
通过筛选的元素会保留其原始顺序。

这与 `.Cast<T>()` 不同，后者在任何元素无法转换为 `T` 时都会抛出 `InvalidCastException`。
`OfType<T>` 是一种安全的替代方案。

### 语法

```csharp
IEnumerable<T> result = source.OfType<T>();
```

其中 `source` 可以是任何 `IEnumerable`（包括非泛型集合，如 `ArrayList` 或 `object[]`），而 `T` 是你想要提取的目标类型。

### 示例

```csharp
// 从混合集合中只提取字符串
object[] data = { 42, "apple", true, "banana", 3.14, "cherry" };
string[] fruits = data.OfType<string>().ToArray();
// 结果: ["apple", "banana", "cherry"]

// 从混合集合中提取 double
object[] measurements = { 1, 2.5, "N/A", 4.0, false, 7.8 };
double[] values = measurements.OfType<double>().ToArray();
// 结果: [2.5, 4.0, 7.8]
// 注意：整数 1 不会被包含，int 和 double 是不同的类型！

// 对空序列同样适用
object[] empty = { };
bool[] flags = empty.OfType<bool>().ToArray();
// 结果: []（空数组）
```

### 重要细节：精确类型匹配

`OfType<T>` 检查元素**是否属于**类型 `T`。
装箱后的 `int` **不是** `double`，即使在普通 C# 代码中整数可以隐式转换为浮点数。
当值被装箱为 `object` 时，这些隐式转换并不适用。

```csharp
object[] nums = { 1, 2.0, 3 };
double[] doubles = nums.OfType<double>().ToArray();
// 结果: [2.0]，整数 1 和 3 不是 double！
```

### 你的任务

编写一个方法，接收一个混合类型的 `object[]` 数组，并仅返回其中的 `int` 值，同时保持它们的原始顺序。

例如，给定 `[1, "hello", 2, 3.5, 3, true]`，其中的整数是 `1`、`2` 和 `3`。
字符串 `"hello"`、双精度浮点数 `3.5` 和布尔值 `true` 都应被排除。

### 方法签名

```csharp
public static int[] GetIntegers(object[] items)
```

### 预期结果

```css
GetIntegers([1, "hello", 2, 3.5, 3, true]) -> [1, 2, 3]
GetIntegers(["a", "b", "c"]) -> []
GetIntegers([10, 20, 30]) -> [10, 20, 30]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] GetIntegers(object[] items)
    {
        // OfType<int> 只保留 int 类型的元素，自动跳过 null 和其他类型
        return items.OfType<int>().ToArray();
    }
}
```
