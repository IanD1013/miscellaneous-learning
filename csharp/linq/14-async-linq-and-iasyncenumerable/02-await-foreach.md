### 使用 `await foreach` 消费 `IAsyncEnumerable<T>`

在现代 C# 中，数据通常是异步到达的：来自数据库游标、分页 API 或流式 gRPC 连接。
`IAsyncEnumerable<T>` 允许你逐个异步地生成和消费元素，而不是一次性将所有内容加载到内存中。
`await foreach` 语句用于遍历这些异步流，在进入下一个元素之前等待当前元素完成。

### 工作原理

常规的 `foreach` 循环在枚举器上同步调用 `MoveNext()`。
而使用 `await foreach` 时，运行时改为调用 `MoveNextAsync()`，它返回一个 `ValueTask<bool>`。
这意味着迭代的每一步都可以暂停以等待下一个元素，而不会阻塞线程。
只有当等待的元素就绪时，循环才会继续前进。

在生产者端，**异步迭代器方法**返回 `IAsyncEnumerable<T>`，并结合使用 `yield return` 和 `await` 表达式。
每次消费者请求下一个元素时，迭代器都会从上次产出的位置继续执行。

### 语法

```csharp
// 生产异步流（异步迭代器）
async IAsyncEnumerable<T> ProduceItemsAsync()
{
    // 可以在迭代器内部 await 异步操作
    await SomeAsyncWork();
    yield return item;
}

// 消费异步流
await foreach (var item in ProduceItemsAsync())
{
    // 在每个元素到达时进行处理
}
```

### 示例

下面是一个模拟从传感器获取温度读数的异步迭代器：

```csharp
async IAsyncEnumerable<double> ReadTemperaturesAsync(int readingCount)
{
    for (int i = 0; i < readingCount; i++)
    {
        await Task.Delay(100); // 模拟传感器延迟
        yield return 20.0 + i * 0.5;
    }
}
```

消费该流以查找最高温度：

```csharp
public static async Task<double> GetMaxTemperatureAsync(int readings)
{
    double max = double.MinValue;
    await foreach (var temp in ReadTemperaturesAsync(readings))
    {
        if (temp > max) max = temp;
    }
    return max;
}
```

另一个示例：从“流”中生成单词并将它们拼接起来：

```csharp
async IAsyncEnumerable<string> StreamWordsAsync(string[] words)
{
    foreach (var word in words)
    {
        await Task.Yield(); // 模拟异步操作
        yield return word;
    }
}

public static async Task<string> JoinWordsAsync(string[] words)
{
    var result = "";
    await foreach (var word in StreamWordsAsync(words))
    {
        result += (result.Length > 0 ? " " : "") + word;
    }
    return result;
}
```

### 要点

- 异步迭代器方法必须返回 `IAsyncEnumerable<T>`（而不是 `Task<IAsyncEnumerable<T>>`）
- 在迭代器内部，你必须至少包含一个 `await` 表达式，即使是 `await Task.Yield()` 也足够了
- `yield return` 关键字逐个产出每个元素
- 消费者使用 `await foreach`（而不是常规的 `foreach`）来进行遍历

### 你的任务

编写一个名为 `SumAsync` 的 `async Task<int>` 方法，该方法接收一个 `int count` 参数并完成以下操作：

1. 使用一个单独的异步迭代器方法，创建一个异步序列，产出从 `1` 到 `count`（包含）的整数
2. 使用 `await foreach` 消费该序列，累加计算总和
3. 返回总和

如果 `count` 为 `0` 或负数，该序列不应产出任何元素，且方法应返回 `0`。

### 方法签名

```csharp
public static async Task<int> SumAsync(int count)
```

### 预期结果

```scss
SumAsync(5)   -> 15    // 1+2+3+4+5
SumAsync(1)   -> 1
SumAsync(10)  -> 55    // 1+2+...+10
SumAsync(0)   -> 0
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> SumAsync(int count)
    {
        // 使用 await foreach 消费异步序列并累加总和
        int sum = 0;
        await foreach (var number in GenerateNumbersAsync(count))
        {
            sum += number;
        }
        return sum;
    }

    // 私有异步迭代器方法：产出 1 到 count 的整数
    // count 为 0 或负数时不产出任何元素
    private static async IAsyncEnumerable<int> GenerateNumbersAsync(int count)
    {
        for (int i = 1; i <= count; i++)
        {
            await Task.Yield(); // 模拟异步操作
            yield return i;
        }
    }
}
```
