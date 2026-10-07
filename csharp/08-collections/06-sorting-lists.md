### 列表排序

`Sort()` 方法按升序（从小到大）排列列表元素。
`Reverse()` 方法反转元素的顺序。
这两个方法都会修改原始列表。

### 使用 Sort()

```csharp
List<int> numbers = new List<int> { 5, 2, 8, 1, 9 };
numbers.Sort();
// numbers 现在为 { 1, 2, 5, 8, 9 }

List<string> names = new List<string> { "Charlie", "Alice", "Bob" };
names.Sort();
// names 现在为 { "Alice", "Bob", "Charlie" }
```

### 使用 Reverse()

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
numbers.Reverse();
// numbers 现在为 { 5, 4, 3, 2, 1 }

// 结合 Sort 和 Reverse 实现降序排列
List<int> scores = new List<int> { 50, 90, 30 };
scores.Sort();
scores.Reverse();
// scores 现在为 { 90, 50, 30 }
```

### 关键要点

| 方法 | 效果 | 返回值 |
| --- | --- | --- |
| `Sort()` | 按升序排列 | void（修改列表） |
| `Reverse()` | 反转元素顺序 | void（修改列表） |

### 你的任务

编写一个方法，接收一个整数列表并返回按升序（从小到大）排序后的列表。

### 方法签名

```csharp
public static List<int> SortAscending(List<int> numbers)
```

### 预期结果

```
SortAscending([5, 2, 8, 1, 9]) -> [1, 2, 5, 8, 9]
SortAscending([3, 1, 2]) -> [1, 2, 3]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static List<int> SortAscending(List<int> numbers)
    {
        // 按升序排列列表
        numbers.Sort();
        return numbers;
    }
}
```
