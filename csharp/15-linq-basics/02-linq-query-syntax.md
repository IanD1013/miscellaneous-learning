### LINQ 查询语法

LINQ 查询语法在 C# 中提供了一种类似 SQL 的查询编写方式，使复杂的数据转换更具可读性。

### 方法语法 vs 查询语法

```csharp
// 方法语法（流式）
var result = numbers.Where(n => n > 5).Select(n => n * 2);

// 查询语法（声明式）
var result = from n in numbers
             where n > 5
             select n * 2;
```

两者生成的结果完全相同 - 根据可读性进行选择！

### 查询语法结构

```csharp
// 基本结构：
from [variable] in [collection]
where [condition]        // 可选：过滤元素
select [expression]      // 必需：要返回的内容

// 示例：获取成年人的名字
var adultNames = from person in people
                 where person.Age >= 18
                 select person.Name;
```

### 关键子句

| 子句 | 作用 | 示例 |
| --- | --- | --- |
| `from` | 声明范围变量 | `from n in numbers` |
| `where` | 过滤元素 | `where n > 0` |
| `select` | 投影/转换 | `select n * 2` |

### 你的任务

将以下方法语法查询转换为查询语法：

```csharp
numbers.Where(n => n % 2 == 0).Select(n => n * 2).ToList()
```

此查询用于过滤出偶数并将其翻倍。

### 方法签名

```csharp
public static List<int> GetEvenNumbersDoubled(List<int> numbers)
```

### 预期结果

```
GetEvenNumbersDoubled([1, 2, 3, 4, 5, 6]) -> [4, 8, 12]
GetEvenNumbersDoubled([2, 4, 6]) -> [4, 8, 12]
GetEvenNumbersDoubled([1, 3, 5]) -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    // 这是方法语法版本：
    // numbers.Where(n => n % 2 == 0).Select(n => n * 2).ToList()
    //
    // 你的任务：使用 LINQ 查询语法重写它
    public static List<int> GetEvenNumbersDoubled(List<int> numbers)
    {
        // 使用查询语法：from ... where ... select ...
        var result = from n in numbers
                     where n % 2 == 0
                     select n * 2;

        return result.ToList();
    }
}
```
