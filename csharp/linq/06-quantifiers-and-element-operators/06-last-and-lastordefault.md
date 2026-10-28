### LINQ 中的 Last 和 LastOrDefault

你已经熟悉了 `First` 和 `FirstOrDefault`，它们用于获取满足条件的第一项元素（或整个序列的第一项元素）。
LINQ 提供了名为 `Last` 和 `LastOrDefault` 的镜像方法，它们执行相同的操作，但从序列的逻辑末尾向前扫描。
当你需要日志中的最新记录、排序列表中的最后一个匹配项或时间序列中的收盘价时，这些方法至关重要。

### 工作原理

`Last()` 返回序列的最后一个元素，或者满足 predicate 的最后一个元素。
如果未找到任何元素，它会抛出 `InvalidOperationException`。
`LastOrDefault()` 的行为完全相同，不同之处在于当没有匹配项时，它不会抛出异常，而是返回该类型的默认值（`int` 为 `0`，引用类型为 `null`，`bool` 为 `false`）。

**性能提示：** 在诸如数组和 `List<T>` 等支持索引的集合上，不带 predicate 的 `Last()` 时间复杂度为 **O(1)**：运行时可以直接跳转到最后一个索引。
但是，当你提供了 predicate，或者数据源是只进迭代器（例如使用 `yield return` 的方法）时，LINQ 必须遍历整个序列以找到最后一个匹配项。
在处理大型数据集或开销较大的枚举时，请牢记这一点。

### 语法

```csharp
// 不带 predicate - 获取最后一个元素
TSource last = sequence.Last();
TSource lastOrDef = sequence.LastOrDefault();

// 带 predicate - 获取满足条件的最后一个元素
TSource last = sequence.Last(element => condition);
TSource lastOrDef = sequence.LastOrDefault(element => condition);
```

### 示例

```csharp
string[] cities = { "Berlin", "Tokyo", "Boston", "Toronto" };

// 整个序列的最后一个元素
string lastCity = cities.Last();  // "Toronto"

// 最后一个以 'B' 开头的城市
string lastB = cities.Last(c => c.StartsWith("B"));  // "Boston"

// 最后一个以 'Z' 开头的城市 - 会抛出异常！
// string boom = cities.Last(c => c.StartsWith("Z"));

// 安全版本 - 返回 null（string 的默认值）
string safe = cities.LastOrDefault(c => c.StartsWith("Z"));  // null

// 用于整数
int[] scores = { 88, 72, 95, 60, 85 };
int lastAbove90 = scores.LastOrDefault(s => s > 90);  // 95
int lastAbove100 = scores.LastOrDefault(s => s > 100); // 0（int 的默认值）
```

### Last 与 LastOrDefault - 何时使用哪一个

| 方法 | 未找到匹配项 | 适用场景... |
| --- | --- | --- |
| `Last()` | 抛出 `InvalidOperationException` | 确信一定存在匹配项 |
| `Last(predicate)` | 抛出 `InvalidOperationException` | 缺少匹配项属于 bug |
| `LastOrDefault()` | 返回 `default(T)` | 空序列是合法的 |
| `LastOrDefault(predicate)` | 返回 `default(T)` | 没有匹配项属于预期情况 |

### 你的任务

编写一个方法，接收一个整数数组并返回该数组中的**最后一个偶数**。
如果不存在偶数，则返回 `0`。

思考一下：鉴于在没有匹配项时需要返回 `0` 的要求，使用 `Last` 还是 `LastOrDefault` 变体更合适，以及如何将“是偶数”表示为一个 predicate。

### 方法签名

```csharp
public static int LastEven(int[] numbers)
```

### 预期结果

```scss
LastEven([1, 3, 5, 4, 6, 7]) -> 6
LastEven([1, 3, 5, 7]) -> 0
LastEven([2]) -> 2
LastEven([10, 20, 30]) -> 30
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int LastEven(int[] numbers)
    {
        // 返回最后一个偶数，没有匹配项时返回 int 的默认值 0
        return numbers.LastOrDefault(n => n % 2 == 0);
    }
}
```
