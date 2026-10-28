### HttpResponseMessage

当你使用 `GetAsync` 而不是 `GetStringAsync` 时，你将接收到一个 `HttpResponseMessage` 对象，它提供了有关 HTTP 响应的详细信息。

### GetAsync 与 GetStringAsync

```csharp
// GetStringAsync - 简单，直接返回内容
string content = await client.GetStringAsync(url);

// GetAsync - 返回包含完整详细信息的 HttpResponseMessage
HttpResponseMessage response = await client.GetAsync(url);
```

### HttpResponseMessage 的关键属性

```csharp
HttpResponseMessage response = await client.GetAsync(url);

// StatusCode - HTTP 状态码（200、404、500 等）
HttpStatusCode status = response.StatusCode;
int statusInt = (int)response.StatusCode; // 转换为 int：200

// IsSuccessStatusCode - 状态码在 200-299 之间时为 true
bool success = response.IsSuccessStatusCode;

// Content - 访问响应体
string body = await response.Content.ReadAsStringAsync();
```

### 常见 HTTP 状态码

| 状态码 | 含义 | IsSuccessStatusCode |
| --- | --- | --- |
| 200 | OK | True |
| 201 | Created | True |
| 204 | No Content | True |
| 400 | Bad Request | False |
| 404 | Not Found | False |
| 500 | Server Error | False |

### 你的任务

实现三个用于处理 `HttpResponseMessage` 的方法：

1. **GetStatusCode** - 发送 GET 请求并将状态码作为整数返回
2. **IsRequestSuccessful** - 发送 GET 请求并返回请求是否成功
3. **ReadResponseContent** - 发送 GET 请求并将响应正文作为字符串返回

### 方法签名

```csharp
public static async Task<int> GetStatusCode(string url)
public static async Task<bool> IsRequestSuccessful(string url)
public static async Task<string> ReadResponseContent(string url)
```

### 预期结果

```
GetStatusCode("https://api.example.com/data") -> 200
IsRequestSuccessful("https://api.example.com/data") -> True
ReadResponseContent("https://api.example.com/hello") -> "Hello, World!"
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> GetStatusCode(string url)
    {
        // 发送 GET 请求，并将状态码作为整数返回
        using var client = new HttpClient();
        HttpResponseMessage response = await client.GetAsync(url);
        return (int)response.StatusCode;
    }

    public static async Task<bool> IsRequestSuccessful(string url)
    {
        // 发送 GET 请求，并返回 IsSuccessStatusCode 是否为 true
        using var client = new HttpClient();
        HttpResponseMessage response = await client.GetAsync(url);
        return response.IsSuccessStatusCode;
    }

    public static async Task<string> ReadResponseContent(string url)
    {
        // 发送 GET 请求，并使用 ReadAsStringAsync 返回内容
        using var client = new HttpClient();
        HttpResponseMessage response = await client.GetAsync(url);
        return await response.Content.ReadAsStringAsync();
    }
}
```
