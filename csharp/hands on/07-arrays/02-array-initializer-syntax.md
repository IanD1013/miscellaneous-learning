### 数组索引

数组使用从零开始的索引来访问元素。
第一个元素位于索引 0，第二个位于索引 1，依此类推。

### 读取元素

```csharp
int[] scores = { 85, 92, 78, 95 };

int first = scores[0];   // 85（第一个元素）
int second = scores[1];  // 92（第二个元素）
int third = scores[2];   // 78（第三个元素）
```

### 查找最后一个元素 - 传统方法

要访问最后一个元素，可以使用数组的 `Length` 属性减去 1：

```csharp
int[] values = { 10, 20, 30, 40, 50 };

int length = values.Length;       // 5 个元素
int lastIndex = values.Length - 1; // 索引 4
int lastValue = values[lastIndex]; // 50

// 常用简写：
int last = values[values.Length - 1]; // 50
```

### 查找最后一个元素 - 从末尾索引（^）运算符

C# 8.0+ 引入了 `^`（从末尾索引）运算符以提供更简洁的语法：

```csharp
int[] values = { 10, 20, 30, 40, 50 };

int last = values[^1];        // 50（最后一个元素）
int secondLast = values[^2];  // 40（倒数第二个）
int thirdLast = values[^3];   // 30（倒数第三个）
```

`^1` 表示“倒数第 1 个”，`^2` 表示“倒数第 2 个”，依此类推。
请注意，`^0` 会导致越界（它等于 `Length`）。

### 比较两种方法

| 任务 | 传统方法 | 从末尾索引 |
| --- | --- | --- |
| 最后一个元素 | `arr[arr.Length - 1]` | `arr[^1]` |
| 倒数第二个 | `arr[arr.Length - 2]` | `arr[^2]` |
| 倒数第三个 | `arr[arr.Length - 3]` | `arr[^3]` |

两种方法都是有效的。
`^` 运算符更加简洁，而传统方法在所有 C# 版本中均可使用，并且在处理计算得到的索引时有时是必需的。

### 为什么是 Length - 1？

由于索引从 0 开始，包含 5 个元素的数组其索引分别为 0、1、2、3、4。
最后一个有效索引始终为 `Length - 1`。

| 数组 | 长度 | 第一个索引 | 最后一个索引 |
| --- | --- | --- | --- |
| `{5, 10, 15}` | 3 | 0 | 2 |
| `{1, 2, 3, 4, 5}` | 5 | 0 | 4 |
| `{100}` | 1 | 0 | 0 |

### 你的任务

编写一个方法，在单独的行上分别打印出整数数组的第一个和最后一个元素。
你可以使用传统方法或 `^` 运算符。

### 方法签名

```csharp
public static void PrintFirstAndLast(int[] numbers)
```

### 预期输出

```
PrintFirstAndLast(new int[] { 10, 20, 30, 40 })
// 打印：
// 10
// 40

PrintFirstAndLast(new int[] { 5, 15, 25 })
// 打印：
// 5
// 25
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintFirstAndLast(int[] numbers)
    {
        // 在一行打印第一个元素
        Console.WriteLine(numbers[0]);
        // 在下一行打印最后一个元素
        Console.WriteLine(numbers[^1]);
    }
}
```
