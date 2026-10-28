### LINQ Reverse 操作符

LINQ 中的 `Reverse()` 操作符按与序列最初出现时**相反的顺序**产出元素。
每当你需要颠倒元素的现有排列时，它都非常有用，例如，优先显示最近添加的项目，或者在不重新排序的情况下撤销先前的排序。

### 工作原理

`Reverse()` 是一个**延迟**（deferred）操作，这意味着直到你迭代结果时它才会执行。
然而，与许多一次流式传输一个元素的 LINQ 操作符不同，`Reverse()` 在开始产出元素之前必须在**内部缓冲整个源序列**（因为它需要先知道最后一个元素）。
这意味着它具有 O(n) 的内存开销。

### Reverse 与 OrderByDescending

一个常见的混淆点是 `Reverse()` 和 `OrderByDescending()` 之间的区别：

| 操作符 | 作用 | 示例 |
| --- | --- | --- |
| `Reverse()` | 颠倒**现有顺序**：第一个变为最后一个，最后一个变为第一个 | `[3, 1, 4]` → `[4, 1, 3]` |
| `OrderByDescending()` | 按键降序**排序**元素 | `[3, 1, 4]` → `[4, 3, 1]` |

注意它们之间的区别：`Reverse()` 保留相对关系并仅对其进行镜像反转，而 `OrderByDescending()` 则根据元素的值重新排列元素。

### 语法

```csharp
// 反转整个序列
IEnumerable<T> reversed = source.Reverse();

// 通常链接在其他 LINQ 操作之后
var result = source.Where(predicate).Reverse();
```

### 示例

```csharp
// 示例 1：反转一个字符串序列
string[] cities = { "Tokyo", "Berlin", "Cairo", "Lima" };
var reversed = cities.Reverse();
// 结果：["Lima", "Cairo", "Berlin", "Tokyo"]

// 示例 2：先过滤再反转 - 操作顺序很重要！
int[] scores = { 85, 42, 91, 33, 78 };
var highScoresReversed = scores.Where(s => s >= 70).Reverse();
// 过滤后：[85, 91, 78] → 反转后：[78, 91, 85]

// 示例 3：Reverse 与 OrderByDescending 对比
int[] data = { 10, 30, 20 };
var flipped = data.Reverse();              // [20, 30, 10] - 镜像
var sorted = data.OrderByDescending(x => x); // [30, 20, 10] - 从高到低排序
```

### 你的任务

编写一个方法，接收一个整数数组，仅过滤出其中的**偶数**（保留它们在输入中的原始顺序），然后**反转**该过滤后的序列。
将结果作为 `int[]` 返回。

例如，给定 `[1, 2, 3, 4, 5, 6]`，按顺序排列的偶数为 `[2, 4, 6]`。
反转后得到 `[6, 4, 2]`。

### 方法签名

```csharp
public static int[] ReverseEvenNumbers(int[] numbers)
```

### 预期结果

```scss
ReverseEvenNumbers([1, 2, 3, 4, 5, 6]) -> [6, 4, 2]
ReverseEvenNumbers([10, 15, 20, 25, 30]) -> [30, 20, 10]
ReverseEvenNumbers([1, 3, 5]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ReverseEvenNumbers(int[] numbers)
    {
        return numbers
            .Where(n => n % 2 == 0)   // 只保留偶数，顺序不变
            .Reverse()                // 反转过滤后的序列
            .ToArray();
    }
}
```
