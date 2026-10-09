### Any 和 All 布尔检查

`Any()` 和 `All()` 是 LINQ 方法，它们根据集合中的条件返回布尔值结果。
它们非常适合用于验证和快速检查。

### Any() 方法

如果**至少有一个元素**满足条件，`Any()` 将返回 `true`。

```csharp
var numbers = new List<int> { 1, 2, -3, 4 };

// 检查是否有任何元素满足条件
bool hasNegative = numbers.Any(n => n < 0);  // true
bool hasZero = numbers.Any(n => n == 0);     // false

// 不带谓词的 Any() 检查集合是否非空
bool hasElements = numbers.Any();            // true
```

### All() 方法

只有当**每个元素**都满足条件时，`All()` 才会返回 `true`。

```csharp
var scores = new List<int> { 75, 82, 90, 68 };

// 检查是否所有元素都满足条件
bool allPassing = scores.All(s => s >= 60);  // true
bool allExcellent = scores.All(s => s >= 80); // false
```

### 主要区别

| 方法 | 何时返回 True | 空集合 |
| --- | --- | --- |
| `Any(predicate)` | 至少有一个匹配 | `false` |
| `All(predicate)` | 每个元素都匹配 | `true` |

```csharp
var empty = new List<int>();
empty.Any(n => n > 0);  // false - 没有可匹配的元素
empty.All(n => n > 0);  // true - 空真（vacuously true，没有元素不满足条件）
```

### 短路求值

这两种方法一旦确定结果就会立即停止处理：

- `Any()` 在遇到第一个 `true` 结果时停止
- `All()` 在遇到第一个 `false` 结果时停止

### 你的任务

实现两个方法：

1. **HasAnyNegative**：如果列表中的任何数字为负数（小于 0），则返回 `true`
2. **AreAllPositive**：如果所有数字都为正数（大于 0），则返回 `true`

### 方法签名

```csharp
public static bool HasAnyNegative(List<int> numbers)
public static bool AreAllPositive(List<int> numbers)
```

### 预期结果

```
HasAnyNegative([1, 2, -3, 4]) -> True
HasAnyNegative([1, 2, 3, 4]) -> False
AreAllPositive([1, 2, 3, 4]) -> True
AreAllPositive([1, 0, 3, 4]) -> False
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static bool HasAnyNegative(List<int> numbers)
    {
        // 检查是否有任何数字为负数
        return numbers.Any(n => n < 0);
    }
    
    public static bool AreAllPositive(List<int> numbers)
    {
        // 检查是否所有数字都为正数（大于 0）
        return numbers.All(n => n > 0);
    }
}
```
