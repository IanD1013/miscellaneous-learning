### 理解 PLINQ 开销

PLINQ（Parallel LINQ）可以通过将工作分配到多个 CPU 核心来加速数据处理。
然而，并行化**绝不是没有代价的**。
每个 PLINQ 查询在开始任何实际工作之前都会产生固定开销，理解这些开销对于编写高性能代码至关重要。

### PLINQ 开销的工作原理

当你在 LINQ 查询上调用 `.AsParallel()` 时，运行时会在后台执行多项操作：

1. **线程池调度（Thread Pool Scheduling）** - 必须从线程池分配或唤醒工作线程。
   这涉及同步原语和上下文切换。
2. **分区（Partitioning）** - 源集合被划分为多个块，以便每个线程处理一部分。
   分区器必须分析或迭代源集合以创建均衡的分区。
3. **结果合并（Result Merging）** - 并行执行后，来自各个线程的部分结果会被合并为单个输出序列。
   此合并步骤可能涉及缓冲、排序和同步。

无论每个元素需要多少实际工作量，这些步骤中的每一步都会增加**固定开销**。
对于像对每个数字加 1 这样微不足道的操作，在小型数据集上协调线程的开销可能会**超过总计算时间**。

### 经验法则

PLINQ 通常只有在**同时**满足以下两个条件时才值得使用：

- 数据集**足够大**（通常为数千个元素或更多）
- **单元素操作开销昂贵**（I/O、复杂数学运算、解析等）

如果缺少任一条件，顺序 LINQ 通常更快：

| 场景 | 元素数量 | 单元素开销 | 建议 |
| --- | --- | --- | --- |
| 过滤小列表 | 50 | 开销低的比较 | 顺序 |
| 从 10,000 个文件中解析 XML | 10,000 | 昂贵的 I/O | 并行 |
| 对 200 个整数求和 | 200 | 微不足道的加法 | 顺序 |
| 对 5,000 张位图进行图像处理 | 5,000 | 重度计算 | 并行 |
| 对 3,000 个项目进行字符串拼接 | 3,000 | 开销低的操作 | 顺序 |

### 语法

```csharp
// 顺序 LINQ - 没有并行开销
var result = data.Where(x => x.IsValid).Select(x => Process(x)).ToList();

// PLINQ - 会增加并行开销
var result = data.AsParallel().Where(x => x.IsValid).Select(x => Process(x)).ToList();
```

### 示例

```csharp
// 示例 1：根据工作负载特征做出决定
var workloads = new[] { new { Name = "ReportGen", Items = 50000, Heavy = true } };
var decisions = workloads
    .Select(w => w.Items >= 1000 && w.Heavy ? "parallel" : "sequential")
    .ToList();
// 结果：["parallel"] - 大型数据集且工作开销昂贵

// 示例 2：一次评估多个场景
var scenarios = new[] {
    new { Label = "TinyList", N = 10, Costly = false },
    new { Label = "BigCompute", N = 20000, Costly = true },
    new { Label = "BigCheap", N = 20000, Costly = false }
};
var recommendations = scenarios
    .Select(s => $"{s.Label}: {(s.N >= 1000 && s.Costly ? "go parallel" : "stay sequential")}")
    .ToList();
// 结果：["TinyList: stay sequential", "BigCompute: go parallel", "BigCheap: stay sequential"]
```

### 你的任务

编写一个实现 PLINQ 开销启发式规则的方法。
给定元素数量以及单元素操作是否昂贵，返回相应的策略：

- 仅当 `elementCount` 为 **1000 或更多**且 `isExpensiveOperation` 为 `true` 时返回 `"use parallel"`
- 在**所有其他情况**下返回 `"use sequential"`

使用 LINQ 风格的逻辑（投影、选择等）而不是单纯的 `if` 语句，以练习通过 LINQ 表达决策逻辑。

### 方法签名

```csharp
public static string ChooseApproach(int elementCount, bool isExpensiveOperation)
```

### 预期结果

```rust
ChooseApproach(500, true)    -> "use sequential"
ChooseApproach(5000, true)   -> "use parallel"
ChooseApproach(5000, false)  -> "use sequential"
ChooseApproach(1000, true)   -> "use parallel"
ChooseApproach(999, true)    -> "use sequential"
ChooseApproach(0, false)     -> "use sequential"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string ChooseApproach(int elementCount, bool isExpensiveOperation)
    {
        // 把输入包装成单元素序列，用 Select 投影出决策结果
        return new[] { elementCount }
            .Select(n => n >= 1000 && isExpensiveOperation ? "use parallel" : "use sequential")
            .First();
    }
}
```
