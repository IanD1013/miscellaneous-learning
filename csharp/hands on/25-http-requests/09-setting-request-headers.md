### HTTP 请求头（HTTP Request Headers）

HTTP 请求头在请求和响应中提供附加信息。
它们用于身份验证、内容协商、缓存等。

### DefaultRequestHeaders

`HttpClient.DefaultRequestHeaders` 是一个集合，会将请求头应用到该客户端实例发出的每一个请求。

```csharp
var client = new HttpClient();

// 添加单个请求头
client.DefaultRequestHeaders.Add("X-Custom-Header", "value");

// 该客户端发出的每个请求都会带上这些请求头
var response = await client.GetStringAsync("https://api.example.com/data");
```

### 常见请求头

| 请求头 | 用途 | 示例 |
| --- | --- | --- |
| Authorization | 身份验证凭据 | `Bearer abc123` |
| Accept | 期望的响应格式 | `application/json` |
| Content-Type | 请求体格式 | `application/json` |
| User-Agent | 客户端标识 | `MyApp/1.0` |

### Authorization 请求头

Authorization 请求头用于发送凭据以向 API 进行身份验证。
Bearer token 是最常见的格式。

```csharp
// Bearer token 身份验证
client.DefaultRequestHeaders.Add("Authorization", "Bearer my-token-here");

// 或者使用字符串插值
string token = "abc123";
client.DefaultRequestHeaders.Add("Authorization", $"Bearer {token}");
```

### Accept 请求头

Accept 请求头告知服务器客户端能够处理的内容类型。

```csharp
// 请求 JSON 响应
client.DefaultRequestHeaders.Add("Accept", "application/json");

// 请求 XML 响应
client.DefaultRequestHeaders.Add("Accept", "application/xml");

// 请求纯文本
client.DefaultRequestHeaders.Add("Accept", "text/plain");
```

### 你的任务

创建一个方法，执行以下操作：

1. 创建一个 HttpClient
2. 添加格式为 `Bearer {authToken}` 的 Authorization 请求头
3. 添加包含所提供 acceptType 的 Accept 请求头
4. 向 URL 发送 GET 请求并返回响应内容

### 方法签名

```csharp
public static async Task<string> FetchWithHeaders(string url, string authToken, string acceptType)
```

### 预期结果

```
FetchWithHeaders("https://api.example.com/data", "token123", "application/json") -> "JSON response data"
FetchWithHeaders("https://api.example.com/text", "secret-key", "text/plain") -> "Plain text response"
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> FetchWithHeaders(string url, string authToken, string acceptType)
    {
        // 创建 HttpClient
        using var client = new HttpClient();

        // 设置 Authorization 和 Accept 请求头
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {authToken}");
        client.DefaultRequestHeaders.Add("Accept", acceptType);

        // 发送 GET 请求并返回响应内容
        return await client.GetStringAsync(url);
    }
}
```
