### LINQ 简介

LINQ（Language Integrated Query）是 C# 中一个强大的功能，它允许你使用一致、可读性高的语法来查询和操作集合。
只需在代码中添加 `using System.Linq;` 即可使用。

### 方法语法基础

LINQ 提供了可以链式调用到任何集合上的扩展方法。
这些方法通过点表示法进行调用：

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 获取第一个元素
int first = numbers.First();

// 获取最后一个元素
int last = numbers.Last();

// 统计元素数量
int count = numbers.Count();
```

### First() 与 FirstOrDefault()

`First()` 方法返回第一个元素，但如果集合为空，则会抛出异常。
当你希望获取默认值而不是抛出异常时，请使用 `FirstOrDefault()`：

```csharp
var empty = new List<int>();

// 这会抛出 InvalidOperationException！
int first = empty.First();

// 这会返回 0（int 的默认值）
int firstOrDefault = empty.FirstOrDefault();
```

### 常用的 LINQ 方法

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| First() | 返回第一个元素 | numbers.First() |
| Last() | 返回最后一个元素 | numbers.Last() |
| Count() | 返回元素数量 | numbers.Count() |
| Any() | 检查是否存在任何元素 | numbers.Any() |

### 你的任务

实现一个方法，使用 LINQ 返回整数列表中的第一个元素。

### 方法签名

```csharp
public static int GetFirstElement(List<int> numbers)
```

### 预期结果

```
GetFirstElement([1, 2, 3]) -> 1
GetFirstElement([42, 17, 99]) -> 42
GetFirstElement([5]) -> 5
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int GetFirstElement(List<int> numbers)
    {
        // 使用 LINQ 返回列表的第一个元素
        return numbers.First();
    }
}
```
