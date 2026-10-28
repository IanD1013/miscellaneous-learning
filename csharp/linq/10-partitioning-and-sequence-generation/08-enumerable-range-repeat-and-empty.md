### 使用 Enumerable.Range、Enumerable.Repeat 和 Enumerable.Empty 生成序列

并不是每个 LINQ 管道都需要从已有的集合开始。
有时你需要从头*创建*一个序列，用于生成测试数据、构建重复模式，或在管道中提供一个中立的起始点。
C# 在 `Enumerable` 上提供了三个静态方法来实现这一功能，而无需任何源集合。

### 它们的工作原理

**`Enumerable.Range(start, count)`** 生成一个从 `start` 开始、包含 `count` 个元素的连续整数序列。
可以将其视为按需截取的一段数轴。

**`Enumerable.Repeat<T>(element, count)`** 生成一个包含重复 `count` 次的相同 `element` 的序列。
该元素可以是*任何*类型：整数、字符串，甚至是整个集合。

**`Enumerable.Empty<T>()`** 返回指定类型的空序列。
它可用作 `Aggregate` 的种子值、在没有可用数据时的默认返回值，或作为 `Concat` 链中的中立元素。

### 语法

```csharp
// 生成从 start 到 start + count - 1 的整数
IEnumerable<int> numbers = Enumerable.Range(start, count);

// 将一个元素重复 count 次
IEnumerable<T> repeated = Enumerable.Repeat(element, count);

// 创建指定类型的空序列
IEnumerable<T> empty = Enumerable.Empty<T>();
```

### 示例

```csharp
// 示例 1：生成从 10 到 18 的偶数
var evens = Enumerable.Range(5, 5).Select(n => n * 2);
// 结果：[10, 12, 14, 16, 18]

// 示例 2：创建包含 4 个默认用户的列表
var defaults = Enumerable.Repeat("Guest", 4).ToList();
// 结果：["Guest", "Guest", "Guest", "Guest"]

// 示例 3：使用 Empty 作为安全的后备值
bool hasData = false;
var result = hasData
    ? Enumerable.Range(1, 5)
    : Enumerable.Empty<int>();
// 结果：[]

// 示例 4：重复一个*序列*并使用 SelectMany 展平
var letters = new[] { "A", "B" };
var tripled = Enumerable.Repeat(letters, 3)
    .SelectMany(seq => seq)
    .ToArray();
// 结果：["A", "B", "A", "B", "A", "B"]
```

### 核心要点：重复序列

注意在上面的示例 4 中，`Enumerable.Repeat` 可以重复*任何*对象，包括整个 `IEnumerable<T>`。
其结果是一个序列的序列（`IEnumerable<IEnumerable<T>>`）。
要将其展平为单个扁平序列，可以使用 `SelectMany`，它会将所有内部序列串联在一起。

### 你的任务

编写一个结合使用 `Enumerable.Range` 和 `Enumerable.Repeat` 来构建重复数字模式的方法。

给定三个参数：

- `start`：范围内的第一个数字
- `count`：范围内有多少个连续整数
- `repeatTimes`：整个范围重复的次数

返回一个包含重复指定次数的范围的 `int[]`。

如果 `count` 为 0，则范围为空，因此无论 `repeatTimes` 为多少，结果都应为空数组。
类似地，如果 `repeatTimes` 为 0，则不重复任何内容，因此结果为空。

### 方法签名

```csharp
public static int[] GeneratePattern(int start, int count, int repeatTimes)
```

### 预期结果

```scss
GeneratePattern(1, 3, 2)  -> [1, 2, 3, 1, 2, 3]
GeneratePattern(5, 2, 3)  -> [5, 6, 5, 6, 5, 6]
GeneratePattern(0, 1, 5)  -> [0, 0, 0, 0, 0]
GeneratePattern(10, 4, 0) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] GeneratePattern(int start, int count, int repeatTimes)
    {
        // 将整个范围重复 repeatTimes 次，再用 SelectMany 展平为单个序列
        return Enumerable.Repeat(Enumerable.Range(start, count), repeatTimes)
            .SelectMany(seq => seq)
            .ToArray();
    }
}
```
