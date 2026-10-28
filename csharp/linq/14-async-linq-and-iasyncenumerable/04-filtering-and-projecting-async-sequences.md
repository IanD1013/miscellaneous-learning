### 使用 `IAsyncEnumerable<T>` 的异步 LINQ 风格管道

在实际应用中，数据通常以异步方式到达，例如来自数据库游标、gRPC 流、分页 API 或文件读取器。
C# 提供了 `IAsyncEnumerable<T>` 来对这些惰性、异步序列进行建模。
与 `IEnumerable<T>` 不同，异步版本在基础框架中**并未**自带诸如 `.Where()` 和 `.Select()` 之类的内置 LINQ 运算符。
为了将过滤和转换串联起来，你需要编写**异步迭代器方法**，这些方法消费一个 `IAsyncEnumerable<T>` 并产生另一个。

### 工作原理

异步迭代器方法：

- 返回 `IAsyncEnumerable<T>`（或 `IAsyncEnumerator<T>`）
- 使用 `yield return` 逐个产出元素
- 使用 `await foreach` 消费上游异步序列
- 可以包含用于真正异步工作的 `await` 表达式

通过组合这些方法，你可以构建一个**管道**：每个阶段惰性地从上一个阶段拉取数据、处理该元素并将其推送至下游。
不会分配任何中间集合，元素逐一流经管道。

### 语法

```csharp
// 生产异步序列
async IAsyncEnumerable<T> ProduceAsync()
{
    // 异步地产出元素
    yield return someValue;
    await Task.Delay(10); // 模拟异步操作
    yield return anotherValue;
}

// 消费并转换异步序列
async IAsyncEnumerable<T> TransformAsync(IAsyncEnumerable<T> source)
{
    await foreach (var item in source)
    {
        // 处理元素，可选择是否 yield return 它
        yield return ProcessedItem;
    }
}
```

### 示例

假设你正在从传感器流读取温度读数，并且只需要高于冰点的读数，并将其转换为华氏度：

```csharp
// 阶段 1：源 - 产出原始读数
async IAsyncEnumerable<double> ReadTemperaturesAsync(double[] readings)
{
    foreach (var r in readings)
    {
        await Task.CompletedTask; // 真实异步 I/O 的占位符
        yield return r;
    }
}

// 阶段 2：过滤 - 只保留高于冰点的读数
async IAsyncEnumerable<double> AboveFreezingAsync(IAsyncEnumerable<double> source)
{
    await foreach (var temp in source)
    {
        if (temp > 0.0)
            yield return temp;
    }
}

// 阶段 3：映射 - 将摄氏度转换为华氏度
async IAsyncEnumerable<double> ToFahrenheitAsync(IAsyncEnumerable<double> source)
{
    await foreach (var celsius in source)
    {
        yield return celsius * 9.0 / 5.0 + 32.0;
    }
}

// 组合管道
var raw = ReadTemperaturesAsync(new[] { -5.0, 10.0, 22.5 });
var warm = AboveFreezingAsync(raw);
var fahrenheit = ToFahrenheitAsync(warm);

await foreach (var f in fahrenheit)
    Console.WriteLine(f); // 输出 50, 72.5
```

请注意每个方法是如何接收 `IAsyncEnumerable<T>` 并返回 `IAsyncEnumerable<T>` 的，这使得链式调用变得非常清晰简洁。
整个管道是**惰性**的：直到最终的 `await foreach` 拉取元素时，任何操作才会真正执行。

### 核心概念

| 概念 | 描述 |
| --- | --- |
| `async IAsyncEnumerable<T>` | 异步迭代器方法的返回类型 |
| `yield return` | 向消费者产出一个元素 |
| `await foreach` | 逐个元素消费异步序列 |
| 管道链式调用 | 将一个方法的输出作为另一个方法的输入 |
| 惰性求值 | 元素按需生成，而非一次性全部生成 |

### 你的任务

编写 `TransformAsync(int[] numbers)`，构建一个**三阶段异步管道**：

1. **源阶段（Source stage）**：一个异步迭代器，产出输入数组中的每个数字
2. **过滤阶段（Filter stage）**：一个异步迭代器，消费源序列并仅产出**正数**（大于零）
3. **映射阶段（Map stage）**：一个异步迭代器，消费过滤后的流并产出每个数字的**平方**

最后，使用 `await foreach` 收集映射阶段的结果，并以 `int[]` 形式返回。

你必须为每个阶段编写独立的异步迭代器方法，不要将所有逻辑合并到一个循环中。

### 方法签名

```csharp
public static async Task<int[]> TransformAsync(int[] numbers)
```

### 预期结果

```scss
TransformAsync([1, -2, 3, -4, 5])    -> [1, 9, 25]
TransformAsync([-1, -2, -3])          -> []
TransformAsync([10])                  -> [100]
TransformAsync([0, 0, 0])             -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int[]> TransformAsync(int[] numbers)
    {
        // 1. 构建异步管道：源 -> 过滤正数 -> 求平方 -> 收集结果
        var source = SourceAsync(numbers);
        var positives = FilterPositiveAsync(source);
        var squares = SquareAsync(positives);

        // 2. 使用 await foreach 收集映射阶段的结果
        var results = new List<int>();
        await foreach (var value in squares)
        {
            results.Add(value);
        }
        return results.ToArray();
    }

    // 源阶段：异步产出源数组中的每个元素
    private static async IAsyncEnumerable<int> SourceAsync(int[] numbers)
    {
        foreach (var number in numbers)
        {
            await Task.Yield(); // 模拟异步 I/O
            yield return number;
        }
    }

    // 过滤阶段：只产出正数
    private static async IAsyncEnumerable<int> FilterPositiveAsync(IAsyncEnumerable<int> source)
    {
        await foreach (var number in source)
        {
            if (number > 0)
                yield return number;
        }
    }

    // 映射阶段：产出每个数字的平方
    private static async IAsyncEnumerable<int> SquareAsync(IAsyncEnumerable<int> source)
    {
        await foreach (var number in source)
        {
            yield return number * number;
        }
    }
}
```
