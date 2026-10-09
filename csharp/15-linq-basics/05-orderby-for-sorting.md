### 使用 OrderBy 进行排序

`OrderBy()` 根据你指定的键按升序对元素进行排序。
它是集合排序的 LINQ 等价实现，但由于你可以控制按什么排序，因此具有更高的灵活性。

### 基本用法

```csharp
var numbers = new List<int> { 5, 2, 8, 1, 9 };
var sorted = numbers.OrderBy(n => n).ToList();
// 结果：[1, 2, 5, 8, 9]

var names = new List<string> { "Charlie", "Alice", "Bob" };
var alphabetical = names.OrderBy(name => name).ToList();
// 结果：["Alice", "Bob", "Charlie"]
```

### OrderBy 与 OrderByDescending

`OrderBy()` 按升序排序（A-Z，0-9），而 `OrderByDescending()` 按降序排序（Z-A，9-0）。

```csharp
var scores = new List<int> { 85, 92, 78, 95 };

// 升序：从低到高
var ascending = scores.OrderBy(s => s).ToList();
// 结果：[78, 85, 92, 95]

// 降序：从高到低
var descending = scores.OrderByDescending(s => s).ToList();
// 结果：[95, 92, 85, 78]
```

### 按属性排序

你可以根据对象的任何属性或计算值进行排序：

```csharp
var words = new List<string> { "apple", "hi", "banana" };
var byLength = words.OrderBy(w => w.Length).ToList();
// 结果：["hi", "apple", "banana"]
```

### 你的任务

给定一个名字列表，返回按字母顺序（A 到 Z）排序后的列表。

### 方法签名

```csharp
public static List<string> SortNamesAlphabetically(List<string> names)
```

### 预期结果

```
SortNamesAlphabetically(["Charlie", "Alice", "Bob"]) -> ["Alice", "Bob", "Charlie"]
SortNamesAlphabetically(["Zara", "Anna", "Mike"]) -> ["Anna", "Mike", "Zara"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static List<string> SortNamesAlphabetically(List<string> names)
    {
        // 以名字本身作为排序键，按升序（A 到 Z）排序
        return names.OrderBy(name => name).ToList();
    }
}
```
