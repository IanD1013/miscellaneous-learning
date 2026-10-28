### static 关键字

`static` 关键字表示某项内容属于**类型本身**，而不是该类型的各个单独实例（对象）。
静态成员在类的所有使用中都是共享的。

### 静态字段

静态字段由访问该类的所有代码共享。
无论你调用该类的方法多少次，它都只有一份副本。

```csharp
public class Counter
{
    private static int count = 0;  // 在所有调用之间共享
    
    public static int GetCount()
    {
        return count;
    }
}
```

### 静态方法

静态方法属于类本身，而不属于某个对象。
你可以直接使用类名来调用它们。

```csharp
// 调用静态方法 - 不需要对象
int result = Math.Max(5, 10);  // Math 是一个类，Max 是静态方法
string text = Console.ReadLine();  // Console 是一个类
```

### 实例与静态对比

| 方面 | 实例 (non-static) | 静态 (Static) |
| --- | --- | --- |
| 归属 | 单个对象 | 类本身 |
| 访问方式 | 对象变量 | 类名 |
| 内存 | 每个对象拥有独立副本 | 仅一份共享副本 |
| 示例 | `myString.Length` | `Math.Abs(-5)` |

### 为什么使用静态？

- **工具方法**：不需要对象状态的函数（例如 `Math.Sqrt`）
- **共享状态**：在整个应用程序中共享的计数器、配置或缓存
- **工厂方法**：用于创建对象的方法

### 你的任务

使用静态计数器创建一个简单的 ID 生成器。
实现以下三个方法：

1. `GetNextId()` - 递增计数器并返回新值
2. `GetCurrentCount()` - 返回当前计数器值而不对其进行修改
3. `ResetCounter()` - 将计数器重置为 0

### 方法签名

```csharp
public static int GetNextId()        // 返回下一个 ID（1, 2, 3, ...）
public static int GetCurrentCount()  // 返回当前计数器值
public static void ResetCounter()    // 将计数器重置为 0
```

### 预期结果

```
GetNextId() -> 1  (第一次调用)
GetNextId() -> 2  (第二次调用)
GetCurrentCount() -> 2  (计数器为 2)
ResetCounter()  (计数器回到 0)
GetNextId() -> 1  (重新开始)
```

### 解答

```csharp
using System;

public class Solution
{
    // 声明一个静态字段来跟踪计数器
    private static int counter = 0;
    
    public static int GetNextId()
    {
        // 递增计数器并返回下一个 ID
        counter++;
        return counter;
    }
    
    public static int GetCurrentCount()
    {
        // 返回当前计数器值，不进行递增
        return counter;
    }
    
    public static void ResetCounter()
    {
        // 将计数器重置为 0
        counter = 0;
    }
}
```
