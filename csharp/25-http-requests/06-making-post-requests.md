### 发送 POST 请求

GET 请求用于检索数据，而 POST 请求则向服务器发送数据。
这通常用于提交表单、创建资源或向 API 发送数据。

### PostAsync 方法

```csharp
// PostAsync 向 URL 发送数据并返回 HttpResponseMessage
var response = await client.PostAsync(url, content);
```

### 用于请求体的 StringContent

要发送文本数据，请将其包装在 `StringContent` 对象中：

```csharp
// 使用文本、编码和媒体类型创建内容
var content = new StringContent("Hello", Encoding.UTF8, "text/plain");

// 用于 JSON 数据
var jsonContent = new StringContent("{\"name\":\"John\"}", Encoding.UTF8, "application/json");
```

### 完整的 POST 示例

```csharp
using var client = new HttpClient();
var content = new StringContent("my data", Encoding.UTF8, "text/plain");
var response = await client.PostAsync("https://api.example.com/submit", content);
int statusCode = (int)response.StatusCode;
```

### GET 与 POST 的对比

| 方面 | GET | POST |
| --- | --- | --- |
| 目的 | 检索数据 | 发送数据 |
| 请求体 | 无 | 包含数据 |
| 方法 | `GetAsync(url)` | `PostAsync(url, content)` |

### 你的任务

创建一个方法，该方法发送包含字符串数据的 POST 请求并返回 HTTP 状态码。

### 方法签名

```csharp
public static async Task<int> PostData(string url, string data)
```

### 预期结果

```
PostData("https://api.example.com/submit", "Hello") -> 200
PostData("https://api.example.com/create", "New Item") -> 201
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> PostData(string url, string data)
    {
        // 创建 HttpClient
        using var client = new HttpClient();

        // 使用 data 创建 StringContent
        var content = new StringContent(data, Encoding.UTF8, "text/plain");

        // 向 URL 发送 POST 请求
        var response = await client.PostAsync(url, content);

        // 将状态码作为整数返回
        return (int)response.StatusCode;
    }
}
```
