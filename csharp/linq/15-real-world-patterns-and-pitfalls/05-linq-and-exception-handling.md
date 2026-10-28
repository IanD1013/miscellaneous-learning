### LINQ 管道中的异常安全性

C# 中的 LINQ 查询采用**延迟执行**：传递给 `Where`、`Select` 和其他操作符的谓词与选择器在*定义*查询时并不会运行。
它们只会在你*枚举*查询时运行（例如调用 `ToArray()`、`ToList()` 或使用 `foreach` 进行迭代）。
这意味着 Lambda 内部抛出的任何异常都会传播到*枚举点的调用方*，而不是声明查询的位置。
这种微妙的行为会使 bug 难以追踪，并可能在意想不到的地方导致应用程序崩溃。

像 `strings.Select(s => int.Parse(s))` 这种朴素的做法，在枚举遇到非数字字符串的瞬间就会抛出 `FormatException`，而且该异常会从调用 `ToArray()` 或 `foreach` 的地方冒泡抛出，这可能离编写查询的地方很远。

### 工作原理

最安全的模式是通过使用返回成功/失败而不是直接抛出异常的验证方法，在 LINQ Lambda 内部**彻底避免异常**。
`TryParse` 系列方法（`int.TryParse`、`double.TryParse`、`DateTime.TryParse` 等）返回一个指示是否成功的 `bool`，并通过 `out` 参数输出解析后的值。
通过在 LINQ 管道中使用这些方法，你可以优雅地过滤掉无效数据，而永远不会触发异常。

### 语法

```csharp
// TryParse 的签名
bool int.TryParse(string s, out int result)

// 在 LINQ lambda 中配合可空投影使用 TryParse
source.Select(item => int.TryParse(item, out int n) ? (int?)n : null)
      .Where(x => x.HasValue)
      .Select(x => x.Value);

// 另一种做法：先过滤，再安全地解析
source.Where(item => int.TryParse(item, out _))
      .Select(item => int.Parse(item));
```

### 示例

```csharp
// 示例 1：从混合输入中安全地提取 double
string[] temps = { "98.6", "N/A", "101.2", "--", "97.0" };
double[] validTemps = temps
    .Select(t => double.TryParse(t, out double d) ? (double?)d : null)
    .Where(t => t.HasValue)
    .Select(t => t.Value)
    .ToArray();
// 结果：[98.6, 101.2, 97.0]

// 示例 2：危险的版本，会在 .ToArray() 处抛出异常
string[] data = { "10", "oops", "30" };
// var nums = data.Select(d => int.Parse(d)).ToArray();
// 遇到 "oops" 时抛出 FormatException！

// 示例 3：先过滤再解析的做法
string[] scores = { "85", "", "92", "abc", "77" };
int[] validScores = scores
    .Where(s => int.TryParse(s, out _))
    .Select(s => int.Parse(s))
    .ToArray();
// 结果：[85, 92, 77]
```

### 为什么不直接用 Try-Catch 包裹？

你*可以*用 `try-catch` 包裹整个枚举过程，但这只能捕获**第一个**失败并会中止整个管道。
你会丢失所有剩余的有效数据。
`TryParse` 模式允许你处理*每一个*元素并仅跳过无效项，这对于现实世界中的数据处理来说是一种更具弹性的方法。

### 常见模式

| 模式 | 优点 | 缺点 |
| --- | --- | --- |
| 在 `Select` 中配合可空类型使用 `TryParse` | 单次遍历，无多余解析 | 稍显冗长 |
| 在 `Where` 中使用 `TryParse` 然后在 `Select` 中使用 `Parse` | 可读性极高 | 有效字符串会被解析两次 |
| 围绕枚举使用 `try-catch` | 对于单个失败处理很简单 | 遇到第一个错误即中止，丢失剩余数据 |

### 你的任务

编写一个方法，接收一个字符串数组并安全地将每个字符串解析为整数。
无效字符串（非数字、空字符串、null、空白字符）应被**静默跳过**，不应抛出任何异常。
仅返回成功解析的整数，并**按升序排序**，结果类型为 `int[]`。

### 方法签名

```csharp
public static int[] SafeParse(string[] values)
```

### 预期结果

```css
SafeParse(["1", "abc", "3", "", "5", "xyz", "7"]) -> [1, 3, 5, 7]
SafeParse(["10", "20", "30"]) -> [10, 20, 30]
SafeParse(["nope", "nada", ""]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] SafeParse(string[] values)
    {
        // 用 TryParse 配合可空投影，无效字符串变成 null 后被过滤掉，不会抛出异常
        return values
            .Select(v => int.TryParse(v, out int n) ? (int?)n : null)
            .Where(x => x.HasValue)
            .Select(x => x.Value)
            .OrderBy(x => x)
            .ToArray();
    }
}
```
