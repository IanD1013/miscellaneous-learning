### 使用 POST 请求发送 JSON

在处理现代 API 时，你通常需要在 POST 请求中发送 JSON 数据。
.NET 提供了两种方法：使用 `StringContent` 进行手动序列化，以及便捷的 `PostAsJsonAsync` 扩展方法。

### 结合 JSON 使用 StringContent

手动方法可让你完全控制序列化过程：

```csharp
var data = new { Name = "Alice", Score = 100 };
string json = JsonSerializer.Serialize(data);

var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync(url, content);
```

### 使用 PostAsJsonAsync

`PostAsJsonAsync` 扩展方法会自动处理序列化：

```csharp
var data = new { Name = "Alice", Score = 100 };
var response = await client.PostAsJsonAsync(url, data);
```

### 主要差异

| 方法 | 优点 | 缺点 |
| --- | --- | --- |
| StringContent | 完全控制，适用范围广 | 较为冗长 |
| PostAsJsonAsync | 简洁，不易出错 | 需要 System.Net.Http.Json |

### 所需命名空间

```csharp
using System.Text;           // 用于 Encoding.UTF8
using System.Text.Json;      // 用于 JsonSerializer
using System.Net.Http.Json;  // 用于 PostAsJsonAsync
```

### 你的任务

实现两个将 Person 对象作为 JSON 进行 POST 的方法：

1. `PostJsonContent` - 使用 `JsonSerializer.Serialize` 和内容类型为 `"application/json"` 的 `StringContent`
2. `PostWithJsonExtension` - 使用 `PostAsJsonAsync` 获得更简洁的实现方式

两个方法都应将 HTTP 状态码作为整数返回。

### 方法签名

```csharp
public static async Task<int> PostJsonContent(string url, string name, int age)
public static async Task<int> PostWithJsonExtension(string url, string name, int age)
```

### 预期结果

```
PostJsonContent("https://api.example.com/users", "John", 30) -> 201
PostWithJsonExtension("https://api.example.com/users", "Jane", 25) -> 201
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int> PostJsonContent(string url, string name, int age)
    {
        // 创建 Person 对象，序列化为 JSON，并使用 StringContent 发送 POST 请求
        var person = new Person { Name = name, Age = age };
        string json = JsonSerializer.Serialize(person);

        using var client = new HttpClient();
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        var response = await client.PostAsync(url, content);

        // 将状态码作为整数返回
        return (int)response.StatusCode;
    }
    
    public static async Task<int> PostWithJsonExtension(string url, string name, int age)
    {
        // 使用 PostAsJsonAsync 发送 Person 对象
        var person = new Person { Name = name, Age = age };

        using var client = new HttpClient();
        var response = await client.PostAsJsonAsync(url, person);

        // 将状态码作为整数返回
        return (int)response.StatusCode;
    }
}

public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}
```
