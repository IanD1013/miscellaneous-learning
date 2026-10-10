### 处理 HTTP 错误

HTTP 请求可能会由于多种原因失败：网络问题、服务器错误或无效的 URL。
妥善的错误处理可确保你的应用程序在出现问题时保持稳定。

### HttpRequestException

当 HTTP 请求在网络层发生失败（连接被拒绝、DNS 失败、超时）时，会抛出 `HttpRequestException`。

```csharp
try
{
    var response = await client.GetAsync(url);
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"Request failed: {ex.Message}");
}
```

### 检查状态码

并非所有已完成的请求都是成功的。
服务器可能会返回 404（Not Found）或 500（Server Error）。
使用 `IsSuccessStatusCode` 来检查是否为 2xx 响应。

```csharp
var response = await client.GetAsync(url);

if (response.IsSuccessStatusCode)
{
    // 状态码在 200-299 之间
    var content = await response.Content.ReadAsStringAsync();
}
else
{
    // 处理错误状态码（4xx、5xx）
    Console.WriteLine($"Error: {response.StatusCode}");
}
```

### 结合两种方法

```csharp
try
{
    var response = await client.GetAsync(url);
    
    if (response.IsSuccessStatusCode)
    {
        return await response.Content.ReadAsStringAsync();
    }
    return "Server returned an error";
}
catch (HttpRequestException)
{
    return "Network error occurred";
}
```

### 你的任务

创建一个方法，从 URL 安全地获取数据并处理所有错误情况。

### 方法签名

```csharp
public static async Task<string> SafeFetch(string url)
```

### 预期行为

- 如果请求完成且状态码为 2xx，则返回 `"Success"`
- 如果服务器返回非 2xx 状态码（4xx、5xx），则返回 `"Failed"`
- 如果发生 `HttpRequestException`，则返回 `"Failed"`

### 预期结果

```
SafeFetch("https://api.example.com/data") -> "Success" (when server returns 200)
SafeFetch("https://api.example.com/missing") -> "Failed" (when server returns 404)
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> SafeFetch(string url)
    {
        try
        {
            // 向 URL 发送 GET 请求
            using var client = new HttpClient();
            var response = await client.GetAsync(url);

            // 2xx 状态码返回 "Success"，否则返回 "Failed"
            if (response.IsSuccessStatusCode)
            {
                return "Success";
            }
            return "Failed";
        }
        catch (HttpRequestException)
        {
            // 网络层失败同样返回 "Failed"
            return "Failed";
        }
    }
}
```
