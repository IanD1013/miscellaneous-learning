### Append 和 Prepend - 向序列中添加单个元素

在使用 LINQ 序列时，有时您需要在不修改原始集合的情况下，在集合的开头或结尾插入单个元素。
.NET 引入 `Prepend` 和 `Append` 方法正是为了满足这一需求。
它们返回一个**新的** `IEnumerable<T>`，源集合保持不变。

### 工作原理

这两种方法都使用**延迟执行**（deferred execution），这意味着在您遍历它们（或使用 `.ToArray()`、`.ToList()` 等将其具体化）之前，它们不会实际生成结果。
可以将它们视为轻量级包装器，表示“当有人遍历我时，在原始元素之前（或之后）生成这个额外元素”。

- `Prepend(element)`：将 `element` 置于所有现有元素之前
- `Append(element)`：将 `element` 置于所有现有元素之后

因为它们返回 `IEnumerable<T>`，所以您可以流畅地将它们**链式调用**。

### 语法

```csharp
IEnumerable<T> result = source.Prepend(element);
IEnumerable<T> result = source.Append(element);
```

两者都是通过 `System.Linq` 提供的 `IEnumerable<T>` 扩展方法。

### 示例

```csharp
// 示例 1：向姓名列表中添加标题标签
var names = new[] { "Bob", "Carol" };
var withHeader = names.Prepend("== Staff ==");
// 遍历 withHeader 生成："== Staff ==", "Bob", "Carol"

// 示例 2：在末尾添加哨兵值
var readings = new[] { 3.1, 4.7, 2.9 };
var terminated = readings.Append(-1.0).ToArray();
// terminated 为 [3.1, 4.7, 2.9, -1.0]

// 示例 3：将两者链式连接在一起
var scores = new List<int> { 85, 92 };
var framed = scores.Prepend(100).Append(0).ToList();
// framed 为 [100, 85, 92, 0]
// scores 仍然是 [85, 92]，未发生改变！
```

### 关键要点

| 方面 | 详情 |
| --- | --- |
| 返回值 | 一个新的 `IEnumerable<T>` - 源集合**不会**被修改 |
| 执行方式 | 延迟执行 - 直到遍历时才会执行操作 |
| 链式调用 | 您可以按任意顺序链式调用 `.Prepend().Append()`（或反之亦然） |
| 具体化 | 当需要具体集合时，请使用 `.ToArray()` 或 `.ToList()` |

### 您的任务

编写一个方法，接收一个整数数组和另外两个整数。
使用 `Prepend` 将第一个值放在开头，使用 `Append` 将第二个值放在末尾。
以 `int[]` 形式返回结果。

### 方法签名

```csharp
public static int[] WrapSequence(int[] numbers, int first, int last)
```

### 预期结果

```scss
WrapSequence([2, 3, 4], 1, 5)      -> [1, 2, 3, 4, 5]
WrapSequence([10, 20], 0, 30)       -> [0, 10, 20, 30]
WrapSequence([], 42, 99)            -> [42, 99]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] WrapSequence(int[] numbers, int first, int last)
    {
        // 在开头放入 first，在末尾放入 last
        return numbers.Prepend(first).Append(last).ToArray();
    }
}
```
