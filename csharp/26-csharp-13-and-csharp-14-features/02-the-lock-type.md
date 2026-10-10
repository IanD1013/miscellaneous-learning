### C# 13 中的 Lock 类型

C# 13 引入了 `System.Threading.Lock`，这是一种用于线程同步的专用类型，与传统的使用 `object` 的 `lock` 语句相比，它更高效且意图更明确。

### 传统的 lock 与 Lock 类型

```csharp
// 旧方式：使用 object 配合 lock
private static readonly object _syncRoot = new object();
lock (_syncRoot)
{
    // 临界区
}

// 新方式：使用 Lock 类型
private static readonly Lock _lock = new Lock();
using (_lock.EnterScope())
{
    // 临界区
}
```

### 为什么使用 Lock 类型？

| 方面 | 传统的 lock | Lock 类型 |
| --- | --- | --- |
| 类型安全 | 使用任意 object | 专用的 Lock 类型 |
| 意图 | 隐式 | 显式 |
| 性能 | 良好 | 针对加锁进行了优化 |
| 作用域控制 | 自动 | 通过 EnterScope() |

### 使用 EnterScope()

`EnterScope()` 方法返回一个实现了 `IDisposable` 的 `Lock.Scope` 结构体。
这允许你使用 `using` 语句来自动释放锁：

```csharp
private static readonly Lock _lock = new Lock();

void ThreadSafeMethod()
{
    using (_lock.EnterScope())
    {
        // 这段代码是线程安全的
        // 作用域结束时锁会自动释放
    }
}
```

### 你的任务

完成 `SafeIncrement` 方法，使用 `Lock` 类型安全地递增 `_counter` 字段。
多个线程将同时调用此方法，因此你必须确保线程安全。

### 方法签名

```csharp
private static void SafeIncrement()
```

### 预期结果

```
IncrementCounter(5) -> 5
IncrementCounter(10) -> 10
IncrementCounter(100) -> 100
```

### 解答

```csharp
using System;
using System.Threading;

public class Solution
{
    private static int _counter = 0;
    private static readonly Lock _lock = new Lock();
    
    public static int IncrementCounter(int times)
    {
        // 每个测试前重置计数器
        _counter = 0;
        
        // 创建多个线程来递增计数器
        Thread[] threads = new Thread[times];
        
        for (int i = 0; i < times; i++)
        {
            threads[i] = new Thread(() => SafeIncrement());
            threads[i].Start();
        }
        
        // 等待所有线程完成
        foreach (var thread in threads)
        {
            thread.Join();
        }
        
        return _counter;
    }
    
    private static void SafeIncrement()
    {
        // 使用 _lock.EnterScope() 获取锁，离开 using 块时自动释放
        using (_lock.EnterScope())
        {
            _counter++;
        }
    }
}
```
