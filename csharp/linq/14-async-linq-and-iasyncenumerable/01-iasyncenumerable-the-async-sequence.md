### IAsyncEnumerable<T> - C# 中的异步流

在同步 C# 中，`IEnumerable<T>` 允许你使用 `yield return` 延迟生成一系列值。
但如果每个值都需要异步操作（例如数据库读取、HTTP 调用或文件块读取）该怎么办？
你无法在常规迭代器内部使用 `await`。
这就是 `IAsyncEnumerable<T>` 的用武之地：它是 `IEnumerable<T>` 的异步对应项，允许你在 `async` 方法内使用 `yield return` 逐个生成元素。
使用者使用 `await foreach` 代替普通的 `foreach` 进行迭代。

这种模式对于流式传输场景至关重要：从数据库游标中读取行而无需将所有内容加载到内存中、处理来自网络流的行，或者生成每一步都依赖于 I/O 的值。

### 工作原理

一个**异步迭代器方法**具有三个显著特征：

1. 它的返回类型是 `IAsyncEnumerable<T>`（或 `IAsyncEnumerator<T>`）
2. 它使用 `yield return` 来生成值
3. 它可以使用 `await` 表达式在 yield 之间执行异步操作

在消费端，`await foreach` 一次拉取一个元素，并在底层等待每个 `MoveNextAsync()` 调用。
这意味着消费者和生产者是松耦合的：生产者以自己的节奏生成值，而消费者在值到达时进行处理。

### 语法

```csharp
// 生产端：异步迭代器方法
private static async IAsyncEnumerable<T> ProduceAsync(/* 参数 */)
{
    // 执行异步操作
    await SomeAsyncOperation();
    yield return value;
    // 可以多次 yield，也可以在循环中 yield 等
}

// 消费端：await foreach
await foreach (var item in ProduceAsync(/* 实参 */))
{
    // 在每个元素可用时进行处理
}
```

### 示例

```csharp
// 示例 1：使用模拟的异步延迟流式读取温度读数
private static async IAsyncEnumerable<double> ReadTemperaturesAsync(int sensorCount)
{
    for (int i = 0; i < sensorCount; i++)
    {
        await Task.Delay(100); // 模拟 I/O 延迟
        yield return 20.0 + i * 0.5;
    }
}

// 消费它：
var temps = new List<double>();
await foreach (var temp in ReadTemperaturesAsync(3))
{
    temps.Add(temp);
}
// temps => [20.0, 20.5, 21.0]

// 示例 2：异步生成分页 URL
private static async IAsyncEnumerable<string> FetchPageUrlsAsync(string baseUrl, int pages)
{
    for (int page = 1; page <= pages; page++)
    {
        await Task.Yield(); // 将控制权交还给调度程序
        yield return $"{baseUrl}?page={page}";
    }
}

// 消费它：
await foreach (var url in FetchPageUrlsAsync("https://example.com/items", 2))
{
    Console.WriteLine(url);
}
// 输出：
// https://example.com/items?page=1
// https://example.com/items?page=2
```

### 关键要点

| 概念 | 同步 | 异步 |
| --- | --- | --- |
| 序列类型 | `IEnumerable<T>` | `IAsyncEnumerable<T>` |
| 迭代 | `foreach` | `await foreach` |
| 方法中的 Yield | `yield return` | `yield return`（配合 `async`） |
| 内部使用 await | ❌ 不允许 | ✅ 允许 |
| 返回类型修饰符 | 无 | `async` |

**重要提示：** 异步迭代器方法必须返回 `IAsyncEnumerable<T>`。
即使你在签名中使用了 `async`，也**不要**返回 `Task<IAsyncEnumerable<T>>`，编译器对此有特殊处理。

你可以使用 `await Task.Yield()` 或 `await Task.Delay(...)` 在每次 yield 之间模拟或执行异步操作。
`Task.Yield()` 是最轻量的选项：它只是将控制权交还给调度程序并立即返回。

### 你的任务

编写一个方法 `CollectAsync(int count)`，该方法：

1. 调用一个你定义的**私有异步迭代器方法**，该方法生成从 `1` 到 `count`（包含）的整数，并在每次 yield 之前执行一些异步操作（如 `await Task.Yield()`）
2. 使用 `await foreach` 消费该异步流，收集所有值
3. 将收集到的值作为 `int[]` 返回

如果 `count` 为 `0` 或负数，该方法应返回一个空数组。

### 方法签名

```csharp
public static async Task<int[]> CollectAsync(int count)
```

你还需要定义一个私有异步迭代器方法，其签名类似于：

```csharp
private static async IAsyncEnumerable<int> YourIteratorMethod(int count)
```

### 预期结果

```scss
CollectAsync(5)  -> [1, 2, 3, 4, 5]
CollectAsync(1)  -> [1]
CollectAsync(0)  -> []
CollectAsync(10) -> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int[]> CollectAsync(int count)
    {
        // 使用 await foreach 消费异步迭代器，并把结果收集到列表中
        var results = new List<int>();
        await foreach (var number in GenerateNumbersAsync(count))
        {
            results.Add(number);
        }
        return results.ToArray();
    }

    // 私有异步迭代器方法：异步生成 1 到 count 的整数
    // count 为 0 或负数时循环不执行，不产出任何元素
    private static async IAsyncEnumerable<int> GenerateNumbersAsync(int count)
    {
        for (int i = 1; i <= count; i++)
        {
            await Task.Yield(); // 每次 yield 之前执行一次异步操作
            yield return i;
        }
    }
}
```
