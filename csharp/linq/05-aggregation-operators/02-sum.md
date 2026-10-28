### LINQ Sum 运算符

在处理数据集合时，最常见的操作之一就是计算总和。
LINQ 的 `Sum` 运算符将序列中的所有数值聚合为一个单独的结果。
它有两种形式：一种直接作用于数值序列，另一种接受一个**选择器函数**（selector function）以在求和前对每个元素进行投影变换。

### 工作原理

`Sum()` 最简单的形式直接作用于数字序列：`int[]`、`List<double>`、`IEnumerable<decimal>` 等。
它遍历每个元素并累加得到总和。

更强大的形式 `Sum(selector)` 接受一个 Lambda 表达式，在将每个元素累加到总和之前先将其转换为数值。
这等同于链式调用 `.Select(selector).Sum()`，但更加简洁且富有表现力。
当你需要从每个元素中计算出一个值而不是直接对元素本身求和时，选择器方法尤其有用。

### 语法

```csharp
// 直接对数值序列求和
int total = numbers.Sum();

// 带选择器的 Sum - 先转换每个元素，再求和
int total = collection.Sum(element => someNumericExpression);
```

### 示例

```csharp
// 示例 1：直接对整数求和
int[] prices = { 10, 25, 40, 5 };
int totalPrice = prices.Sum(); // 80

// 示例 2：带选择器的 Sum - 字符串长度总和
sstring[] words = { "cat", "elephant", "go" };
int totalLength = words.Sum(w => w.Length); // 13

// 示例 3：带选择器的 Sum - 求和前将每个值翻倍
int[] values = { 3, 7, 2 };
int doubledSum = values.Sum(v => v * 2); // 24
// 等价于：values.Select(v => v * 2).Sum()

// 示例 4：对对象的某个属性求和
// 给定一个带有 Amount 属性的订单列表：
// orders.Sum(o => o.Amount)  - 计算所有订单金额的总和
```

### 常见模式

| 模式 | 示例 | 描述 |
| --- | --- | --- |
| 直接求和 | `nums.Sum()` | 按原样对元素求和 |
| 属性求和 | `items.Sum(x => x.Price)` | 对特定属性求和 |
| 计算求和 | `nums.Sum(x => x * x)` | 对计算后的值求和 |
| 条件求和 | `nums.Where(x => x > 0).Sum()` | 仅对匹配的元素求和 |

### 你的任务

编写一个方法，接受一个整数数组并返回**每个元素的平方和**。
例如，给定数组 `[1, 2, 3, 4]`，你需要计算 `1² + 2² + 3² + 4² = 1 + 4 + 9 + 16 = 30`。

使用带有选择器的 `Sum` 运算符，用一个简洁的表达式完成此操作。

### 方法签名

```csharp
public static int SumOfSquares(int[] numbers)
```

### 预期结果

```scss
SumOfSquares([1, 2, 3, 4]) -> 30
SumOfSquares([5]) -> 25
SumOfSquares([]) -> 0
SumOfSquares([0, 0, 0]) -> 0
SumOfSquares([-3, 4]) -> 25
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int SumOfSquares(int[] numbers)
    {
        // 使用带选择器的 Sum，先求每个元素的平方再求和
        return numbers.Sum(n => n * n);
    }
}
```
