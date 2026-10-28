### 使用 HttpClient 发送 GET 请求

最常见的 HTTP 操作是 GET 请求，用于从服务器检索数据。
HttpClient 提供了几种方法，使 GET 请求变得简单而高效。

### GetStringAsync 方法

```csharp
using var client = new HttpClient();

// 以字符串形式获取响应体
string content = await client.GetStringAsync("https://api.example.com/data");
```

### 为什么使用 GetStringAsync？

`GetStringAsync` 是从 URL 获取文本内容最简单的方法。
它：

- 向指定的 URL 发送 GET 请求
- 等待响应
- 将响应体作为字符串返回
- 如果请求失败，则抛出异常

### using 语句

```csharp
// 确保 HttpClient 在使用后被正确释放
using var client = new HttpClient();

// 或者使用显式作用域
using (var client = new HttpClient())
{
    string result = await client.GetStringAsync(url);
}
```

### Async/Await 模式

HTTP 请求是异步操作。
`await` 关键字会暂停执行，直到请求完成：

```csharp
// 方法必须标记为 async 才能使用 await
public static async Task<string> FetchData(string url)
{
    using var client = new HttpClient();
    return await client.GetStringAsync(url);
}
```

### 你的任务

创建一个方法，使用 `GetStringAsync` 从给定的 URL 获取文本内容，并将其作为字符串返回。

### 方法签名

```csharp
public static async Task<string> FetchContent(string url)
```

### 预期结果

```
FetchContent("https://api.example.com/hello") -> "Hello, World!"
FetchContent("https://api.example.com/greeting") -> "Welcome to the API"
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> FetchContent(string url)
    {
        // 使用 HttpClient 从 URL 获取内容
        using var client = new HttpClient();

        // 将内容作为字符串返回
        return await client.GetStringAsync(url);
    }
}
```
