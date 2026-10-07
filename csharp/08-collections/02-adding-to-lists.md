### 向列表中添加元素

`Add()` 方法会将单个元素追加到列表的末尾。
这是处理集合时最常见的操作之一。

### 基本用法

```csharp
List<int> numbers = new List<int>();
numbers.Add(10);    // 列表现在包含：[10]
numbers.Add(20);    // 列表现在包含：[10, 20]
numbers.Add(30);    // 列表现在包含：[10, 20, 30]
```

### 创建空列表与已初始化的列表

```csharp
// 空列表 - 之后使用 Add() 添加元素
List<string> empty = new List<string>();

// 已初始化的列表 - 创建时即提供元素
List<string> initialized = new List<string> { "A", "B", "C" };
```

### 常用方法

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| `Add(item)` | 将元素追加到末尾 | `list.Add("X")` |
| `Count` | 返回元素数量 | `list.Count` |

### 你的任务

创建一个字符串空列表，然后使用 `Add()` 方法添加三种水果："Apple"、"Banana" 和 "Cherry"。
最后，在单独的行上分别打印每个元素。

### 方法签名

```csharp
public static void AddItemsToList()
```

### 预期输出

```
Apple
Banana
Cherry
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static void AddItemsToList()
    {
        // 创建一个字符串空列表
        List<string> fruits = new List<string>();

        // 使用 Add() 添加三种水果
        fruits.Add("Apple");
        fruits.Add("Banana");
        fruits.Add("Cherry");

        // 在单独的行上分别打印每个元素
        foreach (string fruit in fruits)
        {
            Console.WriteLine(fruit);
        }
    }
}
```
