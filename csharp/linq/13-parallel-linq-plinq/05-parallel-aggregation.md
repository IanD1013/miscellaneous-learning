### PLINQ 聚合操作

PLINQ（并行 LINQ）使您只需对代码进行极少的更改，即可跨多个线程运行 LINQ 查询。
它最实用的用途之一是**并行聚合**：在大型集合上计算总和、计数、平均值、最小值和最大值，速度明显快于单线程 LINQ。
在底层，PLINQ 会对数据进行分区，在不同线程上独立聚合各个分区，然后将部分结果合并为单个最终值。
其计算结果在数学上与顺序 LINQ 完全相同。

### 工作原理

当您在序列上调用 `.AsParallel()` 时，PLINQ 会创建一个 `ParallelQuery<T>`，将工作分发到可用的 CPU 核心上。
诸如 `Sum()`、`Count()`、`Average()`、`Min()` 和 `Max()` 等聚合运算符专门针对这种并行执行模型进行了优化：

1. **分区（Partition）** - 源集合被拆分成多个数据块（大致每个核心一个）。
2. **局部聚合（Local Aggregate）** - 每个分区独立计算自己的部分结果。
3. **合并（Merge）** - 将部分结果合并为最终答案。

因为加法既满足结合律又满足交换律，所以处理顺序无关紧要，您始终会获得相同的结果。

### 语法

```csharp
// 将任意 IEnumerable<T> 转换为并行查询
var parallelQuery = source.AsParallel();

// 然后链式调用任意标准聚合操作符
var result = parallelQuery.Sum();       // 并行求和
var count  = parallelQuery.Count();     // 并行计数
var avg    = parallelQuery.Average();   // 并行求平均值
var min    = parallelQuery.Min();       // 并行求最小值
var max    = parallelQuery.Max();       // 并行求最大值

// 也可以使用带选择器的重载
var total = source.AsParallel().Sum(x => (long)x);
```

### 示例

```csharp
// 示例 1：并行计算温度平均值
double[] temps = { 72.5, 68.3, 75.1, 80.0, 66.9 };
double avgTemp = temps.AsParallel().Average();
// avgTemp == 72.56（与 temps.Average() 相同）

// 示例 2：并行统计偶数个数
int[] data = Enumerable.Range(1, 1_000_000).ToArray();
int evenCount = data.AsParallel().Count(x => x % 2 == 0);
// evenCount == 500000

// 示例 3：使用选择器并行求最大值
string[] words = { "apple", "banana", "cherry", "date" };
int longestLength = words.AsParallel().Max(w => w.Length);
// longestLength == 6（"banana" 或 "cherry"）

// 示例 4：转换为 long 以防止溢出
int[] largeValues = { int.MaxValue, 1 };
// largeValues.Sum() 会抛出 OverflowException！
long safeSum = largeValues.AsParallel().Sum(n => (long)n);
// safeSum == 2147483648L
```

### 溢出考量

当对 `int` 数组求和时，默认的 `Sum()` 会返回一个 `int`，如果总和超过 `int.MaxValue`（约 21 亿），则会抛出 `OverflowException`。
为了安全地处理大数值总和，请使用带选择器的重载，在求和前将每个元素转换为 `long`。
这同样适用于顺序 LINQ 和 PLINQ。

### 你的任务

编写一个方法，使用 PLINQ 的并行聚合计算整数数组中所有元素的总和。
你的方法应该：

- 接收一个 `int[]` 并返回一个 `long`（以安全地处理大总和）
- 使用 `AsParallel()` 启用并行执行
- 使用 `Sum()` 计算总和
- 处理空数组（没有元素时的总和为 0）
- 正确处理包含负数的数组

### 方法签名

```csharp
public static long ParallelSum(int[] numbers)
```

### 预期结果

```scss
ParallelSum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) -> 55
ParallelSum([]) -> 0
ParallelSum([-5, 5, -10, 10]) -> 0
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static long ParallelSum(int[] numbers)
    {
        // 求和前将每个元素转换为 long，避免溢出；空数组的和为 0
        return numbers.AsParallel().Sum(n => (long)n);
    }
}
```
