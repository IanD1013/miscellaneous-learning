### LINQ `All` 量词

在实际应用中，你经常需要在继续操作之前验证集合中的**每个**元素是否都满足特定条件，例如，在批量发货前确认所有订单都已付款，或者在启动服务前确保每个配置值都有效。
LINQ 的 `All` 方法正是为此类全称检查量身定制的。

### 工作原理

`All` 接收一个谓词（返回 `bool` 的函数）并针对序列中的每个元素对其求值。
如果**每个**元素都满足该谓词，`All` 将返回 `true`。
一旦遇到**不满足**谓词的元素，它就会**短路（short-circuit）**：立即返回 `false`，而不再检查剩余元素。
这使得它在不满足条件的元素出现在较早位置的大型集合中非常高效。

需要理解的一个重要行为是**空真（vacuous truth）**：当在**空**序列上调用 `All` 时，它会返回 `true`。
这符合数学逻辑：如果没有元素，那么就没有元素违反条件，因此“所有元素都满足谓词”这一陈述显然成立。

### 语法

```csharp
bool result = collection.All(element => condition);
```

谓词是一个 lambda 表达式，接收每个元素并返回 `true` 或 `false`。

### 示例

```csharp
// 检查是否所有学生都及格（分数 >= 60）
int[] scores = { 85, 72, 91, 66 };
bool allPassed = scores.All(s => s >= 60);  // true - 每个分数都在 60 分或以上

// 检查是否所有字符串均非空
string[] words = { "hello", "", "world" };
bool allNonEmpty = words.All(w => w.Length > 0);  // false - 在 "" 处短路

// 空集合的空真性
int[] empty = { };
bool result = empty.All(x => x < 0);  // true - 没有元素违反该条件

// 检查是否所有温度都在冰点以下
double[] temps = { -5.0, -12.3, -0.1 };
bool allFreezing = temps.All(t => t < 0.0);  // true
```

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 范围检查 | `items.All(x => x >= min && x <= max)` |
| Null/空值防范 | `names.All(n => !string.IsNullOrEmpty(n))` |
| 类型检查 | `objects.All(o => o is SomeType)` |
| 属性验证 | `orders.All(o => o.Total > 0)` |

### 你的任务

编写一个方法，判断给定数组中的**每个**数字是否都为**严格正数**（大于零）。
使用 LINQ 的 `All` 方法来执行检查。

- 零**不**被视为正数。
- 空数组应返回 `true`（不存在非正数来违反条件）。

### 方法签名

```csharp
public static bool AllPositive(int[] numbers)
```

### 预期结果

```scss
AllPositive([1, 2, 3])        -> True
AllPositive([1, -2, 3])       -> False
AllPositive([])               -> True
AllPositive([0, 1, 2])        -> False
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static bool AllPositive(int[] numbers)
    {
        // 每个元素都必须严格大于 0，空数组按空真返回 true
        return numbers.All(n => n > 0);
    }
}
```
