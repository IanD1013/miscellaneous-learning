### 从列表中移除元素

列表允许你在不再需要某些元素时将其移除。
C# 提供了两种主要方法：按值移除的 `Remove()`，以及按索引位置移除的 `RemoveAt()`。

### Remove() 方法

```csharp
List<string> fruits = new List<string> { "apple", "banana", "cherry" };

// 按值移除 - 移除第一个匹配项
fruits.Remove("banana");  // 列表现在为：["apple", "cherry"]

// 如果找到并移除了该元素则返回 true，否则返回 false
bool wasRemoved = fruits.Remove("mango");  // 返回 false（不在列表中）
```

### RemoveAt() 方法

```csharp
List<string> colors = new List<string> { "red", "green", "blue" };

// 按索引位置移除
colors.RemoveAt(0);  // 移除 "red"，列表现在为：["green", "blue"]
colors.RemoveAt(1);  // 移除 "blue"，列表现在为：["green"]

// 小心！如果索引超出范围会抛出异常
```

### Remove() 与 RemoveAt()

| 方法 | 移除方式 | 返回值 | 未找到时 |
| --- | --- | --- | --- |
| `Remove(item)` | 值 | `bool` | 返回 `false` |
| `RemoveAt(index)` | 索引 | `void` | 抛出异常 |

### 重要特性

```csharp
List<int> numbers = new List<int> { 1, 2, 2, 3 };
numbers.Remove(2);  // 只移除第一个匹配项
// 列表现在为：[1, 2, 3] - 第二个 2 仍然存在
```

### 你的任务

编写一个方法，从字符串列表中移除指定元素并返回修改后的列表。
使用 `Remove()` 方法按值移除该元素。

### 方法签名

```csharp
public static List<string> RemoveItem(List<string> items, string itemToRemove)
```

### 预期结果

```
RemoveItem(["apple", "banana", "cherry"], "banana") -> ["apple", "cherry"]
RemoveItem(["red", "green", "blue"], "red") -> ["green", "blue"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static List<string> RemoveItem(List<string> items, string itemToRemove)
    {
        // 按值移除该元素（不存在时列表保持不变）
        items.Remove(itemToRemove);
        return items;
    }
}
```
