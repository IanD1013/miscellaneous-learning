### HTTP 状态码

HTTP 状态码是三位数字，用于指示 HTTP 请求的结果。
它们可以帮助你了解请求是成功、失败还是需要进一步的操作。

### 常见状态码类别

| 范围 | 类别 | 含义 |
| --- | --- | --- |
| 2xx | 成功 (Success) | 请求成功 |
| 3xx | 重定向 (Redirection) | 需要进一步操作 |
| 4xx | 客户端错误 (Client Error) | 请求存在问题 |
| 5xx | 服务器错误 (Server Error) | 服务器未能满足请求 |

### HttpStatusCode 枚举

.NET 提供了 `HttpStatusCode` 枚举以实现类型安全的状态码比较：

```csharp
using System.Net;

// 常见状态码
HttpStatusCode.OK           // 200 - 成功
HttpStatusCode.Created      // 201 - 资源已创建
HttpStatusCode.BadRequest   // 400 - 无效请求
HttpStatusCode.NotFound     // 404 - 资源未找到
HttpStatusCode.InternalServerError // 500 - 服务器错误
```

### 检查状态码

```csharp
var response = await client.GetAsync(url);

// 使用枚举（推荐）
if (response.StatusCode == HttpStatusCode.OK)
{
    Console.WriteLine("Success!");
}

// 使用整数值
if ((int)response.StatusCode == 200)
{
    Console.WriteLine("Success!");
}

// 使用 IsSuccessStatusCode 判断任意 2xx 响应
if (response.IsSuccessStatusCode)
{
    Console.WriteLine("Some kind of success!");
}
```

### 你的任务

编写一个方法，发送 GET 请求并根据状态码返回一个字符串：

- 如果状态码为 200，返回 `"OK"`
- 如果状态码为 404，返回 `"Not Found"`
- 对于任何其他状态码，返回 `"Error"`

### 方法签名

```csharp
public static async Task<string> CheckStatusCode(string url)
```

### 预期结果

```
CheckStatusCode("https://api.example.com/data") -> "OK" (when server returns 200)
CheckStatusCode("https://api.example.com/missing") -> "Not Found" (when server returns 404)
CheckStatusCode("https://api.example.com/broken") -> "Error" (when server returns 500)
```

### 解答

```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> CheckStatusCode(string url)
    {
        // 发送 GET 请求并检查状态码
        using var client = new HttpClient();
        var response = await client.GetAsync(url);

        // 200 返回 "OK"，404 返回 "Not Found"，其他情况返回 "Error"
        if (response.StatusCode == HttpStatusCode.OK)
        {
            return "OK";
        }
        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return "Not Found";
        }
        return "Error";
    }
}
```
