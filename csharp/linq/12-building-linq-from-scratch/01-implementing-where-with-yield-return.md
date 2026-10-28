### 使用 `yield return` 从零构建 LINQ 的 Where

是否曾好奇过在 LINQ 中调用 `.Where(x => x > 10)` 时底层究竟发生了什么？
答案就在 C# 最优雅的特性之一中：**由 `yield return` 驱动的迭代器**。
理解这一机制揭示了 LINQ 如何实现延迟执行（deferred execution），即查询在实际遍历其结果之前不会运行。

### 迭代器和 `yield return` 的工作原理

当一个方法包含 `yield return` 时，C# 编译器会将其转换为一个**状态机**。
该方法不会预先计算所有结果并返回一个集合，而是**一次生成一个值**，在每次 `yield return` 后暂停，并在调用者请求下一个值时恢复执行。

这就是延迟执行背后的核心引擎。
在定义 LINQ 查询时不会执行任何实际工作：只有在枚举结果时（例如在 `foreach` 循环中，或通过调用 `.ToArray()`）才会执行工作。

关键行为：

- 方法必须返回 `IEnumerable<T>` 或 `IEnumerator<T>`
- 执行在每次 `yield return` 处暂停，并在下一次调用 `MoveNext()` 时恢复
- `yield break` 用于提前终止序列
- 在迭代开始之前，方法体完全不会执行

### 语法

```csharp
public static IEnumerable<T> ProduceValues(/* 参数 */)
{
    // 首次 yield 之前的代码仅在迭代开始时运行一次
    foreach (var item in someSource)
    {
        if (/* 条件 */)
        {
            yield return item; // 在此处暂停，将此值提供给调用者
        }
    }
    // 到达末尾（或遇到 yield break）表示序列已完成
}
```

### 示例

**示例 1：生成平方数序列**

```csharp
public static IEnumerable<int> Squares(int count)
{
    for (int i = 1; i <= count; i++)
    {
        yield return i * i;
    }
}
// Squares(4) 惰性生成：1, 4, 9, 16
```

**示例 2：按长度过滤字符串**

```csharp
public static IEnumerable<string> LongWords(string[] words, int minLength)
{
    foreach (var word in words)
    {
        if (word.Length >= minLength)
        {
            yield return word;
        }
    }
}
// LongWords(["hi", "hello", "hey", "wonderful"], 4) → "hello", "wonderful"
```

**示例 3：使用 `yield break` 提前终止**

```csharp
public static IEnumerable<int> TakeWhilePositive(int[] values)
{
    foreach (var v in values)
    {
        if (v <= 0)
            yield break; // 完全停止生成值
        yield return v;
    }
}
// TakeWhilePositive([3, 7, 2, -1, 5]) → 3, 7, 2
```

### LINQ Where 内部的模式

从核心来看，`Where` 遵循一个简单的模式：遍历数据源，根据谓词条件测试每个元素，并仅对通过测试的元素执行 `yield return`。
其中的奥妙不在于复杂的算法，而在于 `yield return` 关键字将一个普通的循环转变成了惰性的延迟执行管道。

### 你的任务

编写一个方法 `FilterEvens`，该方法接收一个整数数组并返回一个仅包含偶数的 `IEnumerable<int>`，**保持它们原本的顺序**。
你必须使用循环和 `yield return` 手动实现此逻辑，不允许使用任何 LINQ 运算符。

请记住：

- 如果一个整数除以 2 没有余数，则它是偶数
- 负偶数（例如 -4）也是偶数
- 0 是偶数
- 空输入应生成空序列

### 方法签名

```csharp
public static IEnumerable<int> FilterEvens(int[] numbers)
```

### 预期结果

```scss
FilterEvens([1, 2, 3, 4, 5, 6]) → [2, 4, 6]
FilterEvens([7, 11, 13]) → []
FilterEvens([-3, -2, 0, 1, 4]) → [-2, 0, 4]
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static IEnumerable<int> FilterEvens(int[] numbers)
    {
        foreach (int n in numbers)
        {
            // 除以 2 余数为 0 即为偶数（负数和 0 同样适用）
            if (n % 2 == 0)
            {
                yield return n; // 按原顺序逐个产出偶数
            }
        }
    }
}
```
