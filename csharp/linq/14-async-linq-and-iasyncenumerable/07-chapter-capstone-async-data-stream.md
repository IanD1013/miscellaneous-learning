### 异步迭代器与 `await foreach`

在实际应用中，数据通常是增量到达的：来自数据库游标、分页 API、传感器数据流或消息队列。
C# 提供了**异步迭代器**（`IAsyncEnumerable<T>`）和 `await foreach`，以便逐个元素处理此类数据流，而无需将所有内容缓冲到内存中。
这种模式将 `yield return` 的惰性求值与 `async`/`await` 的非阻塞特性结合在一起。

### 异步迭代器的工作原理

**异步迭代器**是满足以下条件的方法：

1. 返回 `IAsyncEnumerable<T>`
2. 使用 `yield return` 一次产出一个值
3. 可以在 yield 之间包含 `await` 表达式（模拟异步数据到达）

消费者使用 `await foreach` 从流中拉取值。
每次迭代都会等待下一个元素，从而使整个流水线保持异步且非阻塞。

### 语法

```csharp
// 生产异步流
private static async IAsyncEnumerable<T> ProduceAsync(/* 参数 */)
{
    foreach (var item in source)
    {
        await Task.Yield(); // 或任何真实的异步操作
        yield return item;
    }
}

// 消费异步流
await foreach (var item in ProduceAsync(/* 实参 */))
{
    // 在每个元素到达时进行处理
}
```

### 示例

```csharp
// 示例 1：温度读数的异步流
private static async IAsyncEnumerable<double> ReadTemperaturesAsync(double[] sensors)
{
    foreach (var temp in sensors)
    {
        await Task.Delay(10);
        yield return temp;
    }
}

// 消费并找出最高温度
double max = double.MinValue;
await foreach (var temp in ReadTemperaturesAsync(new[] { 72.1, 68.5, 80.3 }))
{
    if (temp > max) max = temp;
}
// max 为 80.3

// 示例 2：从异步流中过滤并收集
private static async IAsyncEnumerable<string> StreamWordsAsync(string[] words)
{
    foreach (var word in words)
    {
        await Task.Yield();
        yield return word;
    }
}

var longWords = new List<string>();
await foreach (var word in StreamWordsAsync(new[] { "hi", "async", "go", "iterator" }))
{
    if (word.Length > 3)
        longWords.Add(word);
}
// longWords 包含 ["async", "iterator"]

// 示例 3：在消费过程中进行聚合
int total = 0;
int items = 0;
await foreach (var score in StreamScoresAsync(scores))
{
    if (score >= passingGrade)
    {
        total += score;
        items++;
    }
}
```

### 关键细节

| 概念 | 描述 |
| --- | --- |
| `IAsyncEnumerable<T>` | 异步迭代器方法的返回类型 |
| `yield return` | 向消费者产出单个值 |
| `await Task.Yield()` | 模拟异步操作；确保该方法是真正异步的 |
| `await foreach` | 迭代 `IAsyncEnumerable<T>`，等待每个元素 |
| 消费时过滤 | 在 `await foreach` 内部应用条件以选择性地处理元素 |
| 消费时聚合 | 随着元素到达累加当前总和、计数或其他指标 |

### 你的任务

编写一个方法 `ProcessStreamAsync`，接收一个整数数组并执行以下操作：

1. **生产**：创建一个私有异步迭代器方法，将数组中的每个整数作为 `IAsyncEnumerable<int>` 产出。
   在每次 yield 之间使用 `await Task.Yield()` 模拟异步传递。
2. **消费与过滤**：使用 `await foreach` 遍历异步流。
   对于每个元素，检查它是否为**严格正数**（大于零）。
3. **聚合**：跟踪遇到的所有正数的**数量**（count）和**总和**（sum）。
4. **返回**：返回格式完全为 `"Count: N, Sum: N"` 的格式化字符串，其中第一个 N 是计数，第二个 N 是总和。

零**不**算作正数。
负数应完全跳过。

### 方法签名

```csharp
public static async Task<string> ProcessStreamAsync(int[] numbers)
```

你还需要一个私有辅助方法：

```csharp
private static async IAsyncEnumerable<int> GenerateAsync(int[] numbers)
```

### 预期结果

```rust
ProcessStreamAsync([1, -2, 3, -4, 5])    -> "Count: 3, Sum: 9"
ProcessStreamAsync([10, 20, 30])          -> "Count: 3, Sum: 60"
ProcessStreamAsync([-1, -2, -3])          -> "Count: 0, Sum: 0"
ProcessStreamAsync([])                    -> "Count: 0, Sum: 0"
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> ProcessStreamAsync(int[] numbers)
    {
        int count = 0;
        int sum = 0;

        // 消费异步流，只对严格正数进行计数和求和
        await foreach (var number in GenerateAsync(numbers))
        {
            if (number > 0)
            {
                count++;
                sum += number;
            }
        }

        return $"Count: {count}, Sum: {sum}";
    }

    // 私有异步迭代器：逐个产出数组中的整数
    private static async IAsyncEnumerable<int> GenerateAsync(int[] numbers)
    {
        foreach (var number in numbers)
        {
            await Task.Yield(); // 模拟异步传递
            yield return number;
        }
    }
}
```
