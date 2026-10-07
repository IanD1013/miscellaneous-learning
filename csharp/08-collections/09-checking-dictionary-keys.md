### 检查 Dictionary 的键

在访问字典的值之前，你需要验证该键是否存在，以避免运行时异常。
C# 提供了两种用于安全检查键的方法。

### ContainsKey()

检查键是否存在并返回一个布尔值。

```csharp
var ages = new Dictionary<string, int> { { "Alice", 25 }, { "Bob", 30 } };

bool hasAlice = ages.ContainsKey("Alice");  // true
bool hasCarol = ages.ContainsKey("Carol");  // false

// 常见模式：先检查再访问
if (ages.ContainsKey("Alice"))
{
    int age = ages["Alice"];  // 可以安全访问
}
```

### TryGetValue()

在一次操作中检查键并检索值，更加高效！

```csharp
var ages = new Dictionary<string, int> { { "Alice", 25 }, { "Bob", 30 } };

// 如果找到则返回 true，并将值放入 'age'
if (ages.TryGetValue("Alice", out int age))
{
    Console.WriteLine($"Alice is {age}");  // Alice is 25
}

// 如果未找到则返回 false，'age' 将为默认值（int 为 0）
if (ages.TryGetValue("Carol", out int carolAge))
{
    // 这里不会执行
}
```

### ContainsKey 与 TryGetValue 对比

| 方法 | 适用场景 | 查找次数 |
| --- | --- | --- |
| `ContainsKey()` | 你只需要知道键是否存在 | 1 次查找 |
| `ContainsKey()` + `[]` | 检查后需要获取该值 | 2 次查找 |
| `TryGetValue()` | 你需要检查并获取该值 | 1 次查找 |

### 你的任务

创建一个方法，安全地检查某个物品是否存在于库存字典中。
如果找到，返回 `"{item}: {quantity} in stock"`。
如果未找到，返回 `"{item}: not found"`。

### 方法签名

```csharp
public static string GetValueSafely(Dictionary<string, int> inventory, string item)
```

### 预期结果

```
GetValueSafely({"apples": 10, "bananas": 5}, "apples") -> "apples: 10 in stock"
GetValueSafely({"apples": 10, "bananas": 5}, "oranges") -> "oranges: not found"
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static string GetValueSafely(Dictionary<string, int> inventory, string item)
    {
        // 使用 TryGetValue 在一次查找中检查键并获取值
        if (inventory.TryGetValue(item, out int quantity))
        {
            return $"{item}: {quantity} in stock";
        }

        return $"{item}: not found";
    }
}
```
