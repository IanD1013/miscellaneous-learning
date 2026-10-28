### 使用 foreach 遍历字典

`foreach` 循环结合 `KeyValuePair<TKey, TValue>` 让你可以遍历字典中的所有条目，同时访问键和值。

### KeyValuePair 基础

```csharp
Dictionary<string, int> ages = new Dictionary<string, int>
{
    { "Alice", 25 },
    { "Bob", 30 }
};

foreach (KeyValuePair<string, int> pair in ages)
{
    Console.WriteLine(pair.Key);   // 先 "Alice"，然后 "Bob"
    Console.WriteLine(pair.Value); // 先 25，然后 30
}
```

### 使用 var 使代码更简洁

```csharp
// 可以使用 var 来避免写出完整的泛型类型
foreach (var pair in ages)
{
    Console.WriteLine($"{pair.Key} is {pair.Value} years old");
}
```

### 另一种方式：解构（C# 7+）

```csharp
// 直接解构为 key 和 value 变量
foreach (var (name, age) in ages)
{
    Console.WriteLine($"{name}: {age}");
}
```

### KeyValuePair 属性

| 属性 | 说明 | 示例 |
| --- | --- | --- |
| `Key` | 获取条目的键 | `pair.Key` |
| `Value` | 获取条目的值 | `pair.Value` |

### 你的任务

编写一个方法，接收一个 `Dictionary<string, int>`，并按 `Key: Value` 的格式将每个键值对分别打印在单独的一行上。

### 方法签名

```csharp
public static void PrintDictionary(Dictionary<string, int> dictionary)
```

### 预期结果

```
For { "apple": 5, "banana": 3 }:
apple: 5
banana: 3

For { "x": 10 }:
x: 10
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static void PrintDictionary(Dictionary<string, int> dictionary)
    {
        // 遍历每个键值对，按 Key: Value 格式打印
        foreach (var pair in dictionary)
        {
            Console.WriteLine($"{pair.Key}: {pair.Value}");
        }
    }
}
```
