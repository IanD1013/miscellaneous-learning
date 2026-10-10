### 什么是 BaseAddress？

`BaseAddress` 是 `HttpClient` 上的一个属性，用于为所有请求设置基础 URL。
无需在每个请求中重复完整的 URL，只需设置一次基础地址并使用相对路径即可。

### 设置 BaseAddress

```csharp
var client = new HttpClient();
client.BaseAddress = new Uri("https://api.example.com/");

// 现在可以使用相对路径
string result = await client.GetStringAsync("users");  // 调用 https://api.example.com/users
string data = await client.GetStringAsync("products"); // 调用 https://api.example.com/products
```

### 不使用 BaseAddress 与使用 BaseAddress 的对比

```csharp
// 不使用 BaseAddress - 重复基础 URL
await client.GetStringAsync("https://api.example.com/users");
await client.GetStringAsync("https://api.example.com/products");
await client.GetStringAsync("https://api.example.com/orders");

// 使用 BaseAddress - 更简洁、更易维护
client.BaseAddress = new Uri("https://api.example.com/");
await client.GetStringAsync("users");
await client.GetStringAsync("products");
await client.GetStringAsync("orders");
```

### 重要提示：末尾斜杠

基础 URL 应当以末尾斜杠（`/`）结尾，以确保相对路径能够被正确解析：

```csharp
// 正确 - 基础地址以 / 结尾
client.BaseAddress = new Uri("https://api.example.com/");
await client.GetStringAsync("users"); // -> https://api.example.com/users

// 注意：带路径但没有末尾斜杠的基础地址会丢掉最后一段
client.BaseAddress = new Uri("https://api.example.com/v2");
await client.GetStringAsync("items"); // -> https://api.example.com/items（v2 丢失了）
```

### 你的任务

编写一个方法，完成以下操作：

1. 创建一个 `HttpClient` 实例
2. 将 `BaseAddress` 属性设置为提供的基础 URL
3. 在该 client 上使用 `GetStringAsync` 从相对路径获取内容
4. 返回响应内容

### 方法签名

```csharp
public static async Task<string> FetchWithBaseAddress(string baseUrl, string relativePath)
```

### 预期结果

```
FetchWithBaseAddress("https://api.example.com/", "hello") -> "Hello, World!"
FetchWithBaseAddress("https://data.service.io/", "status") -> "OK"
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<string> FetchWithBaseAddress(string baseUrl, string relativePath)
    {
        // 创建 HttpClient，并将 baseUrl 设置为 BaseAddress
        using var client = new HttpClient();
        client.BaseAddress = new Uri(baseUrl);

        // 然后从 relativePath 获取内容
        return await client.GetStringAsync(relativePath);
    }
}
```
