### 投影：逐个元素转换序列

在 LINQ 中，`Select` 运算符将序列中的每个元素投影为一种新的形式。
但在底层究竟发生了什么？
其核心在于，投影是一个**迭代器**（iterator），它遍历源集合，对每个元素应用转换，并一次 **yield**（产出）一个结果，而绝不会将整个输出缓冲到内存中。

理解这一机制对于编写内存高效的管道以及深入理解 C# 中延迟执行（deferred execution）的真正工作原理至关重要。

### 迭代器方法的工作原理

当一个方法包含 `yield return` 语句时，C# 会将其编译为一个实现 `IEnumerable<T>` 的**状态机**（state machine）。
该方法在被调用时并不会立即执行方法体，而是返回一个枚举器对象。
每次调用方请求下一个元素时（通过 `foreach` 或 `MoveNext()`），执行会从上次 yield 的地方恢复，处理下一个元素，然后再次挂起。

这意味着：

- 不会创建任何中间列表或数组
- 元素是按需**延迟**（lazily）生成的
- 源集合只会被精确遍历一次

### 语法

```csharp
public static IEnumerable<T> MyIterator(IEnumerable<T> source)
{
    foreach (var item in source)
    {
        yield return /* 转换后的元素 */;
    }
}
```

返回类型必须是 `IEnumerable<T>`、`IEnumerable`、`IEnumerator<T>` 或 `IEnumerator`。
`yield return` 语句一次产出一个元素。

### 示例

假设你想在不使用 LINQ 的情况下将名称列表转换为大写：

```csharp
public static IEnumerable<string> ToUpperAll(string[] names)
{
    foreach (var name in names)
    {
        yield return name.ToUpper();
    }
}
// ToUpperAll(["alice", "bob"]) 产出 "ALICE", "BOB"
```

或者计算序列中每个数字的平方：

```csharp
public static IEnumerable<int> SquareAll(int[] values)
{
    foreach (var v in values)
    {
        yield return v * v;
    }
}
// SquareAll([3, 5]) 产出 9, 25
```

请注意，这两个示例都没有分配 `List<int>` 或数组，结果都是逐个流式输出的。

### 延迟执行的实际应用

因为迭代器方法是惰性的，所以在枚举开始之前不会执行任何实际工作：

```csharp
var result = SquareAll(new[] { 1, 2, 3 }); // 尚未进行任何计算
foreach (var item in result) // 现在每个元素才按需计算
{
    Console.WriteLine(item);
}
```

这也是驱动 LINQ 的 `Select`、`Where` 以及其他流式运算符的同一种延迟执行模型。

### 你的任务

编写方法 `DoubleAll`，该方法接收一个整数数组，并返回一个 `IEnumerable<int>`，其中每个元素都是输入中对应元素乘以 2 的结果。

**要求：**

- 使用 `foreach` 循环和 `yield return` 来生成每个转换后的元素
- **不要**使用 LINQ 的 `Select` - 本题的目标是让你亲自实现投影模式
- 该方法应妥善处理空数组（不产出任何元素）
- 负数与正数一样需要翻倍

### 方法签名

```csharp
public static IEnumerable<int> DoubleAll(int[] numbers)
```

### 预期结果

```scss
DoubleAll([1, 2, 3, 4])    -> [2, 4, 6, 8]
DoubleAll([0])              -> [0]
DoubleAll([])               -> []
DoubleAll([-3, 5])          -> [-6, 10]
DoubleAll([100, -100, 50])  -> [200, -200, 100]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static IEnumerable<int> DoubleAll(int[] numbers)
    {
        foreach (int n in numbers)
        {
            // 将每个元素乘以 2 后逐个产出
            yield return n * 2;
        }
    }
}
```
