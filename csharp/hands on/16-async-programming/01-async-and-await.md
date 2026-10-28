### Async 和 Await

`async` 和 `await` 关键字允许你编写看起来和行为类似于同步代码的异步代码，使其更易于阅读和维护，同时保持应用程序的响应能力。

### 为什么使用 Async/Await？

如果没有异步编程，当你的代码等待缓慢的操作（例如读取文件、调用 API 或等待计时器）时，整个线程都会被阻塞。
这意味着：

- 在 UI 应用程序中，界面会冻结
- 在 Web 服务器中，能够处理的请求数量会减少
- 资源在无所事事时被浪费

Async/await 通过允许线程在等待期间执行其他工作来解决这个问题：

```csharp
// 同步 - 线程被阻塞 2 秒
Thread.Sleep(2000);
Console.WriteLine("Done");

// 异步 - 线程可以空出来做其他工作
await Task.Delay(2000);
Console.WriteLine("Done");
```

### async 关键字

使用 `async` 标记方法以允许在其内部使用 `await`：

```csharp
public static async Task DoWorkAsync()
{
    await Task.Delay(1000);
    Console.WriteLine("Work complete!");
}
```

### await 关键字

在任何 `Task` 之前使用 `await` 可以暂停执行，直到该任务完成：

```csharp
await Task.Delay(500);  // 等待 500ms 而不阻塞
string data = await FetchDataAsync();  // 等待数据
```

### Task 与 Task<T>

| 返回类型 | 使用场景 | 示例 |
| --- | --- | --- |
| `Task` | 无返回值的方法 | `async Task SaveAsync()` |
| `Task<T>` | 有返回值的方法 | `async Task<int> CalculateAsync()` |

### 常见的异步操作

```csharp
// 不阻塞地延迟
await Task.Delay(1000);

// 从异步方法返回一个值
public static async Task<string> GetMessageAsync()
{
    await Task.Delay(100);
    return "Hello!";
}
```

### 你的任务

从头创建一个异步方法，要求：

1. 命名为 `DelayedGreetingAsync`
2. 接收 `name` (string) 和 `delayMs` (int) 作为参数
3. 返回 `Task<string>`
4. `await` 一个指定毫秒数的 `Task.Delay`
5. 返回格式为 `"Hello, {name}!"` 的问候语

### 需要创建的方法签名

```csharp
public static async Task<string> DelayedGreetingAsync(string name, int delayMs)
```

### 预期结果

```
DelayedGreetingAsync("Alice", 100) -> "Hello, Alice!"
DelayedGreetingAsync("Bob", 50) -> "Hello, Bob!"
```

### 解答

```csharp
using System;
using System.Threading.Tasks;

public class Solution
{
    // 异步方法：等待指定的毫秒数后返回问候语
    public static async Task<string> DelayedGreetingAsync(string name, int delayMs)
    {
        await Task.Delay(delayMs);
        return $"Hello, {name}!";
    }
}
```
