### 添加和访问 Dictionary 项

Dictionaries 存储键值对并提供快速查找功能。
使用 `Add()` 插入项，使用索引器 `[]` 根据键检索值。

### 使用 Add() 添加项

```csharp
Dictionary<string, int> ages = new Dictionary<string, int>();

// 添加键值对
ages.Add("Alice", 25);
ages.Add("Bob", 30);
ages.Add("Charlie", 35);
```

### 使用索引器访问值

```csharp
// 使用键检索值
int aliceAge = ages["Alice"];  // 返回 25
int bobAge = ages["Bob"];      // 返回 30

// 警告：如果键不存在，会抛出 KeyNotFoundException
// int unknown = ages["Unknown"];  // 异常！
```

### 用于添加项时的 Add() 与索引器对比

```csharp
// 如果键已存在，Add() 会抛出异常
ages.Add("Alice", 26);  // 异常！键已存在

// 索引器既可以添加也可以更新
ages["Alice"] = 26;     // 更新已有的键
ages["David"] = 40;     // 添加新键
```

### 你的任务

创建一个将水果名称映射到其颜色的 dictionary，使用 `Add()` 添加指定的项，然后返回所请求水果的颜色。

添加这些水果-颜色对：

- "apple" → "red"
- "banana" → "yellow"
- "grape" → "purple"

### 方法签名

```csharp
public static string BuildAndRetrieve(string keyToRetrieve)
```

### 预期结果

```
BuildAndRetrieve("apple") -> "red"
BuildAndRetrieve("banana") -> "yellow"
BuildAndRetrieve("grape") -> "purple"
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static string BuildAndRetrieve(string keyToRetrieve)
    {
        // 创建一个存储水果颜色的字典
        Dictionary<string, string> fruitColors = new Dictionary<string, string>();

        // 使用 Add() 添加水果-颜色对
        fruitColors.Add("apple", "red");
        fruitColors.Add("banana", "yellow");
        fruitColors.Add("grape", "purple");

        // 返回给定键对应的值
        return fruitColors[keyToRetrieve];
    }
}
```
