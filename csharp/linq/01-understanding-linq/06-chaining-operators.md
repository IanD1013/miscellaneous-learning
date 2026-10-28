### LINQ 管道 - 链式调用操作符

LINQ 最大的优势之一是大多数操作符都会返回 `IEnumerable<T>`，这意味着你可以将它们链接成一个**管道**（pipeline）。
每个操作符接收上一个操作符的输出，并逐步转换数据。
该管道是**惰性求值**（lazy）的：在你遍历结果（例如通过调用 `.ToArray()`、`.ToList()` 或使用 `foreach`）之前，不会执行任何操作。

这种方法让你的代码保持声明式且易读：无需编写嵌套循环和临时变量，而是以一系列转换的形式来描述你*想要*什么。

### 工作原理

想象工厂中的一条装配线。
原材料从一端进入，每个工位执行单一任务：过滤掉有缺陷的零件、重塑组件、按尺寸排序、仅包装前几个零件。
LINQ 管道的工作方式与之相同：

1. **过滤**（Filter）- 移除不满足条件的元素
2. **转换**（Transform）- 将每个元素转换为新的形式
3. **排序**（Sort）- 重新排列元素
4. **截取**（Limit）- 仅获取结果的子集

每个步骤都会生成一个新的 `IEnumerable<T>`，直接输入到下一步中。

### 语法

```csharp
var result = source
    .Where(predicate)           // 过滤
    .Select(transformation)     // 转换
    .OrderBy(keySelector)       // 升序排序
    .Take(n)                    // 限制为前 n 个
    .ToArray();                 // 物化管道
```

你可以根据逻辑需要以任意顺序组合匹配任何操作符。
整个链条从上到下阅读，就像一份食谱。

### 示例

```csharp
// 示例 1：从列表中获取最长的 2 个大写名称
string[] names = { "Alice", "Bo", "Charlotte", "Dan", "Evangeline" };

var result = names
    .Where(name => name.Length > 3)         // ["Alice", "Charlotte", "Evangeline"]
    .Select(name => name.ToUpper())         // ["ALICE", "CHARLOTTE", "EVANGELINE"]
    .OrderByDescending(name => name.Length) // ["EVANGELINE", "CHARLOTTE", "ALICE"]
    .Take(2)                                // ["EVANGELINE", "CHARLOTTE"]
    .ToArray();

// 示例 2：对超过 $50 的商品应用 10% 折扣后，找出最高的 3 个价格
double[] prices = { 120.0, 30.0, 75.0, 45.0, 200.0, 60.0 };

var discounted = prices
    .Where(p => p > 50)                    // [120, 75, 200, 60]
    .Select(p => p * 0.9)                  // [108, 67.5, 180, 54]
    .OrderByDescending(p => p)             // [180, 108, 67.5, 54]
    .Take(3)                               // [180, 108, 67.5]
    .ToArray();
```

请注意每行代码是如何只做一件事的，而且管道读起来就像是对所需结果的描述。

### 关键操作符

| 操作符 | 作用 | 返回类型 |
| --- | --- | --- |
| `Where(predicate)` | 保留满足条件的元素 | `IEnumerable<T>` |
| `Select(transform)` | 将每个元素投影为新的形式 | `IEnumerable<TResult>` |
| `OrderBy(key)` | 按键升序排序 | `IOrderedEnumerable<T>` |
| `OrderByDescending(key)` | 按键降序排序 | `IOrderedEnumerable<T>` |
| `Take(n)` | 返回前 n 个元素 | `IEnumerable<T>` |
| `ToArray()` | 将管道物化为数组 | `T[]` |

### 你的任务

编写一个方法，对整数数组构建一个四步 LINQ 管道：

1. **过滤**：仅保留奇数
2. **转换**：将每个剩余的数字进行平方
3. **排序**：将平方后的值按降序排列
4. **截取**：将结果限制为前 `count` 个值

将最终结果作为 `int[]` 返回。

请记住，不能被 2 整除的数是奇数。
对一个数求平方意味着将其与自身相乘。

### 方法签名

```csharp
public static int[] TopSquaredOdds(int[] numbers, int count)
```

### 预期结果

```scss
TopSquaredOdds([1, 2, 3, 4, 5, 6, 7], 3) -> [49, 25, 9]
TopSquaredOdds([10, 20, 30], 2)           -> []
TopSquaredOdds([3, 1, 4, 1, 5], 4)       -> [25, 9, 1, 1]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] TopSquaredOdds(int[] numbers, int count)
    {
        return numbers
            .Where(n => n % 2 != 0)      // 过滤：只保留奇数
            .Select(n => n * n)          // 转换：求平方
            .OrderByDescending(n => n)   // 排序：降序
            .Take(count)                 // 截取：前 count 个
            .ToArray();
    }
}
```
