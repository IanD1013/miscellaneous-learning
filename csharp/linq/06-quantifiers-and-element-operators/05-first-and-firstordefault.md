### First 和 FirstOrDefault - 元素检索操作符

在 C# 中处理集合时，通常需要获取满足某个条件的单个元素。
LINQ 提供了两个主要方法来实现此功能：`First` 和 `FirstOrDefault`。
理解何时使用它们至关重要，选错方法可能会导致应用程序崩溃或静默返回非预期值。

### 工作原理

**`First(predicate)`** 从左到右扫描集合，并返回满足断言（predicate）的第一个元素。
如果**没有元素匹配**，它将抛出 `InvalidOperationException`。
当您确信存在匹配项，并且希望在假设错误时立即报错时，这非常有用。

**`FirstOrDefault(predicate, defaultValue)`** 在存在匹配项时的行为与 `First` 完全相同：它返回第一个匹配的元素。
不同之处在于**未找到匹配项**时发生的情况：它不会抛出异常，而是返回您指定的 `defaultValue`。
这使得它非常适合生产环境代码，在这种情况下未找到匹配项属于正常场景而非错误。

### 语法

```csharp
// 如果没有匹配项，抛出 InvalidOperationException
T result = collection.First(element => condition);

// 如果没有匹配项，返回 defaultValue（该重载在 .NET 6+ 中可用）
T result = collection.FirstOrDefault(element => condition, defaultValue);

// 旧的重载 - 如果没有匹配项，返回 default(T)（int 为 0，引用类型为 null）
T result = collection.FirstOrDefault(element => condition);
```

带有显式 `defaultValue` 参数的版本（在 .NET 6 中引入）更受推荐，因为它避免了二义性：您可以精确控制“未找到”时的返回值。

### 示例

```csharp
string[] cities = { "Berlin", "Boston", "Bangkok", "Cairo" };

// 第一个以 'B' 开头的城市 → "Berlin"
string city = cities.First(c => c.StartsWith("B"));

// 第一个以 'Z' 开头的城市 → 抛出 InvalidOperationException！
// string oops = cities.First(c => c.StartsWith("Z"));

// 安全版本：如果没有城市以 'Z' 开头，返回 "Unknown"
string safe = cities.FirstOrDefault(c => c.StartsWith("Z"), "Unknown");
// safe == "Unknown"
```

```csharp
double[] temperatures = { 18.5, 22.1, 19.8, 30.4, 25.0 };

// 第一个高于 25 的温度 → 30.4
double hot = temperatures.First(t => t > 25.0);

// 第一个低于零的温度 → 返回 -999.0（我们的哨兵值）
double cold = temperatures.FirstOrDefault(t => t < 0.0, -999.0);
// cold == -999.0
```

### 常见模式

| 场景 | 使用 | 原因 |
| --- | --- | --- |
| 元素**必须**存在（否则为数据错误） | `First(predicate)` | 异常表明存在 bug |
| 元素**可能不存在**（正常场景） | `FirstOrDefault(predicate, default)` | 优雅降级 |
| 缺少引用类型时需要 null | `FirstOrDefault(predicate)` | 默认返回 `null` |
| 值类型需要自定义哨兵值 | `FirstOrDefault(predicate, sentinel)` | 避免将 `0` 与“未找到”混淆 |

### 您的任务

编写一个方法，搜索一个整数数组并返回**严格大于**给定阈值的**第一个数字**。
如果没有数字超过该阈值，则返回 `-1` 作为表示“未找到”的哨兵值。

思考哪种 LINQ 方法最适合这种情况：元素可能存在也可能不存在，并且您需要特定的回退值而不是抛出异常。

### 方法签名

```csharp
public static int FirstAboveThreshold(int[] numbers, int threshold)
```

### 预期结果

```scss
FirstAboveThreshold([1, 3, 5, 7], 4)       → 5
FirstAboveThreshold([1, 2, 3], 10)          → -1
FirstAboveThreshold([10, 20, 30], 0)        → 10
FirstAboveThreshold([], 5)                  → -1
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int FirstAboveThreshold(int[] numbers, int threshold)
    {
        // 返回第一个严格大于阈值的数字，未找到时返回哨兵值 -1
        return numbers.FirstOrDefault(n => n > threshold, -1);
    }
}
```
