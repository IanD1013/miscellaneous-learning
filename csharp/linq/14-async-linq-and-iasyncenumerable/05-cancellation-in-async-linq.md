### IAsyncEnumerable<T> 中的取消支持

异步流（`IAsyncEnumerable<T>`）在处理随时间到达的数据序列时非常强大，例如数据库行、API 分页或传感器读数。
但是，如果你只需要前几项数据，或者用户导航离开了页面，该怎么办？
你需要**取消支持**，以便生产者停止进行不必要的工作。

在 C# 中，异步迭代器可以接受一个使用 `[EnumeratorCancellation]` 特性修饰的 `CancellationToken`。
当你在 `await foreach` 循环中使用 `.WithCancellation(token)` 时，此 token 会自动从消费者传递给生产者。

### 工作原理

生产者与消费者之间的协作遵循以下模式：

1. **生产者**（异步迭代器方法）声明一个带有 `[EnumeratorCancellation]` 的 `CancellationToken` 参数
2. **生产者**定期检查该 token：可以通过将其传递给像 `Task.Delay(ms, token)` 这样的可等待调用，或者调用 `token.ThrowIfCancellationRequested()`
3. **消费者**创建一个 `CancellationTokenSource` 来控制该 token
4. **消费者**在异步可枚举对象上使用 `.WithCancellation(cts.Token)` 传递 token
5. 当消费者调用 `cts.Cancel()` 时，生产者会在其下一次检查时收到 `OperationCanceledException`

这是**协作式取消**：生产者必须主动检查 token。
仅仅取消并不会强制停止迭代器。

### 语法

```csharp
// 生产者：支持取消的异步迭代器
public static async IAsyncEnumerable<T> ProduceAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    while (hasMoreData)
    {
        cancellationToken.ThrowIfCancellationRequested();
        var data = await FetchNextAsync(cancellationToken);
        yield return data;
    }
}

// 消费者：传递 token
var cts = new CancellationTokenSource();
await foreach (var item in ProduceAsync().WithCancellation(cts.Token))
{
    // 处理元素，完成后取消
}
```

### 示例

```csharp
// 示例 1：响应取消的温度传感器流
public static async IAsyncEnumerable<double> ReadTemperaturesAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    while (!ct.IsCancellationRequested)
    {
        double temp = await ReadSensorAsync(ct);
        yield return temp;
    }
}

// 消费者在 10 秒后取消
var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
await foreach (var temp in ReadTemperaturesAsync().WithCancellation(cts.Token))
{
    Console.WriteLine($"Temperature: {temp}°C");
}
```

```csharp
// 示例 2：将 token 传递给 Task.Delay 会导致 OperationCanceledException
public static async IAsyncEnumerable<string> PollMessagesAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    int page = 0;
    while (true)
    {
        // 当 ct 被取消时，这里会抛出 OperationCanceledException
        await Task.Delay(500, ct);
        yield return $"Message batch {++page}";
    }
}

// 消费者用 try/catch 包裹以实现优雅停止
var cts = new CancellationTokenSource();
try
{
    await foreach (var msg in PollMessagesAsync().WithCancellation(cts.Token))
    {
        Process(msg);
        if (shouldStop) cts.Cancel();
    }
}
catch (OperationCanceledException) { /* 优雅退出 */ }
```

### 核心概念

| 概念 | 描述 |
| --- | --- |
| `[EnumeratorCancellation]` | 异步迭代器中 `CancellationToken` 参数上的特性 |
| `.WithCancellation(token)` | 向异步枚举器传递 token 的扩展方法 |
| `ThrowIfCancellationRequested()` | 如果 token 已被取消，则抛出 `OperationCanceledException` |
| `CancellationTokenSource` | 创建并控制一个 `CancellationToken` |
| `cts.Cancel()` | 向所有观察该 token 的代码发出取消信号 |
| `OperationCanceledException` | 观察到已取消的 token 时抛出 |

### 你的任务

编写两个方法：

1. **`GenerateNumbersAsync(int count, CancellationToken)`** - 一个异步迭代器，生成从 `1` 到 `count` 的整数。
   它必须在每次迭代时检查取消 token 来响应取消（可以通过 `ThrowIfCancellationRequested()`，也可以将 token 传递给类似 `Task.Delay` 的可等待调用）。
2. **`TakeWithCancellation(int count, int limit)`** - 创建一个 `CancellationTokenSource`，使用 `WithCancellation` 遍历 `GenerateNumbersAsync(count)`，将项收集到一个列表中，并在**正好收集到 `limit` 项后取消 token**（如果序列比 `limit` 短，则收集更少的项）。
   将收集到的项作为 `int[]` 返回。

该方法必须妥善处理 `OperationCanceledException`：它不应该传播给调用者。

### 方法签名

```csharp
public static async Task<int[]> TakeWithCancellation(int count, int limit)
public static async IAsyncEnumerable<int> GenerateNumbersAsync(
    int count,
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
```

### 预期结果

```scss
TakeWithCancellation(10, 3)  -> [1, 2, 3]
TakeWithCancellation(5, 5)   -> [1, 2, 3, 4, 5]
TakeWithCancellation(3, 10)  -> [1, 2, 3]
TakeWithCancellation(100, 1) -> [1]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int[]> TakeWithCancellation(int count, int limit)
    {
        // limit 为 0 或负数时无需收集任何项
        if (limit <= 0)
            return Array.Empty<int>();

        // 1. 创建 CancellationTokenSource
        using var cts = new CancellationTokenSource();
        var results = new List<int>();

        try
        {
            // 2. 使用 await foreach 和 WithCancellation 从 GenerateNumbersAsync 收集项
            await foreach (var number in GenerateNumbersAsync(count).WithCancellation(cts.Token))
            {
                results.Add(number);

                // 3. 正好收集到 limit 项后取消 token
                if (results.Count == limit)
                    cts.Cancel();
            }
        }
        catch (OperationCanceledException)
        {
            // 取消是预期行为，不向调用者传播
        }

        // 4. 以 int[] 形式返回收集到的项
        return results.ToArray();
    }

    public static async IAsyncEnumerable<int> GenerateNumbersAsync(
        int count,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        // 产出 1 到 count 的整数
        for (int i = 1; i <= count; i++)
        {
            // 每次迭代都检查取消 token
            cancellationToken.ThrowIfCancellationRequested();
            await Task.Yield(); // 模拟异步操作
            yield return i;
        }
    }
}
```
