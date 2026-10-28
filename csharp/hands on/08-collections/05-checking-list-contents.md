### 检查列表内容

有两个基本方法可以帮助你在列表中搜索元素：`Contains()` 检查元素是否存在，而 `IndexOf()` 则告诉你它所在的位置。

### 使用 Contains()

`Contains()` 返回一个布尔值，指示该元素是否存在于列表中。

```csharp
List<string> fruits = new List<string> { "apple", "banana", "orange" };

bool hasApple = fruits.Contains("apple");    // True
bool hasGrape = fruits.Contains("grape");    // False

if (fruits.Contains("banana"))
{
    Console.WriteLine("We have bananas!");
}
```

### 使用 IndexOf()

`IndexOf()` 返回元素首次出现时从零开始的索引，如果未找到则返回 `-1`。

```csharp
List<string> colors = new List<string> { "red", "green", "blue", "green" };

int redIndex = colors.IndexOf("red");      // 0
int greenIndex = colors.IndexOf("green");  // 1（首次出现）
int yellowIndex = colors.IndexOf("yellow"); // -1（未找到）
```

### 结合使用这两个方法

你可以使用 `Contains()` 进行快速的存在性检查，然后使用 `IndexOf()` 获取位置。

```csharp
List<string> names = new List<string> { "Alice", "Bob", "Charlie" };

if (names.Contains("Bob"))
{
    int position = names.IndexOf("Bob");
    Console.WriteLine($"Bob is at position {position}");
}
```

### 你的任务

编写一个在列表中搜索元素的方法。
如果该元素存在，返回 `"Found at index X"`，其中 X 是该元素的位置。
如果该元素不存在，返回 `"Not found"`。

### 方法签名

```csharp
public static string FindItem(List<string> items, string searchItem)
```

### 预期结果

```
FindItem(["apple", "banana", "cherry"], "banana") -> "Found at index 1"
FindItem(["apple", "banana", "cherry"], "grape") -> "Not found"
FindItem(["cat"], "cat") -> "Found at index 0"
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static string FindItem(List<string> items, string searchItem)
    {
        // 先检查元素是否存在，再获取它的位置
        if (items.Contains(searchItem))
        {
            return $"Found at index {items.IndexOf(searchItem)}";
        }

        return "Not found";
    }
}
```
