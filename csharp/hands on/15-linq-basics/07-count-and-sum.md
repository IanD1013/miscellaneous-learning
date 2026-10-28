### Count 和 Sum 聚合方法

`Count()` 和 `Sum()` 是 LINQ 聚合方法，用于将集合规约为单个值。
它们对于从数据中计算总和与数量至关重要。

### Count() 方法

`Count()` 返回集合中的元素数量。
它可以带谓词使用，也可以不带谓词使用。

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 统计所有元素
int total = numbers.Count();           // 返回 5

// 统计满足条件的元素
int evens = numbers.Count(n => n % 2 == 0);  // 返回 2
```

### Sum() 方法

`Sum()` 将集合中的所有数值相加。
它可以直接作用于数值类型，也可以使用选择器（selector）。

```csharp
var numbers = new List<int> { 10, 20, 30 };

// 对所有元素求和
int total = numbers.Sum();              // 返回 60

// 使用选择器求和（先转换再求和）
int doubled = numbers.Sum(n => n * 2);  // 返回 120
```

### 与 Where 结合使用

你可以先进行筛选，然后再进行聚合：

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// 只对奇数求和
int oddSum = numbers.Where(n => n % 2 != 0).Sum();  // 返回 9
```

### 快速参考

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `Count()` | 计算所有元素的数量 | `list.Count()` |
| `Count(predicate)` | 计算匹配元素的数量 | `list.Count(x => x > 0)` |
| `Sum()` | 计算所有元素的总和 | `list.Sum()` |
| `Sum(selector)` | 计算转换后值的总和 | `list.Sum(x => x * 2)` |

### 你的任务

实现两个方法：

1. **CountPositiveNumbers**：计算有多少个大于零的数字
2. **SumEvenNumbers**：计算列表中所有偶数的总和

### 方法签名

```csharp
public static int CountPositiveNumbers(List<int> numbers)
public static int SumEvenNumbers(List<int> numbers)
```

### 预期结果

```
CountPositiveNumbers([1, -2, 3, -4, 5]) -> 3
CountPositiveNumbers([-1, -2, -3]) -> 0
SumEvenNumbers([1, 2, 3, 4, 5, 6]) -> 12
SumEvenNumbers([1, 3, 5, 7]) -> 0
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int CountPositiveNumbers(List<int> numbers)
    {
        // 使用 Count() 统计正数的个数
        return numbers.Count(n => n > 0);
    }
    
    public static int SumEvenNumbers(List<int> numbers)
    {
        // 使用 Sum() 对所有偶数求和
        return numbers.Where(n => n % 2 == 0).Sum();
    }
}
```
