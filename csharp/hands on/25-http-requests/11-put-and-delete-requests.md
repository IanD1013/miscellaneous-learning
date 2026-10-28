### PUT 和 DELETE 请求

GET 用于检索数据，POST 用于创建新资源，而 PUT 和 DELETE 则通过更新和删除资源来补全 CRUD 操作。

### PUT 请求 - 更新资源

`PutAsync` 发送数据以更新特定 URL 处的现有资源。

```csharp
using var client = new HttpClient();
var content = new StringContent(
    "{\"name\":\"Updated Name\"}",
    Encoding.UTF8,
    "application/json"
);
var response = await client.PutAsync("https://api.example.com/users/1", content);
```

### DELETE 请求 - 删除资源

`DeleteAsync` 删除指定 URL 处的资源。
不需要请求体。

```csharp
using var client = new HttpClient();
var response = await client.DeleteAsync("https://api.example.com/users/1");
```

### 常见状态码

| 状态码 | 含义 | 典型用途 |
| --- | --- | --- |
| 200 | OK | 成功更新/删除 |
| 204 | No Content | 成功删除（无响应体） |
| 404 | Not Found | 资源不存在 |
| 400 | Bad Request | 发送的数据无效 |

### 检查方法类型

使用字符串比较来确定要执行哪个 HTTP 方法：

```csharp
if (method.ToUpper() == "PUT")
{
    // 执行 PUT 请求
}
else if (method.ToUpper() == "DELETE")
{
    // 执行 DELETE 请求
}
```

### 你的任务

实现一个方法，满足以下要求：

1. 接收一个 URL、HTTP 方法（"PUT" 或 "DELETE"）以及可选的 JSON 内容
2. 根据 method 参数执行相应的 HTTP 请求
3. 对于 PUT 请求，将 jsonContent 作为请求体发送
4. 对于 DELETE 请求，不需要请求体
5. 将 HTTP 状态码作为整数返回

### 方法签名

```csharp
public static async Task<int> ExecuteRequest(string url, string method, string jsonContent = null)
```

### 预期结果

```
ExecuteRequest("https://api.example.com/users/1", "PUT", "{\"name\":\"John\"}") -> 200
ExecuteRequest("https://api.example.com/users/1", "DELETE") -> 204
ExecuteRequest("https://api.example.com/users/999", "DELETE") -> 404
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> ExecuteRequest(string url, string method, string jsonContent = null)
    {
        using var client = new HttpClient();
        HttpResponseMessage response;

        // 根据 method 参数执行 PUT 或 DELETE（忽略大小写）
        if (method.ToUpper() == "PUT")
        {
            // PUT：将 jsonContent 作为请求体发送
            var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
            response = await client.PutAsync(url, content);
        }
        else
        {
            // DELETE：不需要请求体
            response = await client.DeleteAsync(url);
        }

        // 将 HTTP 状态码作为整数返回
        return (int)response.StatusCode;
    }
}
```
