### 使用 WithCancellation 让 PLINQ 查询可取消

并行 LINQ（PLINQ）可以通过在多个线程之间分配工作来显著加快数据处理速度。
但是，当用户点击“取消”或在海量并行查询仍在处理数据时发生超时，会发生什么呢？
如果没有取消支持，查询仍会继续运行直至完成，从而浪费 CPU 并阻塞应用程序。
`WithCancellation` 方法将 `CancellationToken` 接入 PLINQ 管道，以便可以协作式地停止它。

### 工作原理

.NET 取消模型是协作式的。
由三个部分协同工作：

1. **CancellationTokenSource** - 控制器，可以通过调用 `Cancel()` 发出取消信号。
2. **CancellationToken** - 传递给操作的轻量级结构体。
   它负责携带信号。
3. **WithCancellation(token)** - 一个定期检查令牌的 PLINQ 操作符。
   如果检测到取消信号，它会抛出 `OperationCanceledException`，从而展开并终止并行查询。

关键在于查询本身会在内部调度点检查该令牌。
你不需要在 `Select` 或 `Where` 的 lambda 表达式中手动轮询令牌（尽管对于极其繁重的单元素操作，你可以这样做来获得更快的响应）。

### 语法

```csharp
using var cts = new CancellationTokenSource();
CancellationToken token = cts.Token;

var result = source
    .AsParallel()
    .WithCancellation(token)
    .Where(predicate)
    .Select(transform)
    .ToArray();

// 从另一个线程或在超时后取消：
// cts.Cancel();  - 这会导致查询中抛出 OperationCanceledException
```

### 示例

```csharp
// 示例 1：可取消的并行过滤操作
using var cts = new CancellationTokenSource();
string[] words = { "apple", "avocado", "banana", "blueberry", "cherry" };

string[] aWords = words
    .AsParallel()
    .WithCancellation(cts.Token)
    .Where(w => w.StartsWith("a"))
    .OrderBy(w => w)
    .ToArray();
// 结果：["apple", "avocado"]

// 示例 2：超时后取消
using var cts2 = new CancellationTokenSource(TimeSpan.FromSeconds(5));
try
{
    double[] results = Enumerable.Range(1, 10_000_000)
        .AsParallel()
        .WithCancellation(cts2.Token)
        .Select(n => Math.Sqrt(n))
        .ToArray();
}
catch (OperationCanceledException)
{
    Console.WriteLine("Query was cancelled due to timeout.");
}

// 示例 3：将取消机制接入求和聚合
using var cts3 = new CancellationTokenSource();
int total = new[] { 10, 20, 30, 40 }
    .AsParallel()
    .WithCancellation(cts3.Token)
    .Sum();
// 结果：100（未触发取消）
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `new CancellationTokenSource()` | 创建一个可以手动发出信号的源 |
| `new CancellationTokenSource(TimeSpan)` | 超时后自动取消 |
| `cts.Token` | 获取要传递到管道中的令牌 |
| `.AsParallel().WithCancellation(token)` | 将取消机制链接到 PLINQ 中 |
| `using var cts = ...` | 确保源被正确释放（dispose） |
| `try/catch (OperationCanceledException)` | 优雅地处理取消异常 |

### 你的任务

编写一个方法来演示 PLINQ 的取消接入模式。
给定一个整数数组：

1. 创建一个 `CancellationTokenSource` 并获取其 `CancellationToken`。
2. 构建一个使用带有 `WithCancellation(token)` 的 `AsParallel()` 的 PLINQ 管道。
3. 对数组中的每个元素求平方。
4. 以升序排序的 `int[]` 形式返回这些平方值。

在测试期间不会取消令牌：目标是练习正确的接入模式，以便你的代码具备取消功能支持。

### 方法签名

```csharp
public static int[] CancellableParallel(int[] numbers)
```

### 预期结果

```scss
CancellableParallel([3, 1, 2])    -> [1, 4, 9]
CancellableParallel([5, -3, 0])   -> [0, 9, 25]
CancellableParallel([])           -> []
CancellableParallel([7])          -> [49]
```

### 解答

```csharp
using System;
using System.Linq;
using System.Threading;

public class Solution
{
    public static int[] CancellableParallel(int[] numbers)
    {
        // 创建取消令牌源并获取令牌
        using var cts = new CancellationTokenSource();
        CancellationToken token = cts.Token;

        // 将令牌接入 PLINQ 管道，求平方后按升序排序
        return numbers
            .AsParallel()
            .WithCancellation(token)
            .Select(n => n * n)
            .OrderBy(n => n)
            .ToArray();
    }
}
```
