### LINQ 与手动循环：理解性能权衡

LINQ 是 C# 最强大的特性之一，它能让你用简洁的声明式代码表达复杂的数据转换。
但这种表达能力是有代价的。
理解**何时**这种代价很重要（以及何时并不重要）是编写生产级高质量 C# 代码的关键技能。

### LINQ 的开销从何而来？

像 `Where`、`Select` 和 `First` 这样的 LINQ 方法依赖于三种机制，与原生 `for` 循环相比，它们会引入额外的开销：

1. **委托调用（Delegate Invocation）** - 你传入的每一个 lambda（例如 `x => x > 5`）都会变成一个委托。调用委托比内联代码慢，因为 JIT 并不总能将其内联，而且存在通过函数指针进行的间接调用。
2. **迭代器状态机（Iterator State Machines）** - 像 `Select` 和 `Where` 这样的方法返回由编译器生成的状态机所支持的 `IEnumerable<T>`。每次调用 `MoveNext()` 都涉及状态转换，这比递增索引变量更重。
3. **堆分配与装箱（Heap Allocations & Boxing）** - 匿名类型、捕获变量的闭包以及枚举器对象本身都是在堆上分配的。在对分配敏感的代码中（游戏循环、高频交易、实时系统），这会产生 GC 压力。

### 何时它才真正重要？

对于**大多数应用程序代码**（Web 控制器、业务逻辑、CRUD 操作），LINQ 的开销是可以忽略不计的。
一个耗时 50 毫秒的数据库查询完全会让微秒级的 LINQ 开销显得微不足道。
**在这种场景下，可读性胜出。**

但在**热点路径**（hot paths）上（处理数百万项的紧凑内部循环、实时音视频管线、低延迟网络），开销会不断累积。
在这些上下文中，手动 `for` 循环或基于 `Span<T>` 的 API 可能会快 2 到 10 倍。

### 语法：带索引的 LINQ `Select`

LINQ 的 `Select` 方法有一个重载，可以同时为你提供元素及其索引：

```csharp
// 通用语法
source.Select((element, index) => new { element, index })
```

这会将每个元素投射到一个包含值及其位置的匿名类型中。
然后你可以过滤或搜索这个投影后的序列。

### 示例

```csharp
// 示例 1：查找第一个负数的索引
int[] temps = { 12, 5, -3, 8, -1 };
var match = temps
    .Select((val, idx) => new { val, idx })
    .FirstOrDefault(x => x.val < 0);
int result = match != null ? match.idx : -1;
// result 为 2（元素 -3 位于索引 2）

// 示例 2：查找第一个长度超过 5 个字符的字符串的索引
string[] words = { "cat", "dog", "elephant", "fox" };
var found = words
    .Select((word, i) => new { word, i })
    .FirstOrDefault(x => x.word.Length > 5);
int pos = found != null ? found.i : -1;
// pos 为 2（"elephant" 位于索引 2）

// 示例 3：等价的手动循环（用于对比）
int manualResult = -1;
for (int i = 0; i < temps.Length; i++)
{
    if (temps[i] < 0) { manualResult = i; break; }
}
// manualResult 同样为 2，但没有任何分配
```

### 核心概念

| 方法 | 作用 | 返回值 |
| --- | --- | --- |
| `Select((elem, idx) => ...)` | 投影每个元素及其索引 | `IEnumerable<T>` |
| `First(predicate)` | 返回第一个匹配项；若无匹配则抛出异常 | 匹配的项 |
| `FirstOrDefault(predicate)` | 返回第一个匹配项，若无匹配则返回 `null`/默认值 | 匹配的项或默认值 |

**重要提示：** 当 `FirstOrDefault` 用于引用类型序列（如匿名对象）时，如果未找到匹配项，它将返回 `null`。
当用于值类型（如 `int`）时，它返回 `default(int)` 即 `0`，因此你需要谨慎处理如何检测“未找到匹配项”。

### 你的任务

编写一个方法 `FindFirstMatch`，接受一个整数数组 `numbers` 和一个整数 `target`。
返回**严格大于** `target` 的**第一个元素的索引**。
如果不存在这样的元素，则返回 `-1`。

请使用结合了 `Select`（获取索引）和 `FirstOrDefault`（查找匹配项）的 **LINQ 方法**来实现这一点。

### 方法签名

```csharp
public static int FindFirstMatch(int[] numbers, int target)
```

### 预期结果

```scss
FindFirstMatch([1, 3, 5, 7, 9], 4)       -> 2
FindFirstMatch([10, 20, 30], 5)           -> 0
FindFirstMatch([1, 2, 3], 10)             -> -1
FindFirstMatch([], 5)                     -> -1
FindFirstMatch([5, 5, 5, 6], 5)           -> 3
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int FindFirstMatch(int[] numbers, int target)
    {
        // 把每个元素和它的索引投影成匿名对象，再找第一个严格大于 target 的元素
        var match = numbers
            .Select((val, idx) => new { val, idx })
            .FirstOrDefault(x => x.val > target);

        // 匿名对象是引用类型，未找到时为 null，此时返回 -1
        return match != null ? match.idx : -1;
    }
}
```
