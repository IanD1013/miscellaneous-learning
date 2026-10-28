### IAsyncEnumerable 与 PLINQ：选择合适的并发模型

C# 提供了两种用于并发处理集合的强大工具，但它们解决的问题有着本质的不同。
选错工具不仅会降低性能，还可能因浪费线程或完全失去并行性而对应用程序造成实质性损害。
理解**何时**使用它们，比了解**如何**使用它们更为重要。

### 各种模型的工作原理

**PLINQ (Parallel LINQ)** 将集合划分到多个 CPU 核心上，并在独立的线程上同时处理各个数据块。
当每个元素都需要大量计算时（例如哈希计算、图像处理、数学建模），它能大显身手，因为它可以让所有核心都忙于处理实际工作。

**IAsyncEnumerable / Async LINQ** 逐个处理元素，但在等待每个结果时**不会阻塞线程**。
当你调用 API、从数据库读取数据或等待文件时，线程会被释放回线程池。
这对于 I/O 密集型（I/O-bound）操作至关重要，因为瓶颈在于外部资源，而不是你的 CPU。

### 核心区别

| 工作负载类型 | 瓶颈 | 合适的工具 | 原因 |
| --- | --- | --- | --- |
| CPU 密集型（CPU-bound） | 处理器周期 | PLINQ | 将计算分布到各个核心 |
| I/O 密集型（I/O-bound） | 外部资源 | Async LINQ | 在等待期间释放线程 |

### 为什么选错会有害

将 **PLINQ 用于 I/O 密集型工作**会生成多个线程，而这些线程都会立即阻塞以等待网络或磁盘响应。
你消耗了线程池线程却什么都没做，这是导致 Web 应用程序中线程池饥饿（thread pool starvation）的根源。

将 **async LINQ 用于 CPU 密集型工作**会通过在每个元素上使用 `await` 来按顺序处理元素。
你将获得零并行性，因为 `async`/`await` 的本质是非阻塞，而不是同时执行任务。

### 实际示例

考虑一个验证税号（tax ID）的服务。
每次验证都涉及一个复杂的校验和算法，需要 50 毫秒的纯计算：

```csharp
// CPU 密集型：使用 PLINQ 在多个核心上并行处理
var results = taxIds.AsParallel()
    .Select(id => ValidateChecksum(id))
    .ToList();
```

现在考虑一个从远程 API 获取用户配置文件的服务：

```csharp
// I/O 密集型：使用 async LINQ 避免阻塞线程
await foreach (var userId in userIdStream)
{
    var profile = await httpClient.GetAsync($"/users/{userId}");
    yield return ParseProfile(profile);
}
```

批量图片缩放？CPU 密集型（CPU-bound）- PLINQ。
从多个云存储桶中拉取日志的聚合器？I/O 密集型（I/O-bound）- async LINQ。
运行统计模型的报告生成器？CPU 密集型（CPU-bound）- PLINQ。
对数十个微服务进行 ping 测试的健康检查器？I/O 密集型（I/O-bound）- async LINQ。

### 决策框架

问问自己：**“线程是在工作，还是在等待某些东西？”**

- 如果线程正在**积极计算**（转换数据、处理数字、编码/解码），则该工作负载为 **CPU-bound**。
- 如果线程在**等待时处于空闲状态**（等待网络响应、文件读取、数据库查询），则该工作负载为 **I/O-bound**。

### 你的任务

编写一个方法，根据工作负载的性质推荐正确的并发方法。
给定一个表示工作负载是否为 I/O-bound 的布尔值，对于 I/O 密集型工作负载返回字符串 `"async LINQ"`，对于 CPU 密集型工作负载返回 `"PLINQ"`。

### 方法签名

```csharp
public static string ChooseApproach(bool isIoBound)
```

### 预期结果

```rust
ChooseApproach(true)  -> "async LINQ"   // I/O 密集型：网络调用、文件读取
ChooseApproach(false) -> "PLINQ"        // CPU 密集型：计算、数据处理
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

public class Solution
{
    public static string ChooseApproach(bool isIoBound)
    {
        // I/O 密集型选 async LINQ，CPU 密集型选 PLINQ
        return isIoBound ? "async LINQ" : "PLINQ";
    }
}
```
