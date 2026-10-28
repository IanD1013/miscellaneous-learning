### SkipWhile - TakeWhile 的互补操作

在 LINQ 中，只要条件满足，`TakeWhile` 就会从序列的开头获取元素。
`SkipWhile` 则恰恰相反：当谓词为 true 时，它会**丢弃**序列开头的元素，然后**产出剩余的每一个元素**，无论它们是什么。
一旦谓词首次返回 false，“大门就会打开”，之后的所有内容都会顺畅通过，即使这些元素满足原始谓词也是如此。

这使得 `SkipWhile` 非常适合用于跳过已知的前缀，例如跳过数据中的表头行、绕过开头的空白字符 token，或丢弃开头的连续无用值。

### 工作原理

想象一下你正在从左到右读取一个列表。
只要你提供的条件返回 `true`，`SkipWhile` 就会不断丢弃元素。
在条件返回 `false` 的**瞬间**，它就会完全停止检查，并无条件地通过所有剩余元素。
这一点非常关键：它**不会**过滤整个序列。
它只检查开头的前缀部分。

### 语法

```csharp
IEnumerable<T> result = source.SkipWhile(element => condition);
```

谓词按顺序接收每个元素。
另一个重载还提供了索引：

```csharp
IEnumerable<T> result = source.SkipWhile((element, index) => condition);
```

### 示例

```csharp
// 跳过开头的零，然后获取其余所有元素
int[] readings = { 0, 0, 0, 42, 0, 7, 0 };
int[] meaningful = readings.SkipWhile(r => r == 0).ToArray();
// 结果：[42, 0, 7, 0]
// 注意后面的零会被包含在内，SkipWhile 只跳过开头的连续部分。

// 跳过字符串开头的小写字母
char[] chars = { 'a', 'b', 'C', 'd', 'E' };
char[] fromFirstUpper = chars.SkipWhile(c => char.IsLower(c)).ToArray();
// 结果：['C', 'd', 'E']
// 'd' 是小写，但它出现在第一个大写字母之后，因此被保留。

// 跳过少于 4 个字符的单词
string[] words = { "an", "is", "the", "magnificent", "a", "castle" };
string[] fromLong = words.SkipWhile(w => w.Length < 4).ToArray();
// 结果：["magnificent", "a", "castle"]
// "a" 的长度为 1，但它出现在 "magnificent" 处大门打开之后。
```

### 核心要点：SkipWhile 与 Where

| 操作符 | 行为 | 检查范围 |
| --- | --- | --- |
| `Where(predicate)` | 过滤序列中的**每一个**元素 | 所有元素 |
| `SkipWhile(predicate)` | 仅丢弃**开头连续满足条件的元素**，然后产出其余所有元素 | 仅前缀部分 |

当你想使用 `SkipWhile` 却误用了 `Where`（反之亦然）时，会产生截然不同的结果。

### 你的任务

编写一个方法，接收一个整数数组，并使用 `SkipWhile` 跳过所有**开头的负数**。
以数组形式返回从第一个非负数开始及之后的所有内容。
请记住，出现在第一个非负数*之后*的负数仍应包含在结果中。

- 如果数组以非负数开头，则不跳过任何内容。
- 如果每个元素都是负数，则结果为空数组。
- 空输入应返回空数组。

### 方法签名

```csharp
public static int[] SkipWhileNegative(int[] numbers)
```

### 预期结果

```scss
SkipWhileNegative([-3, -1, 2, -4, 5])  -> [2, -4, 5]
SkipWhileNegative([10, -2, 3])          -> [10, -2, 3]
SkipWhileNegative([-5, -3, -1])         -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] SkipWhileNegative(int[] numbers)
    {
        // 跳过开头的负数，从第一个非负数开始保留其余所有元素
        return numbers.SkipWhile(x => x < 0).ToArray();
    }
}
```
