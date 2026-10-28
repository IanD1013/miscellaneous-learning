### using 语句

`using` 语句可确保在用完 `IDisposable` 对象后对其进行妥善清理，即使发生异常也是如此。
这就是 C# 管理文件、数据库连接、网络套接字和锁的方式。

### IDisposable 模式

持有资源的类型会实现 `IDisposable`。
当调用 `Dispose()` 时，所持有的资源就会被释放：

```csharp
public class DatabaseConnection : IDisposable
{
    public void Dispose()
    {
        // 自动关闭连接
    }
}
```

### 传统的 using 块

经典语法使用花括号包裹代码，`Dispose()` 会在闭合花括号处被自动调用：

```csharp
using (var connection = new DatabaseConnection("server1"))
{
    connection.RunQuery("SELECT * FROM users");
} // 此处自动调用 Dispose() - 连接现已关闭
```

### 为什么这很重要

核心要点在于：一旦 `using` 块结束，`Dispose()` 就已经执行，资源也已被释放。
如果该资源是一个锁，那么该项现在就可以供其他人使用了。

| 不使用 using | 使用 using |
| --- | --- |
| 必须牢记调用 Dispose() | 自动清理 |
| 发生异常时可能会跳过清理 | 即使发生异常也能进行清理 |
| 资源泄漏 / 锁卡死 | 资源始终得到释放 |

### LockedResource 类

在 `Resource.cs` 中为你提供了一个 `LockedResource` 类。
主要成员包括：

| 成员 | 描述 |
| --- | --- |
| `new LockedResource(name)` | 获取（锁定）资源。如果已被锁定则抛出异常。 |
| `Process(content)` | 返回 `"[name] Processed: content"`。 |
| `LockedResource.IsAvailable(name)` (static) | 如果资源当前**未**被锁定，则返回 `true`。 |
| `Dispose()` | 释放锁（由 `using` 自动调用）。 |

### 你的任务

实现三个使用 `LockedResource` 类的方法：

1. **ProcessLockedResource(resourceName, content)**：使用 `using` 块获取资源、处理内容并返回结果。
2. **IsResourceAvailable(resourceName)**：返回给定的资源名称当前是否可用（未锁定）。
3. **ProcessThenReport(resourceName, content)**：使用 `using` 块处理内容。在 `using` 块结束**之后**（此时锁已被释放），检查资源是否再次可用。返回：`"Result: {processed}, ReleasedAfterUse: {isAvailable}"`。

注意在方法 3 中，资源在事后应该始终报告为可用，这证明了 `using` 块已正确释放了锁。

### 方法签名

```csharp
public static string ProcessLockedResource(string resourceName, string content)
public static bool IsResourceAvailable(string resourceName)
public static string ProcessThenReport(string resourceName, string content)
```

### 预期结果

```
ProcessLockedResource("doc", "hello") -> "[doc] Processed: hello"
IsResourceAvailable("file") -> True
ProcessThenReport("report", "data") -> "Result: [report] Processed: data, ReleasedAfterUse: True"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ProcessLockedResource(string resourceName, string content)
    {
        // 使用 Resource.cs 中的 LockedResource 类
        // 1. 使用 'using' 语句创建 LockedResource
        // 2. 调用其 Process(content) 获取处理结果
        // 3. 返回结果
        // 'using' 语句确保自动调用 Dispose()，
        // 从而释放锁，使资源再次空闲。
        using (var resource = new LockedResource(resourceName))
        {
            return resource.Process(content);
        }
    }

    public static bool IsResourceAvailable(string resourceName)
    {
        // 检查资源是否可用（当前未被锁定）
        // 使用静态辅助方法 LockedResource.IsAvailable(resourceName)
        return LockedResource.IsAvailable(resourceName);
    }

    public static string ProcessThenReport(string resourceName, string content)
    {
        // 使用 'using' 块处理内容，然后报告在块结束之后
        // 资源是否再次可用。
        // 因为 'using' 会在块结束时调用 Dispose()，锁会被释放，
        // 资源再次变为可用。
        // 返回："Result: {processed}, ReleasedAfterUse: {isAvailable}"
        //   其中 {isAvailable} 在 using 块关闭之后检查。
        string processed;
        using (var resource = new LockedResource(resourceName))
        {
            processed = resource.Process(content);
        }

        bool isAvailable = LockedResource.IsAvailable(resourceName);
        return $"Result: {processed}, ReleasedAfterUse: {isAvailable}";
    }
}
```
