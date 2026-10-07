### 修改数组元素

数组是可变的（mutable），这意味着你可以在创建数组后更改其中的元素。
你可以通过索引位置来访问和修改元素。

### 按索引访问元素

```csharp
int[] scores = { 85, 90, 78 };

// 读取元素
int firstScore = scores[0];  // 85

// 修改元素
scores[0] = 95;  // 第一个元素现在为 95
scores[2] = 82;  // 第三个元素现在为 82
```

### 记住：从零开始的索引（Zero-Based Indexing）

```csharp
string[] fruits = { "apple", "banana", "cherry" };
//                    [0]       [1]        [2]

// “第二个”元素位于索引 1
fruits[1] = "blueberry";  // 把 "banana" 改为 "blueberry"
```

### 常见错误

```csharp
int[] nums = { 10, 20, 30 };

// 错误：尝试用索引 2 访问“第二个”位置
// nums[2] 实际上是第三个元素（值为 30）

// 正确：第二个元素位于索引 1
nums[1] = 99;  // 把 20 改为 99
```

### 你的任务

编写一个修改数组并打印其所有元素的方法：

1. 将**第二个元素**（索引 1）的值修改为 `99`
2. 在单独的一行中打印数组的每个元素

### 方法签名

```csharp
public static void ModifyAndPrint(int[] numbers)
```

### 预期结果

```
ModifyAndPrint({10, 20, 30}) 打印：
10
99
30

ModifyAndPrint({5, 15}) 打印：
5
99
```

### 解答

```csharp
using System;

public class Solution
{
    public static void ModifyAndPrint(int[] numbers)
    {
        // 把第二个元素（索引 1）改为 99
        numbers[1] = 99;
        // 然后打印修改后的数组，每个元素各占一行
        foreach (int number in numbers)
        {
            Console.WriteLine(number);
        }
    }
}
```
