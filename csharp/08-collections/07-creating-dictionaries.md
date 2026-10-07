### C# 中的 Dictionary

`Dictionary<TKey, TValue>` 用于存储键值对，其中每个键都是唯一的，并精确映射到一个值。
当你需要通过特定键查找值时，请使用字典。

### 声明与初始化

```csharp
// 空字典
Dictionary<string, int> scores = new Dictionary<string, int>();

// 带初始值的字典（集合初始化器）
Dictionary<string, int> ages = new Dictionary<string, int>
{
    { "Alice", 25 },
    { "Bob", 30 }
};

// 另一种语法（C# 6+）
Dictionary<string, int> prices = new Dictionary<string, int>
{
    ["Apple"] = 1,
    ["Banana"] = 2
};
```

### Dictionary 与 List 的对比

| 特性 | List<T> | Dictionary<TKey, TValue> |
| --- | --- | --- |
| 访问方式 | 索引 (0, 1, 2...) | 键 (任意类型) |
| 查找速度 | O(n) - 必须按值搜索 | O(1) - 通过键即时查找 |
| 重复项 | 允许 | 键必须唯一 |
| 使用场景 | 有序集合 | 键值映射 |

### 常见的键/值类型

```csharp
Dictionary<string, string> capitals;    // 国家 -> 首都
Dictionary<int, string> idToName;       // ID -> 名字
Dictionary<string, double> productPrices; // 产品 -> 价格
```

### 你的任务

创建一个将人名映射到年龄的字典，包含以下确切条目：

- "Alice" → 25
- "Bob" → 30
- "Charlie" → 35

### 方法签名

```csharp
public static Dictionary<string, int> CreateAgeDictionary()
```

### 预期结果

```
CreateAgeDictionary()["Alice"] -> 25
CreateAgeDictionary()["Bob"] -> 30
CreateAgeDictionary()["Charlie"] -> 35
CreateAgeDictionary().Count -> 3
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static Dictionary<string, int> CreateAgeDictionary()
    {
        // 使用集合初始化器创建人名到年龄的映射
        return new Dictionary<string, int>
        {
            { "Alice", 25 },
            { "Bob", 30 },
            { "Charlie", 35 }
        };
    }
}
```
