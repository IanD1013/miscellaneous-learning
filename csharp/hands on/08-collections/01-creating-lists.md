### 创建 List

`List<T>` 是一个可以动态增长或缩小的集合。
与数组不同，你无需预先指定固定大小。

### 声明与初始化

```csharp
// 空列表
List<int> numbers = new List<int>();

// 使用集合初始化器创建带初始值的列表
List<string> fruits = new List<string> { "Apple", "Banana", "Cherry" };

// 使用 var 让语法更简洁
var colors = new List<string> { "Red", "Green", "Blue" };
```

### List 与 Array

| 特性 | Array | List |
| --- | --- | --- |
| 大小 | 固定 | 动态 |
| 声明 | `string[]` | `List<string>` |
| 添加项 | 无法添加 | `.Add()` 方法 |
| 命名空间 | 内置 | `System.Collections.Generic` |

### 遍历 List

```csharp
List<string> names = new List<string> { "Alice", "Bob" };

// 使用 foreach
foreach (string name in names)
{
    Console.WriteLine(name);
}

// 使用 for 循环配合 Count 属性
for (int i = 0; i < names.Count; i++)
{
    Console.WriteLine(names[i]);
}
```

### 你的任务

创建一个包含恰好三个名字（"Alice"、"Bob" 和 "Charlie"）的 `List<string>`。
然后将每个名字分别打印在单独的一行上。

### 方法签名

```csharp
public static void PrintNames()
```

### 预期输出

```
Alice
Bob
Charlie
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static void PrintNames()
    {
        // 创建包含三个名字的 List<string>
        List<string> names = new List<string> { "Alice", "Bob", "Charlie" };

        // 将每个名字分别打印在单独的一行上
        foreach (string name in names)
        {
            Console.WriteLine(name);
        }
    }
}
```
