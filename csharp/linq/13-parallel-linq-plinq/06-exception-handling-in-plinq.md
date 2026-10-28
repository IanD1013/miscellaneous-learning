### PLINQ 中的异常处理

在使用 PLINQ 进行并行化工作时，异常的行为与顺序执行的代码不同。
由于多个线程并发执行，**可能会同时发生多个异常**。
PLINQ 会收集所有这些异常，并将它们包装在单个 `AggregateException` 中，该异常会在使用结果时（例如调用 `.ToArray()`、`.ToList()` 或使用 `foreach` 迭代时）被抛出。

理解这种模式对于编写健壮的并行代码至关重要：如果你只捕获单纯的 `DivideByZeroException`，你的并行查询将会因为未处理的 `AggregateException` 而崩溃。

### 工作原理

在顺序 LINQ 中，`.Select()` 投影中的异常会立即作为特定的异常类型（例如 `DivideByZeroException`）传播。
而在 PLINQ 中，运行时会将工作调度到多个线程上。
如果一个或多个分区抛出异常，PLINQ 会**推迟**这些异常，直到消费操作将结果具体化（materialize）为止。
此时，它会抛出一个 `AggregateException`，其 `InnerExceptions` 集合包含跨所有线程发生的每个单独异常。

这意味着：

1. 你必须捕获 `AggregateException`，而不是直接捕获内部异常类型。
2. `InnerExceptions` 属性（类型为 `ReadOnlyCollection<Exception>`）允许你访问每个单独的错误。
3. 你可以使用 `.Handle()` 或 `.Flatten()` 进行更高级的检查场景。

### 语法

```csharp
try
{
    var results = source
        .AsParallel()
        .Select(item => SomeRiskyOperation(item))
        .ToArray(); // <-- 异常在此处抛出
}
catch (AggregateException ex)
{
    // ex.InnerExceptions 包含所有单独的异常
    foreach (var inner in ex.InnerExceptions)
    {
        Console.WriteLine(inner.Message);
    }
}
```

### 示例

```csharp
// 示例 1：并行解析字符串 - 某些可能会失败
try
{
    string[] inputs = { "42", "abc", "7", "xyz" };
    int[] parsed = inputs
        .AsParallel()
        .Select(s => int.Parse(s)) // "abc" 和 "xyz" 将会抛出异常
        .ToArray();
}
catch (AggregateException ex)
{
    // ex.InnerExceptions 可能包含 2 个 FormatException
    Console.WriteLine($"Caught {ex.InnerExceptions.Count} errors");
}

// 示例 2：并行访问可空引用
try
{
    string[] words = { "hello", null, "world", null };
    int[] lengths = words
        .AsParallel()
        .Select(w => w.Length) // null 项会抛出 NullReferenceException
        .ToArray();
}
catch (AggregateException ex)
{
    // 检查每个内部异常
    foreach (var inner in ex.InnerExceptions)
    {
        Console.WriteLine($"Type: {inner.GetType().Name}");
    }
}

// 示例 3：成功的并行计算 - 无异常
int[] scores = { 90, 85, 78, 92 };
int[] curved = scores
    .AsParallel()
    .Select(s => s + 5)
    .ToArray();
Array.Sort(curved);
// curved 为 [83, 90, 95, 97]
```

### 关键要点

| 概念 | 详情 |
| --- | --- |
| `AggregateException` | 包装来自并行任务的一个或多个异常 |
| `.InnerExceptions` | 包含所有捕获错误的 `ReadOnlyCollection<Exception>` |
| 在消费时抛出 | 当发生 `.ToArray()`、`.ToList()` 或枚举时异常才会暴露出来 |
| 与顺序执行的区别 | 顺序 LINQ 直接抛出原始异常类型 |

### 你的任务

编写一个方法，接收一个整数数组和一个除数。
使用 `AsParallel()` 结合 `Select` 将每个数字除以该除数。
如果操作成功，以**已排序**的 `int[]` 形式返回结果。
如果在并行计算期间发生**任何**异常，捕获 `AggregateException` 并返回一个**空**的 `int[]`。

思考以下问题：

- 在 PLINQ 管道中，异常到底是在哪里被抛出的？
- 你需要捕获什么异常类型：内部异常还是包装异常？
- PLINQ 不保证顺序，那么你如何确保输出是排序后的结果？

### 方法签名

```csharp
public static int[] SafeParallelDivide(int[] numbers, int divisor)
```

### 预期结果

```scss
SafeParallelDivide([10, 20, 30], 5)    -> [2, 4, 6]
SafeParallelDivide([10, 20, 30], 0)    -> []
SafeParallelDivide([100, 50, 25], 25)  -> [1, 2, 4]
SafeParallelDivide([], 3)              -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] SafeParallelDivide(int[] numbers, int divisor)
    {
        try
        {
            // 异常在 ToArray() 具体化结果时抛出
            int[] results = numbers
                .AsParallel()
                .Select(n => n / divisor)
                .ToArray();

            // PLINQ 不保证顺序，因此手动排序
            Array.Sort(results);
            return results;
        }
        catch (AggregateException)
        {
            // 并行计算中的任何异常都被包装在 AggregateException 中
            return Array.Empty<int>();
        }
    }
}
```
