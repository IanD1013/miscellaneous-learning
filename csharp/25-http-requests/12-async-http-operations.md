### 异步 HTTP 操作

HttpClient 方法本质上是异步的，会返回表示正在进行的操作的 `Task` 对象。
正确使用 `async/await` 可以确保您的应用程序在等待 HTTP 响应时保持响应能力。

### 顺序请求 vs 并发请求

**顺序**（较慢 - 每个请求都会等待前一个请求完成）：

```csharp
var result1 = await client.GetStringAsync(url1);
var result2 = await client.GetStringAsync(url2);
var result3 = await client.GetStringAsync(url3);
```

**并发**（更快 - 所有请求同时运行）：

```csharp
var task1 = client.GetStringAsync(url1);
var task2 = client.GetStringAsync(url2);
var task3 = client.GetStringAsync(url3);

var results = await Task.WhenAll(task1, task2, task3);
```

### Task.WhenAll

`Task.WhenAll` 接收多个任务，并返回一个在所有输入任务完成时结束的单一任务。
它会保留结果的顺序，与输入任务的顺序相匹配。

```csharp
// 使用 LINQ 从集合创建任务
var tasks = urls.Select(url => client.GetStringAsync(url));
string[] results = await Task.WhenAll(tasks);
```

### 关键点

| 概念 | 描述 |
| --- | --- |
| `async` | 将方法标记为异步 |
| `await` | 暂停执行直到任务完成 |
| `Task<T>` | 表示返回类型为 T 的异步操作 |
| `Task.WhenAll` | 并发等待多个任务 |

### 你的任务

创建一个使用 `Task.WhenAll` **并发**从多个 URL 获取内容的方法。
返回一个字符串响应数组，其顺序与输入的 URL 顺序相同。

### 方法签名

```csharp
public static async Task<string[]> FetchAllConcurrently(string[] urls)
```

### 预期结果

```
FetchAllConcurrently(["https://api.example.com/a", "https://api.example.com/b"]) -> ["Response A", "Response B"]
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Linq;

public class Solution
{
    public static async Task<string[]> FetchAllConcurrently(string[] urls)
    {
        // 所有请求共用同一个 HttpClient
        using var client = new HttpClient();

        // 为每个 URL 启动一个请求任务（此时尚未 await，请求并发进行）
        var tasks = urls.Select(url => client.GetStringAsync(url));

        // 使用 Task.WhenAll 等待全部完成，结果顺序与输入 URL 顺序一致
        return await Task.WhenAll(tasks);
    }
}
```
