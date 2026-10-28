### LINQ 中的延迟执行与提前具体化 (Deferred Execution vs. Early Materialization)

C# 中的 LINQ 查询**默认是惰性的 (lazy)**。
当你编写 `.Where(...)`、`.Select(...)` 或 `.OrderBy(...)` 时，此时并不会发生任何计算，LINQ 仅构建了一个执行计划，只有当你真正消费结果时才会运行。
这被称为**延迟执行 (deferred execution)**，它是 LINQ 最强大的性能特性之一。

相反的做法，即强制执行查询并将结果存储在内存中，被称为**具体化 (materialization)**。
诸如 `.ToList()`、`.ToArray()` 和 `.ToDictionary()` 之类的方法会触发具体化。

### 为什么延迟执行很重要

对 `.ToList()` 或 `.ToArray()` 的每次调用都会在内存中分配一个新的集合，并迭代处理截止到该位置的所有元素。
如果在长 LINQ 链中穿插具体化操作，每一次调用都会创建一个**完整的中间集合**，而该集合存在的唯一目的就是被下一个操作符迭代一次。
这既浪费了内存，又浪费了 CPU 周期。

以处理 100 万条记录为例：如果你在每一步操作后都进行具体化，可能会创建三个包含数十万项的独立列表。
而使用延迟执行，元素会逐个流经整个管道：单个元素在被过滤、转换并输出后，下一个元素才会进入。

### 何时进行具体化

只有在以下三种情况下，你**才应该**调用 `.ToList()` 或 `.ToArray()`：

1. **多次迭代** - 你需要多次遍历结果。对延迟查询的每次枚举都会重新执行整条调用链。
2. **集合修改** - 你需要添加、删除或修改元素。`IEnumerable<T>` 不支持修改操作。
3. **API 契约** - 某个方法或属性需要诸如 `List<T>`、`T[]` 或 `ICollection<T>` 等具体类型。

如果这些情况均不适用，请保持链式调用的延迟执行状态。

### 语法

```csharp
// 不好：不必要的中间具体化
var step1 = source.Where(x => x > 10).ToList();    // 分配一个 List<int>
var step2 = step1.Select(x => x * 2).ToList();      // 再分配一个 List<int>
var result = step2.OrderBy(x => x).ToArray();        // 分配一个 int[]
// 三次分配，三次完整迭代！

// 好：单个延迟链，只在最后具体化一次
var result = source
    .Where(x => x > 10)
    .Select(x => x * 2)
    .OrderBy(x => x)
    .ToArray();  // 一次分配，元素流经整个管道
```

### 示例

```csharp
// 示例 1：过滤并投影员工薪资
string[] highEarners = employees
    .Where(e => e.Salary > 80000)
    .Select(e => e.Name)
    .OrderBy(name => name)
    .ToArray();  // 只具体化一次，因为我们需要 string[]

// 示例 2：多次迭代需要具体化
var expensiveItems = catalog
    .Where(i => i.Price > 100)
    .ToList();  // 在这里具体化，因为下面要迭代两次

int count = expensiveItems.Count;
decimal total = expensiveItems.Sum(i => i.Price);

// 示例 3：反模式，无缘无故在中间调用 ToList()
var bad = orders
    .Where(o => o.Status == "Shipped")
    .ToList()                              // 不必要的分配！
    .Select(o => o.Total)
    .ToList()                              // 又一次不必要的分配！
    .OrderByDescending(t => t)
    .ToArray();

// 修正后的版本：
var good = orders
    .Where(o => o.Status == "Shipped")
    .Select(o => o.Total)
    .OrderByDescending(t => t)
    .ToArray();  // 单次具体化
```

### 实用参考

| 方法 | 是否延迟？ | 说明 |
| --- | --- | --- |
| `.Where()` | 是 | 惰性过滤元素 |
| `.Select()` | 是 | 惰性投影元素 |
| `.Distinct()` | 是 | 惰性去除重复项（使用内部 set） |
| `.OrderBy()` | 是\* | 延迟到枚举时执行，但必须读取所有元素才能排序 |
| `.ToList()` | **否** | 立即具体化为 `List<T>` |
| `.ToArray()` | **否** | 立即具体化为 `T[]` |
| `.Count()` | **否** | 强制枚举以进行计数 |

\* `OrderBy` 的延迟性在于直到枚举时才会执行，但一旦触发，它必须读取整个数据源来进行排序。

### 你的任务

编写一个接收整数数组和阈值的方法。
返回一个新的 `int[]`，其中仅包含**严格大于**该阈值的**去重**值，并按**升序**排序。

核心约束条件：构建**单个 LINQ 链**，不进行中间具体化。
仅在链的最后调用一次 `.ToArray()`。

### 方法签名

```csharp
public static int[] OptimalChain(int[] numbers, int threshold)
```

### 预期结果

```scss
OptimalChain([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 3) -> [4, 5, 6, 9]
OptimalChain([10, 20, 30, 10, 20], 15) -> [20, 30]
OptimalChain([1, 2, 3], 5) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] OptimalChain(int[] numbers, int threshold)
    {
        // 单个延迟链：过滤、去重、升序排序，只在最后具体化一次
        return numbers
            .Where(n => n > threshold)
            .Distinct()
            .OrderBy(n => n)
            .ToArray();
    }
}
```
