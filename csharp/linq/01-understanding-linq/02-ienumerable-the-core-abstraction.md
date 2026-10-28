### IEnumerable<T> - LINQ 的基石

你将用到的每一个 LINQ 方法（`Where`、`Select`、`Sum`、`OrderBy`、`Any` 以及其他数十个方法）都被定义在同一个接口的扩展方法上：`IEnumerable<T>`。
该接口表示*任何可以逐个迭代的元素序列*。
数组实现了它，列表（List）实现了它，HashSet、Queue、Stack、字典键集合，它们都实现了 `IEnumerable<T>`。

这非常强大，因为当你编写一个接收 `IEnumerable<T>` 而不是像 `int[]` 或 `List<int>` 这样的具体类型的方法时，你的方法无需修改即可适用于**每一种集合类型**。
这是 .NET 生态系统中最重要的设计决策之一。

### 工作原理

可以将 `IEnumerable<T>` 视为一份契约，它表明：“我可以逐个向你提供我的元素。”
它不承诺支持随机访问（如使用 `[i]` 进行索引），不承诺提供 `.Count` 属性，也不承诺你可以添加或删除项目。
它只承诺可以进行迭代。

由于 LINQ 方法建立在这个最小契约之上，因此它们具有通用性。
当你将 LINQ 方法链式连接在一起时，每个方法都会消费一个 `IEnumerable<T>` 并生成一个新的 `IEnumerable<T>`，从而形成一个管道。

### 语法

```csharp
// 通过 IEnumerable<T> 接收任意集合类型
public static double ProcessValues(IEnumerable<double> values)
{
    // 'values' 参数上可以使用所有 LINQ 方法
    return values.SomeLinqMethod();
}
```

### 示例

```csharp
// 这个方法适用于任何字符串集合
public static int CountLongWords(IEnumerable<string> words)
{
    return words.Where(w => w.Length > 5).Count();
}

// 以下所有调用都能正常工作：数组、列表等等：
CountLongWords(new string[] { "cat", "elephant", "dog" });   // 1
CountLongWords(new List<string> { "extraordinary", "hi" });   // 1
CountLongWords(new HashSet<string> { "ab", "cdef", "ghijkl" }); // 1
```

```csharp
// 过滤并聚合温度
public static double AverageFreezing(IEnumerable<double> temps)
{
    return temps.Where(t => t < 0.0).Average();
}

// 适用于任何序列：
AverageFreezing(new double[] { -5.0, 10.0, -3.0, 22.0 }); // -4.0
AverageFreezing(new List<double> { -1.0, -2.0 });          // -1.5
```

### IEnumerable<T> 上的常用 LINQ 方法

| 方法 | 描述 | 返回值 |
| --- | --- | --- |
| `Where(predicate)` | 筛选符合条件的元素 | `IEnumerable<T>` |
| `Select(transform)` | 转换每个元素 | `IEnumerable<TResult>` |
| `Sum()` | 将数值元素相加 | `int`、`double` 等 |
| `Count()` | 统计元素数量 | `int` |
| `Any(predicate)` | 检查是否有任何元素匹配 | `bool` |
| `First(predicate)` | 返回第一个匹配的元素 | `T` |

### 为什么使用 IEnumerable<T> 而不是具体类型？

如果你编写了一个接收 `int[]` 的方法，传入 `List<int>` 的调用方就需要先调用 `.ToArray()`。
如果你接收的是 `List<int>`，传入数组的调用方就需要调用 `.ToList()`。
而通过接收 `IEnumerable<int>`，**所有调用方都可以直接传入他们的集合**，无需进行任何转换。
这就是面向接口编程，而不是面向实现编程。

### 你的任务

编写一个接收 `IEnumerable<int>` 并返回序列中**所有正数之和**的方法。
负数和零应排除在求和之外。
如果没有正数，则返回 `0`。

因为参数是 `IEnumerable<int>`，所以无论调用方传入的是数组、列表还是任何其他集合，你的方法都能正常工作。

### 方法签名

```csharp
public static int SumPositives(IEnumerable<int> source)
```

### 预期结果

```scss
SumPositives([1, -2, 3, -4, 5])  -> 9
SumPositives([-1, -2, -3])       -> 0
SumPositives([10, 20, 30])       -> 60
SumPositives([])                 -> 0
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int SumPositives(IEnumerable<int> source)
    {
        // 先过滤出正数，再求和（没有元素时 Sum 返回 0）
        return source.Where(n => n > 0).Sum();
    }
}
```
