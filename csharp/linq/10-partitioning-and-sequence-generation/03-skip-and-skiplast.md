### Skip 和 SkipLast - 丢弃两端的元素

在处理数据序列时，你经常需要忽略开头或末尾的一定数量的元素。
例如，你可能正在处理一个 CSV 文件并希望跳过表头行，或者正在从信号缓冲区中修剪填充数据。
LINQ 为此提供了两个互补的方法：`Skip` 和 `SkipLast`。

### 它们如何工作

**`Skip(n)`** 跳过序列中的前 `n` 个元素，并产出其后的所有元素。
如果 `n` 大于或等于元素总数，结果将是一个空序列。

**`SkipLast(n)`** 在内部缓冲序列并忽略最后的 `n` 个元素。
它实际上通过“向前看”来获知哪些元素接近末尾，然后将它们排除。
与 `Skip` 类似，如果 `n` 大于或等于总数，结果将为空。

这两个方法都是延迟执行的（deferred），它们返回一个 `IEnumerable<T>`，在对其进行迭代或物化结果之前不会执行。

### 语法

```csharp
IEnumerable<T> result = source.Skip(count);
IEnumerable<T> result = source.SkipLast(count);
```

你可以将它们链接在一起，在一个表达式中同时移除两端的元素。

### 示例

```csharp
// 跳过前 3 条日志条目（例如它们是初始化噪声）
string[] logs = { "INIT", "BOOT", "READY", "Request A", "Request B", "Request C" };
var meaningful = logs.Skip(3);
// 结果: ["Request A", "Request B", "Request C"]

// 从传感器读取缓冲区中移除最后 2 项（尾部无效数据）
double[] readings = { 22.1, 22.3, 22.0, 21.9, 0.0, 0.0 };
var clean = readings.SkipLast(2);
// 结果: [22.1, 22.3, 22.0, 21.9]

// 链式调用：从页码的开头移除 1 个并从末尾移除 1 个
int[] pages = { 0, 1, 2, 3, 4, 99 };
var interior = pages.Skip(1).SkipLast(1);
// 结果: [1, 2, 3, 4]

// 边界情况：跳过的元素数量超过现有数量
int[] tiny = { 10, 20 };
var empty = tiny.Skip(5);
// 结果: [] (空序列)
```

### 常见模式

| 模式 | 描述 |
| --- | --- |
| `source.Skip(n)` | 移除前 `n` 项（例如：跳过表头） |
| `source.SkipLast(n)` | 移除后 `n` 项（例如：丢弃表尾行） |
| `source.Skip(a).SkipLast(b)` | 从开头修剪 `a` 个，并从末尾修剪 `b` 个 |
| `source.Skip(n).ToArray()` | 将结果物化为数组 |

### 你的任务

编写一个方法，接收一个整数数组和一个整数 `n`，并返回一个从开头和末尾**两端**各移除 `n` 个元素后的新数组。
该方法应同时使用 `Skip` 和 `SkipLast` 来实现此目的。

例如，给定 `[1, 2, 3, 4, 5, 6, 7, 8]` 和 `n = 2`，从前面移除 2 个得到 `[3, 4, 5, 6, 7, 8]`，然后从后面移除 2 个得到 `[3, 4, 5, 6]`。

如果 `n` 足够大导致没有剩余元素，则返回一个空数组。

### 方法签名

```csharp
public static int[] TrimSequence(int[] numbers, int n)
```

### 预期结果

```scss
TrimSequence([1, 2, 3, 4, 5, 6, 7, 8], 2) -> [3, 4, 5, 6]
TrimSequence([10, 20, 30, 40, 50], 1) -> [20, 30, 40]
TrimSequence([5, 10, 15], 2) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] TrimSequence(int[] numbers, int n)
    {
        // 先从开头移除 n 个，再从末尾移除 n 个
        return numbers.Skip(n).SkipLast(n).ToArray();
    }
}
```
