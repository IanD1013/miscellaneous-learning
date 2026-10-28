### LINQ 单元素与聚合操作符

LINQ 提供了一系列操作符，无需手动编写循环即可快速查询序列的相关信息。
在实际开发中，你经常需要检查集合中的条件（“是否有订单超出信用额度？”）、查找极值（“最便宜的产品是什么？”）或获取边界元素（“显示最新的日志条目”）。
掌握这些操作符可以让你清晰、简洁地表达意图。

### 它们的工作原理

这些操作符分为两类：

**布尔量词（Boolean quantifiers）** 评估每个元素是否满足条件，并返回 `true` 或 `false`：

- `Any(predicate)` - 如果*至少有一个*元素满足谓词条件，则返回 `true`。
- `All(predicate)` - 仅当*所有*元素都满足谓词条件时，才返回 `true`。

**元素 / 聚合选择器（Element / aggregate selectors）** 扫描序列并返回单个值：

- `Min()` - 返回序列中的最小值。
- `Max()` - 返回序列中的最大值。
- `First()` - 返回序列中的第一个元素。
- `Last()` - 返回序列中的最后一个元素。

### 语法

```csharp
// 布尔量词
bool result = collection.Any(element => condition);
bool result = collection.All(element => condition);

// 聚合选择器
var smallest = collection.Min();
var largest  = collection.Max();

// 位置选择器
var head = collection.First();
var tail = collection.Last();
```

### 示例

```csharp
// 假设我们有考试成绩
int[] scores = { 88, 42, 95, 73, 61 };

// 是否有人不及格（成绩低于 50）？
bool anyFailed = scores.Any(s => s < 50);   // True (42 < 50)

// 是否所有人都及格了（成绩 >= 50）？
bool allPassed = scores.All(s => s >= 50);  // False (42 未及格)

// 极值是多少？
int lowest  = scores.Min();   // 42
int highest = scores.Max();   // 95

// 记录的第一个和最后一个成绩是多少？
int firstRecorded = scores.First();  // 88
int lastRecorded  = scores.Last();   // 61
```

```csharp
// 一天中的温度读数
double[] temps = { 18.5, 22.3, 27.1, 25.0, 19.8 };

bool anyFreezing = temps.Any(t => t <= 0);   // False
bool allWarm     = temps.All(t => t > 15.0); // True
double coldest   = temps.Min();              // 18.5
double hottest   = temps.Max();              // 27.1
```

### 常见模式

| 操作符 | 返回值 | 为空时是否抛出异常？ |
| --- | --- | --- |
| `Any(predicate)` | `bool` | 否 - 返回 `false` |
| `All(predicate)` | `bool` | 否 - 返回 `true`（空真/vacuous truth） |
| `Min()` | 元素类型 | 是 - `InvalidOperationException` |
| `Max()` | 元素类型 | 是 - `InvalidOperationException` |
| `First()` | 元素类型 | 是 - `InvalidOperationException` |
| `Last()` | 元素类型 | 是 - `InvalidOperationException` |

使用 `$"..."` 进行字符串插值非常适合将多个计算值组装为格式化输出。

### 你的任务

编写一个方法，对非空整数数组执行全面检查，并返回一个包含六项信息的格式化字符串：

1. **HasNeg** - 是否存在负数元素
2. **AllPos** - 是否所有元素都是严格正数（大于零）
3. **Min** - 最小元素
4. **Max** - 最大元素
5. **First** - 第一个元素
6. **Last** - 最后一个元素

输出格式必须严格为：

`HasNeg:{value}, AllPos:{value}, Min:{value}, Max:{value}, First:{value}, Last:{value}`

布尔值应显示为 `True` 或 `False`（C# 默认的 `bool.ToString()` 大小写格式）。

### 方法签名

```csharp
public static string Inspect(int[] numbers)
```

### 预期结果

```rust
Inspect([2, -1, 3, 5])    -> "HasNeg:True, AllPos:False, Min:-1, Max:5, First:2, Last:5"
Inspect([10, 20, 30])     -> "HasNeg:False, AllPos:True, Min:10, Max:30, First:10, Last:30"
Inspect([0])              -> "HasNeg:False, AllPos:False, Min:0, Max:0, First:0, Last:0"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string Inspect(int[] numbers)
    {
        // 依次使用 Any、All、Min、Max、First、Last，并用字符串插值组装输出
        return $"HasNeg:{numbers.Any(n => n < 0)}, AllPos:{numbers.All(n => n > 0)}, Min:{numbers.Min()}, Max:{numbers.Max()}, First:{numbers.First()}, Last:{numbers.Last()}";
    }
}
```
