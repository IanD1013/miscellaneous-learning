### 带有 `yield return` 的异步迭代器方法

C# 支持一种强大的组合：在同一个方法体中同时使用 `await` 和 `yield return` 的**异步迭代器方法**。
这使你可以惰性（lazily）生成值流，在决定是否生成以及生成什么内容之前，先针对每个元素执行异步操作。
当你需要从异步数据源一次产出一个结果时（例如读取数据库行、处理 API 分页或通过异步验证过滤项目），这种模式是必不可少的。

### 工作原理

普通的迭代器方法在返回 `IEnumerable<T>` 的方法内部使用 `yield return`。
异步迭代器方法也是如此，但返回类型为 `IAsyncEnumerable<T>`，且方法被标记为 `async`。
在方法内部，你可以在每次 `yield return` 之前 `await` 任何异步操作。
调用方则使用 `await foreach` 代替普通的 `foreach` 来消费该流。

核心原理：`yield return` 会暂停方法并向消费者产出一个值，而 `await` 会暂停方法以等待异步操作。
两者结合起来，就创建了一个基于拉取（pull-based）的异步流：每次迭代都会恢复方法的执行、执行异步操作并产出下一个结果。

### 语法

```csharp
// 异步迭代器方法
async IAsyncEnumerable<T> ProduceItemsAsync()
{
    foreach (var item in someSource)
    {
        await SomeAsyncWork();   // 异步暂停
        yield return item;       // 向消费者产出值
    }
}

// 消费异步流
async Task ConsumeAsync()
{
    await foreach (var item in ProduceItemsAsync())
    {
        // 在每个元素到达时进行处理
    }
}
```

### 示例

这是一个模拟从慢速服务中获取用户名的异步迭代器：

```csharp
async IAsyncEnumerable<string> FetchUserNamesAsync(int[] userIds)
{
    foreach (var id in userIds)
    {
        // 为每个用户模拟一次异步网络调用
        await Task.Delay(10);
        yield return $"User_{id}";
    }
}

// 消费：
async Task PrintUsersAsync()
{
    await foreach (var name in FetchUserNamesAsync(new[] { 1, 2, 3 }))
    {
        Console.WriteLine(name);  // User_1, User_2, User_3
    }
}
```

下面是一个使用异步谓词进行过滤的示例，仅产出通过验证的项：

```csharp
async IAsyncEnumerable<string> GetValidEmailsAsync(string[] emails)
{
    foreach (var email in emails)
    {
        // 模拟异步验证
        await Task.Yield();
        if (email.Contains("@"))
        {
            yield return email;
        }
    }
}
```

注意该方法如何仅产出满足条件的元素。
不匹配的元素会被直接跳过，不会为它们产出任何值。

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `await Task.Yield()` | 让出控制权以模拟无延迟的异步操作 |
| `await Task.Delay(ms)` | 通过时间延迟模拟真实的异步操作 |
| `await foreach (var x in stream)` | 消费 `IAsyncEnumerable<T>` |
| 条件 `yield return` | 仅产出符合条件的元素 |
| 收集到列表 | 使用 `await foreach` 将元素添加到 `List<T>`，然后进行转换 |

### 注意事项

- 异步迭代器**必须**返回 `IAsyncEnumerable<T>`（而不是 `Task<IAsyncEnumerable<T>>`）
- 它**必须**包含至少一个 `yield return` 语句
- 它**必须**包含至少一个 `await` 表达式
- 消费者**必须**使用 `await foreach` 来遍历流
- 你可以将异步迭代器定义为一个**私有辅助方法**，并从你的公开方法中调用它

### 你的任务

编写一个方法 `FilterAsync`，接收一个 `int[]` 并以 `int[]` 形式返回其中的偶数。
在内部，你必须定义并使用一个**异步迭代器方法**（返回 `IAsyncEnumerable<int>`），该方法遍历输入，对每个元素执行 `await`（例如 `await Task.Yield()`），并使用 `yield return` 仅产出偶数。
你的 `FilterAsync` 方法应使用 `await foreach` 消费此异步流，收集结果，并将其作为数组返回。
元素的顺序必须保持不变。

### 方法签名

```csharp
public static async Task<int[]> FilterAsync(int[] numbers)
```

### 预期结果

```scss
FilterAsync([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]
FilterAsync([7, 11, 13]) -> []
FilterAsync([2, 4, 6, 8]) -> [2, 4, 6, 8]
FilterAsync([]) -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public class Solution
{
    public static async Task<int[]> FilterAsync(int[] numbers)
    {
        // 使用 await foreach 消费异步迭代器，按原顺序收集结果
        var results = new List<int>();
        await foreach (var number in EvenNumbersAsync(numbers))
        {
            results.Add(number);
        }
        return results.ToArray();
    }

    // 私有异步迭代器：对每个元素执行 await，只产出偶数
    private static async IAsyncEnumerable<int> EvenNumbersAsync(int[] numbers)
    {
        foreach (var number in numbers)
        {
            await Task.Yield(); // 模拟异步操作
            if (number % 2 == 0)
            {
                yield return number;
            }
        }
    }
}
```
