### Average、Min 和 Max 聚合方法

`Average()`、`Min()` 和 `Max()` 是 LINQ 聚合方法，用于计算集合中的统计值。
它们对于分析数值数据至关重要。

### Average()

返回集合中所有元素的算术平均值。

```csharp
var numbers = new List<int> { 10, 20, 30 };
double avg = numbers.Average(); // 20.0

var prices = new List<double> { 9.99, 19.99, 29.99 };
double avgPrice = prices.Average(); // 19.99
```

### Min() 和 Max()

返回集合中的最小值和最大值。

```csharp
var scores = new List<int> { 85, 92, 78, 95, 88 };
int lowest = scores.Min();   // 78
int highest = scores.Max();  // 95

var temps = new List<double> { -5.2, 12.8, 3.1 };
double coldest = temps.Min();  // -5.2
double warmest = temps.Max();  // 12.8
```

### 与 Select 结合使用

你可以将这些方法与 `Select()` 结合使用来处理特定属性：

```csharp
var students = new List<Student> { ... };
double avgAge = students.Select(s => s.Age).Average();
int youngestAge = students.Select(s => s.Age).Min();
```

### 重要提示

- 如果集合为空，这些方法会抛出 `InvalidOperationException`
- 对于整数集合，`Average()` 返回 `double`
- 对于可空类型，使用 `Average()`、`Min()`、`Max()` 时会忽略 null 值

### 你的任务

实现三个方法来分析考试成绩列表：

1. `GetAverageScore` - 返回所有成绩的平均值
2. `GetMinimumScore` - 返回最低分
3. `GetMaximumScore` - 返回最高分

### 方法签名

```csharp
public static double GetAverageScore(List<int> scores)
public static int GetMinimumScore(List<int> scores)
public static int GetMaximumScore(List<int> scores)
```

### 预期结果

```
GetAverageScore([85, 92, 78, 95, 88]) -> 87.6
GetMinimumScore([85, 92, 78, 95, 88]) -> 78
GetMaximumScore([85, 92, 78, 95, 88]) -> 95
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static double GetAverageScore(List<int> scores)
    {
        // 返回所有成绩的平均值
        return scores.Average();
    }

    public static int GetMinimumScore(List<int> scores)
    {
        // 返回最低分
        return scores.Min();
    }

    public static int GetMaximumScore(List<int> scores)
    {
        // 返回最高分
        return scores.Max();
    }
}
```
