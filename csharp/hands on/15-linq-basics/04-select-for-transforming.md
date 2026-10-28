### Select 方法

`Select()` 将集合中的每个元素转换为新的形式。
可以将其视为一种“映射”（map）操作，它接收每个元素，应用转换，并返回包含转换结果的新集合。

### 基本用法

```csharp
// 将数字转换为其两倍
var numbers = new List<int> { 1, 2, 3 };
var doubled = numbers.Select(n => n * 2).ToList();
// 结果：[2, 4, 6]

// 将字符串转换为其长度
var words = new List<string> { "cat", "elephant", "dog" };
var lengths = words.Select(w => w.Length).ToList();
// 结果：[3, 8, 3]

// 转换为不同的类型
var prices = new List<int> { 10, 20, 30 };
var formatted = prices.Select(p => $"${p}.00").ToList();
// 结果：["$10.00", "$20.00", "$30.00"]
```

### Select 对比 Where

| 方法 | 作用 | 返回结果 |
| --- | --- | --- |
| `Where()` | 过滤元素 | 相同类型，更少或相同数量的元素 |
| `Select()` | 转换元素 | 可以改变类型，相同数量的元素 |

```csharp
var nums = new List<int> { 1, 2, 3, 4, 5 };

// Where：只保留满足条件的元素
var filtered = nums.Where(n => n > 3).ToList(); // [4, 5]

// Select：转换每一个元素
var transformed = nums.Select(n => n * 10).ToList(); // [10, 20, 30, 40, 50]
```

### 你的任务

编写一个方法，接收一个整数列表并返回一个包含每个数字平方的新列表。

**公式：** 平方 = 数字 × 数字（或 数字²）

### 方法签名

```csharp
public static List<int> GetSquares(List<int> numbers)
```

### 预期结果

```
GetSquares([1, 2, 3]) -> [1, 4, 9]
GetSquares([5, 10]) -> [25, 100]
GetSquares([-3, -2]) -> [9, 4]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static List<int> GetSquares(List<int> numbers)
    {
        // 将每个数字转换为它的平方
        return numbers.Select(n => n * n).ToList();
    }
}
```
