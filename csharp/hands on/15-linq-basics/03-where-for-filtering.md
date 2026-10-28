### Where 方法

`Where()` 是最常用的 LINQ 方法之一。
它根据条件（谓词 predicate）过滤集合，并仅返回匹配的元素。

### 基本用法

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// 过滤出大于 3 的数字
var result = numbers.Where(n => n > 3);
// 结果：{ 4, 5, 6 }

// 过滤出奇数
var oddNumbers = numbers.Where(n => n % 2 != 0);
// 结果：{ 1, 3, 5 }
```

### 理解谓词（Predicates）

谓词是一个接收元素并返回 `true` 或 `false` 的函数。
`Where()` 方法会保留谓词返回 `true` 的元素。

```csharp
// lambda 表达式就是谓词
numbers.Where(n => n % 2 == 0)  // n => n % 2 == 0 对偶数返回 true

// 你也可以使用单独的方法作为谓词
bool IsEven(int n) => n % 2 == 0;
numbers.Where(IsEven);
```

### 延迟执行（Deferred Execution）

`Where()` 采用延迟执行，这意味着在您遍历结果或将其转换为具体类型之前，过滤操作不会实际发生。

```csharp
var query = numbers.Where(n => n > 3);  // 尚未进行过滤
var list = query.ToList();              // 过滤在这里发生
```

### 用于谓词的常用运算符

| 运算符 | 描述 | 示例 |
| --- | --- | --- |
| `%` | 取模（求余） | `n % 2 == 0`（偶数检查） |
| `==` | 等于 | `n == 5` |
| `!=` | 不等于 | `n != 0` |
| `>`, `<` | 大于/小于 | `n > 10` |
| `&&` | 逻辑与 | `n > 0 && n < 10` |
| `||` | 逻辑或 | `n < 0 || n > 100` |

### 你的任务

使用 `Where()` 方法过滤一个整数列表，并仅返回偶数。
偶数是指能被 2 整除且没有余数的数字。

### 方法签名

```csharp
public static List<int> GetEvenNumbers(List<int> numbers)
```

### 预期结果

```
GetEvenNumbers([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]
GetEvenNumbers([7, 8, 9, 10]) -> [8, 10]
GetEvenNumbers([1, 3, 5]) -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static List<int> GetEvenNumbers(List<int> numbers)
    {
        // 只保留能被 2 整除的数字
        return numbers.Where(n => n % 2 == 0).ToList();
    }
}
```
