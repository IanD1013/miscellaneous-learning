### Task.WhenAny

`Task.WhenAny` 会在提供的任务中**任意一个**完成时立即返回，而不是像 `Task.WhenAll` 那样等待所有任务完成。

### 基本用法

```csharp
Task<int> task1 = GetValueAsync(100);  // 耗时 100ms
Task<int> task2 = GetValueAsync(50);   // 耗时 50ms
Task<int> task3 = GetValueAsync(200);  // 耗时 200ms

// 返回最先完成的任务（task2）
Task<int> winner = await Task.WhenAny(task1, task2, task3);
int result = await winner;  // 获取实际结果
```

### WhenAny 与 WhenAll 的对比

| 方法 | 返回时机 | 返回类型 |
| --- | --- | --- |
| `Task.WhenAll` | 所有任务完成 | `Task<T[]>` |
| `Task.WhenAny` | 第一个任务完成 | `Task<Task<T>>` |

### 重要：双重 await 模式

```csharp
// WhenAny 返回的是 Task<Task<T>>，而不是 Task<T>
Task<string> firstTask = await Task.WhenAny(tasks);  // 获取胜出的任务
string result = await firstTask;                      // 获取实际的值
```

### 常见使用场景

- 竞速多个数据源（使用最快的响应）
- 实现超时机制
- 先响应者胜出（First-response-wins）的场景

### 你的任务

创建三个异步任务，每个任务在指定的延迟后返回一条消息。
使用 `Task.WhenAny` 返回最先完成的任务的消息。

你需要一个辅助方法来创建延迟任务：

```csharp
private static async Task<string> DelayedMessageAsync(string message, int delayMs)
{
    await Task.Delay(delayMs);
    return message;
}
```

### 方法签名

```csharp
public static async Task<string> FirstToCompleteAsync(string message1, int delay1, string message2, int delay2, string message3, int delay3)
```

### 预期结果

```
FirstToCompleteAsync("A", 100, "B", 50, "C", 200) -> "B"  // B 的延迟最短
FirstToCompleteAsync("Fast", 10, "Slow", 500, "Medium", 200) -> "Fast"
```

### 解答

```csharp
using System;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> FirstToCompleteAsync(string message1, int delay1, string message2, int delay2, string message3, int delay3)
    {
        // 同时启动三个延迟任务
        Task<string> task1 = DelayedMessageAsync(message1, delay1);
        Task<string> task2 = DelayedMessageAsync(message2, delay2);
        Task<string> task3 = DelayedMessageAsync(message3, delay3);

        // 获取最先完成的任务
        Task<string> winner = await Task.WhenAny(task1, task2, task3);

        // 获取该任务的实际值
        return await winner;
    }

    // 在指定延迟后返回消息的辅助方法
    private static async Task<string> DelayedMessageAsync(string message, int delayMs)
    {
        await Task.Delay(delayMs);
        return message;
    }
}
```
