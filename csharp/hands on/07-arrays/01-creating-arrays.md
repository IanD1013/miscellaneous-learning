### C# 中的数组

数组是一块固定大小的内存区域，用于存储多个相同类型的值。
当你预先知道需要多少个元素时，就可以使用数组：例如报告中十二个月的总计、一周七天的温度，或者微小精灵的十六个像素。

### 工作原理

使用 `new` 创建数组会一次性预留所有槽位，并用默认值填充它们（数字为 `0`，`bool` 为 `false`，引用类型为 `null`）。
之后，你可以通过**索引 (index)** 来访问每个槽位，索引从 `0` 开始，到 `Length - 1` 结束。
写入槽位会替换默认值；从槽位读取则会获取当前存储在那里的值。

### 语法

```csharp
// 声明并设置数组大小
Type[] name = new Type[size];

// 将值写入槽位
name[index] = value;

// 从槽位读取值
Type item = name[index];

// 它有多少个槽位？
int howMany = name.Length;
```

### 示例

```csharp
// 1. 创建、赋值、读取
string[] weekdays = new string[3];   // [null, null, null]
weekdays[0] = "Monday";
weekdays[1] = "Tuesday";
weekdays[2] = "Wednesday";
Console.WriteLine(weekdays[1]);      // Tuesday
Console.WriteLine(weekdays.Length);  // 3

// 2. 使用由 Length 驱动的循环填充每个槽位
double[] prices = new double[4];
for (int i = 0; i < prices.Length; i++)
{
    prices[i] = 9.99;                // [9.99, 9.99, 9.99, 9.99]
}

// 3. 使用索引本身来计算存储的值
int[] squares = new int[5];
for (int i = 0; i < squares.Length; i++)
{
    squares[i] = i * i;              // [0, 1, 4, 9, 16]
}

// 4. 快捷方式：在创建时初始化值
int[] primes = new int[] { 2, 3, 5, 7 };
```

### 常见模式

| 模式 | 作用 |
| --- | --- |
| `new int[n]` | 预留 `n` 个槽位，每个槽位初始值为 `0` |
| `arr[0]`, `arr[arr.Length - 1]` | 第一个和最后一个元素 |
| `for (int i = 0; i < arr.Length; i++)` | 安全地访问每个索引 |
| `arr[i] = someExpression;` | 覆盖槽位 `i` 中的默认值 |

超出 `0 .. Length - 1` 范围的索引会抛出 `IndexOutOfRangeException`，因此循环几乎总是以 `Length` 为界。

### 任务

编写 `BuildMultiples(int count, int step)` 方法，返回一个包含 `count` 个元素的**新** `int` 数组，其中第一个元素是 `step` 的 1 倍，第二个元素是 `step` 的 2 倍，以此类推。

例如，当 `step = 3` 时，值为 3, 6, 9, 12, ... 。
如果 `count` 为 `0`，则返回一个空数组（`Length` 为 0 的数组，而不是 `null`）。

### 方法签名

```csharp
public static int[] BuildMultiples(int count, int step)
```

### 预期结果

```
BuildMultiples(5, 3) -> [3, 6, 9, 12, 15]
BuildMultiples(1, 10) -> [10]
BuildMultiples(0, 7) -> []
BuildMultiples(3, -2) -> [-2, -4, -6]
```

### 解答

```csharp
using System;

public class Solution
{
    public static int[] BuildMultiples(int count, int step)
    {
        // 创建一个能容纳 count 个元素的 int 数组（count 为 0 时就是空数组）
        int[] multiples = new int[count];
        // 索引 i 处存放 step 的 (i + 1) 倍
        for (int i = 0; i < multiples.Length; i++)
        {
            multiples[i] = (i + 1) * step;
        }
        // 返回填充好的数组
        return multiples;
    }
}
```
