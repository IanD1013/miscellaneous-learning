### 使用 for 遍历数组

`for` 循环是在需要访问索引时遍历数组的经典方式。
它让你可以精确控制访问哪些元素以及按什么顺序访问。

### Length 属性

每个数组都有一个 `Length` 属性，用于告知你该数组包含多少个元素：

```csharp
int[] scores = { 85, 92, 78 };
Console.WriteLine(scores.Length); // 输出：3
```

### 基本 For 循环模式

遍历整个数组的标准模式：

```csharp
int[] values = { 10, 20, 30, 40 };

for (int i = 0; i < values.Length; i++)
{
    Console.WriteLine(values[i]);
}
// 输出：
// 10
// 20
// 30
// 40
```

### 理解循环

| 部分 | 含义 |
| --- | --- |
| `int i = 0` | 从索引 0 开始（第一个元素） |
| `i < values.Length` | 当索引有效时继续循环 |
| `i++` | 每次迭代后移动到下一个索引 |
| `values[i]` | 访问当前索引处的元素 |

### 为什么使用 i < Length（而不是 <=）？

数组是从 0 开始索引的，因此有效索引范围是 `0` 到 `Length - 1`：

```csharp
int[] arr = { 5, 10, 15 };
// Length 为 3
// 有效索引：0, 1, 2
// 使用 i <= arr.Length 会尝试访问索引 3（报错！）
```

### 你的任务

编写一个方法，使用 `for` 循环打印整数数组的所有元素，每个元素各占一行。

### 方法签名

```csharp
public static void PrintAllElements(int[] numbers)
```

### 预期结果

```
PrintAllElements([1, 2, 3]) 打印：
1
2
3

PrintAllElements([42]) 打印：
42
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintAllElements(int[] numbers)
    {
        // 使用 for 循环，以 numbers.Length 为界，每个元素各占一行
        for (int i = 0; i < numbers.Length; i++)
        {
            Console.WriteLine(numbers[i]);
        }
    }
}
```
