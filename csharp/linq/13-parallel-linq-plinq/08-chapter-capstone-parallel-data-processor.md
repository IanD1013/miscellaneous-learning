### PLINQ 综合实践：包含分组与聚合的并行管道

并行 LINQ（PLINQ）允许你以声明式方式表达数据并行管道，运行时会将其分区并在多个核心上执行。
在生产环境中，当需要对大型集合进行 CPU 密集型转换（如图像处理、财务计算、科学模拟）时，PLINQ 大放异彩，因为每个元素所需的计算工作量远大于线程协调的开销。

本综合实践练习将五个 PLINQ 概念结合到一个管道中：**并行过滤**、**有序执行**、**并行投影**、**按谓词分组**以及**并行聚合**。

### 工作原理

PLINQ 使用 `AsParallel()` 将顺序 LINQ 管道转换为并行管道。
默认情况下，PLINQ 不保证元素的顺序：由于各个分区并发执行，结果可能以任意顺序返回。
添加 `AsOrdered()` 可以在付出一定协调开销的代价下恢复原始元素的顺序。

一旦获得了并行查询，`Where` 和 `Select` 的工作方式与顺序查询相同，但会在各个分区之间并发执行。
像 `Sum`、`Count` 和 `Aggregate` 这样的聚合方法会将各个分区的局部结果合并为最终值。

### 语法

```csharp
// 基本的 PLINQ 管道
var result = source
    .AsParallel()       // 切换到并行执行
    .AsOrdered()        // 保留元素的原始顺序
    .Where(predicate)   // 并行过滤
    .Select(transform)  // 并行投影
    .ToArray();         // 具体化结果

// 并行聚合
int total = source.AsParallel().Where(predicate).Sum();
```

### 示例

```csharp
// 示例 1：对员工薪资进行并行过滤 + 转换
double[] salaries = { 45000, 62000, 38000, 91000, 55000 };
var highAdjusted = salaries
    .AsParallel()
    .AsOrdered()
    .Where(s => s > 50000)
    .Select(s => s * 1.10)   // 高收入者加薪 10%
    .ToArray();
// highAdjusted: [68200, 100100, 60500]

// 示例 2：按类别并行求和
int[] temps = { -5, 12, 0, 28, -3, 17, 35 };
int freezing = temps.AsParallel().Where(t => t <= 0).Sum();   // -8
int warm     = temps.AsParallel().Where(t => t > 0).Sum();    // 92

// 示例 3：拆分并聚合
int[] scores = { 88, 73, 95, 60, 42 };
var passing = scores.AsParallel().Where(s => s >= 70).ToArray();  // [88, 73, 95]
var failing = scores.AsParallel().Where(s => s < 70).ToArray();   // [60, 42]
int passSum = passing.AsParallel().Sum();  // 256
int failSum = failing.AsParallel().Sum();  // 102
```

### 常见模式

| 模式 | 用途 |
| --- | --- |
| `.AsParallel().Where(p).Select(t)` | 并行过滤然后转换 |
| `.AsParallel().AsOrdered()` | 具有确定性排序的并行处理 |
| `.AsParallel().Sum()` | 跨分区并行聚合 |
| `Array.Sort(arr)` | 原地排序数组以获得一致的输出 |
| `n % 2 == 0` | 检查数字是否为偶数 |

### 你的任务

编写 `ParallelProcess(int[] numbers)` 来执行以下步骤：

1. **过滤**输入以仅保留正数（大于零），使用 `AsParallel().AsOrdered().Where(...)`
2. 使用 `Select` 并行计算每个过滤后数字的**平方**
3. 将平方值**拆分**为两组：偶数和奇数
4. 使用并行聚合对每组进行**求和**
5. 将两个和按升序排序并作为 `int[]` **返回**

例如，给定 `[1, -2, 3, -4, 5, 6]`：

- 正数：`[1, 3, 5, 6]`
- 平方：`[1, 9, 25, 36]`
- 偶数平方：`[36]` → 和 = 36
- 奇数平方：`[1, 9, 25]` → 和 = 35
- 升序排序的结果：`[35, 36]`

### 方法签名

```csharp
public static int[] ParallelProcess(int[] numbers)
```

### 预期结果

```scss
ParallelProcess([1, -2, 3, -4, 5, 6]) -> [35, 36]
ParallelProcess([2, 4, 6])             -> [0, 56]
ParallelProcess([-1, -2, -3])          -> [0, 0]
ParallelProcess([7])                   -> [0, 49]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ParallelProcess(int[] numbers)
    {
        // 并行过滤正数（保持顺序）并计算平方
        int[] squares = numbers
            .AsParallel()
            .AsOrdered()
            .Where(n => n > 0)
            .Select(n => n * n)
            .ToArray();

        // 拆分为偶数组和奇数组，并分别并行求和
        int evenSum = squares.AsParallel().Where(n => n % 2 == 0).Sum();
        int oddSum = squares.AsParallel().Where(n => n % 2 != 0).Sum();

        // 将两个和按升序排序后返回
        int[] result = { evenSum, oddSum };
        Array.Sort(result);
        return result;
    }
}
```
