### 反序列化 JSON 响应

当 API 返回 JSON 数据时，你需要将该 JSON 字符串转换为可以操作的 C# 对象。
这个过程称为反序列化。

### 使用 JsonSerializer.Deserialize

```csharp
using System.Text.Json;

// 定义一个与 JSON 结构匹配的类
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}

// 将 JSON 字符串反序列化为对象
string json = "{\"Name\":\"Widget\",\"Price\":29.99}";
Product product = JsonSerializer.Deserialize<Product>(json);
Console.WriteLine(product.Name);  // Widget
```

### 将 HttpClient 与反序列化结合使用

```csharp
using var client = new HttpClient();
string json = await client.GetStringAsync("https://api.example.com/product");
Product product = JsonSerializer.Deserialize<Product>(json);
```

### 处理大小写差异

API 返回的 JSON 通常使用 camelCase（`name`），而 C# 使用 PascalCase（`Name`）。
使用 `JsonSerializerOptions` 来处理这种情况：

```csharp
var options = new JsonSerializerOptions 
{ 
    PropertyNameCaseInsensitive = true 
};
var product = JsonSerializer.Deserialize<Product>(json, options);
```

### 你的任务

实现两个从 URL 获取 JSON 并返回特定属性的方法：

1. `GetUserName` - 返回用户的 `Name` 属性
2. `GetUserAge` - 返回用户的 `Age` 属性

`User` 类已经定义好了 `Name`、`Age` 和 `Email` 属性。

### 方法签名

```csharp
public static async Task<string> GetUserName(string url)
public static async Task<int> GetUserAge(string url)
```

### 预期结果

```
GetUserName("https://api.example.com/user") -> "Alice"
GetUserAge("https://api.example.com/user") -> 30
```

### 解答

```csharp
using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

public class User
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Email { get; set; }
}

public class Solution
{
    public static async Task<string> GetUserName(string url)
    {
        // 从 URL 获取 JSON 并反序列化为 User 对象
        using var client = new HttpClient();
        string json = await client.GetStringAsync(url);

        // 忽略大小写，同时兼容 camelCase 和 PascalCase 的 JSON
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        User user = JsonSerializer.Deserialize<User>(json, options);

        // 返回 Name 属性
        return user.Name;
    }

    public static async Task<int> GetUserAge(string url)
    {
        // 从 URL 获取 JSON 并反序列化为 User 对象
        using var client = new HttpClient();
        string json = await client.GetStringAsync(url);

        // 忽略大小写，同时兼容 camelCase 和 PascalCase 的 JSON
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        User user = JsonSerializer.Deserialize<User>(json, options);

        // 返回 Age 属性
        return user.Age;
    }
}
```
