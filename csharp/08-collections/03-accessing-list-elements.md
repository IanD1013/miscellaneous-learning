### 访问 List 元素

List 按顺序存储元素，你可以通过其位置（索引）访问任意元素。
索引从 0 开始，因此第一个元素位于索引 0。

### 索引访问

```csharp
List<string> fruits = new List<string> { "apple", "banana", "cherry" };

string first = fruits[0];   // "apple" - 第一个元素
string second = fruits[1];  // "banana" - 第二个元素
string third = fruits[2];   // "cherry" - 第三个元素
```

### Count 属性

`Count` 属性可以告诉你列表中有多少个元素。
这在查找最后一个元素时非常有用。

```csharp
List<string> fruits = new List<string> { "apple", "banana", "cherry" };

int total = fruits.Count;        // 3
string last = fruits[total - 1]; // "cherry" - 最后一个元素
```

### 为什么是 Count - 1？

由于索引从 0 开始，一个包含 3 个元素的列表具有索引 0、1 和 2。
最后一个有效索引始终是 `Count - 1`。

| List 大小 | 有效索引 | 最后一个索引 |
| --- | --- | --- |
| 3 个元素 | 0, 1, 2 | 2 (Count-1) |
| 5 个元素 | 0, 1, 2, 3, 4 | 4 (Count-1) |

### 你的任务

编写一个方法，打印字符串列表中的第一个和最后一个元素。
在一行打印第一个元素，然后在下一行打印最后一个元素。

### 方法签名

```csharp
public static void PrintFirstAndLast(List<string> items)
```

### 预期输出

```
For ["red", "green", "blue"]:
red
blue

For ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
Monday
Friday
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static void PrintFirstAndLast(List<string> items)
    {
        // 在一行打印第一个元素
        Console.WriteLine(items[0]);
        // 在下一行打印最后一个元素
        Console.WriteLine(items[items.Count - 1]);
    }
}
```
