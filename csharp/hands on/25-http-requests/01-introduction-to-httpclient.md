### 什么是 HttpClient？

HttpClient 是 .NET 中用于向 Web 服务和 API 发送 HTTP 请求并接收 HTTP 响应的核心类。

### 为什么使用 HttpClient？

```csharp
// HttpClient 处理 HTTP 通信的所有复杂性
// - 发送 GET、POST、PUT、DELETE 请求
// - 管理请求头和内容
// - 处理响应和状态码
// - 支持 async/await 模式
```

### 创建 HttpClient

创建 HttpClient 非常简单，只需使用 `new` 关键字将其实例化即可。

```csharp
// 基本创建方式
HttpClient client = new HttpClient();

// 或者使用目标类型 new（C# 9+）
HttpClient client = new();
```

### `using` 关键字与释放（Disposal）

HttpClient 实现了 `IDisposable` 接口，这意味着它持有非托管资源（例如网络连接），这些资源在使用完毕后应当被释放。

```csharp
// 方式 1：using 语句（作用域结束时自动释放）
using (HttpClient client = new HttpClient())
{
    // 在这里发送请求
    // 当这个代码块结束时，client 会被自动释放
}

// 方式 2：using 声明（C# 8+，在方法结束时释放）
using HttpClient client = new HttpClient();
// 在这里发送请求
// 当方法返回时，client 会被释放
```

### Socket 耗尽问题

频繁创建和释放 HttpClient 会引发一个严重的问题，称为 **socket 耗尽**（socket exhaustion，或 socket starvation）。

```csharp
// 错误：每个请求都创建新的 HttpClient
for (int i = 0; i < 1000; i++)
{
    using HttpClient client = new HttpClient();
    var response = await client.GetAsync("https://api.example.com/data");
    // 释放后 socket 进入 TIME_WAIT 状态
    // socket 堆积的速度比回收的速度更快！
}
// 结果：SocketException - 没有更多可用的 socket！
```

当你释放 HttpClient 时，底层的 socket 会进入 `TIME_WAIT` 状态长达 240 秒，然后才会被完全释放。
在高负载下，可能会耗尽所有可用的 socket。

### 解决方案 1：复用单个实例

```csharp
// 适用于简单场景 - 复用同一个实例
public class ApiService
{
    // 单个实例，所有请求复用
    private static readonly HttpClient _client = new HttpClient();

    public async Task<string> GetDataAsync(string url)
    {
        return await _client.GetStringAsync(url);
    }
}
```

**DNS 缓存问题：** 静态 HttpClient 会永久缓存 DNS 查询结果。
如果服务器的 IP 地址发生变更（负载均衡轮换、故障转移、DNS 更新），你的应用程序在重启前将无法获取新的 IP。
这可能导致请求失败或被路由到错误的服务器。

```csharp
// 问题所在：DNS 只解析一次并被永久缓存
private static readonly HttpClient _client = new HttpClient();

// 如果 api.example.com 从 1.2.3.4 变为 5.6.7.8，
// _client 仍然会尝试连接 1.2.3.4！
```

对于长期运行的应用程序（Web 服务器、后台服务）来说，这是一个非常关键的问题。
请改用 `IHttpClientFactory`。

### 进阶：IHttpClientFactory（可选）

在更大型的应用程序中（例如使用 ASP.NET Core 构建的 Web 应用），通常不需要自己创建 `HttpClient`。
相反，你会通过 `IHttpClientFactory` 向框架请求一个实例，它会为你复用连接并刷新 DNS，从而避免上述两个问题。
它依赖于一种称为依赖注入（dependency injection）的技术，这超出了本课程的范围，因此在本次练习中不需要使用它。
目前规则很简单：创建一次 `HttpClient` 并复用它。

### 你的任务

创建并返回一个新的 HttpClient 实例。
由于你需要将其返回给调用方，请不要将其包装在 `using` 语句中，调用方将负责管理其生命周期和释放。

**注意：** 在实际应用中，建议优先使用 `IHttpClientFactory` 或共享的静态实例，以避免 socket 耗尽！

### 方法签名

```csharp
public static HttpClient CreateHttpClient()
```

### 预期结果

```
CreateHttpClient() -> HttpClient instance (not null)
```

### 解答

```csharp
using System;
using System.Net.Http;

public class Solution
{
    public static HttpClient CreateHttpClient()
    {
        // 创建并返回一个新的 HttpClient 实例（不使用 using，由调用方负责释放）
        return new HttpClient();
    }
}
```
