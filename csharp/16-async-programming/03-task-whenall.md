### Task.WhenAll

`Task.WhenAll` 允许你并行运行多个异步操作并等待它们全部完成。
这比按顺序逐个 await 每个任务要快得多。

### 顺序执行与并行执行

```csharp
// 顺序执行 - 每个任务都要等待前一个任务（慢）
var result1 = await GetDataAsync(1);
var result2 = await GetDataAsync(2);
var result3 = await GetDataAsync(3);
// 总耗时：delay1 + delay2 + delay3

// 并行执行 - 所有任务同时运行（快）
var task1 = GetDataAsync(1);
var task2 = GetDataAsync(2);
var task3 = GetDataAsync(3);
var results = await Task.WhenAll(task1, task2, task3);
// 总耗时：max(delay1, delay2, delay3)
```

### 使用 Task.WhenAll

```csharp
// 返回相同类型的任务：WhenAll 会给你一个结果数组，
// 顺序与你传入的任务相同
Task<string> nameTask = FetchNameAsync();
Task<string> cityTask = FetchCityAsync();

string[] results = await Task.WhenAll(nameTask, cityTask);
string name = results[0];
string city = results[1];

// 返回不同类型的任务：一起 await 它们，然后分别读取每个结果
Task<string> countryTask = FetchCountryAsync();
Task<int> ageTask = FetchAgeAsync();

await Task.WhenAll(countryTask, ageTask);
string country = countryTask.Result;  // 在 WhenAll 之后访问是安全的
int age = ageTask.Result;
```

### 要点

| 方面 | 描述 |
| --- | --- |
| 返回类型 | `Task<T[]>` - 结果数组，顺序与传入的任务相同 |
| 执行 | 所有任务并发运行 |
| 完成 | 等待所有任务完成 |
| 异常 | 如果任何任务失败，则抛出 `AggregateException` |

### 你的任务

实现 `SumOfThreeDelaysAsync`，使用 `Task.WhenAll` 并行运行三个异步操作。
每个操作都使用提供的 `ProcessValueAsync` 辅助方法，该方法会在延迟后将值翻倍。

1. 使用每组 value/delay 参数对启动对 `ProcessValueAsync` 的三次调用
2. 使用 `Task.WhenAll` 同时等待所有三个任务完成
3. 返回所有三个结果的总和

### 方法签名

```csharp
public static async Task<int> SumOfThreeDelaysAsync(int value1, int delay1, int value2, int delay2, int value3, int delay3)
```

### 预期结果

```
SumOfThreeDelaysAsync(5, 10, 10, 10, 15, 10) -> 60  // (5*2) + (10*2) + (15*2)
SumOfThreeDelaysAsync(1, 10, 2, 10, 3, 10) -> 12   // (1*2) + (2*2) + (3*2)
```

### 解答

```csharp
using System;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> SumOfThreeDelaysAsync(int value1, int delay1, int value2, int delay2, int value3, int delay3)
    {
        // 同时启动三个任务
        Task<int> task1 = ProcessValueAsync(value1, delay1);
        Task<int> task2 = ProcessValueAsync(value2, delay2);
        Task<int> task3 = ProcessValueAsync(value3, delay3);

        // 等待所有任务完成，结果顺序与传入的任务相同
        int[] results = await Task.WhenAll(task1, task2, task3);

        // 返回三个结果的总和
        return results[0] + results[1] + results[2];
    }
    
    // 模拟异步操作的辅助方法
    private static async Task<int> ProcessValueAsync(int value, int delayMs)
    {
        await Task.Delay(delayMs);
        return value * 2;
    }
}
```
