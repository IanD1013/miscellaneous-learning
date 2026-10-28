### TakeWhile - 条件序列分区

LINQ 的 `TakeWhile` 会从序列的**开头**开始产出元素，只要谓词条件返回 `true`。
一旦有任何元素不满足条件，迭代就会**永久停止**，即使后面的元素满足谓词条件也是如此。
这使得它与扫描整个集合的 `Where` 有着本质的区别。

当处理有序或序列化数据，且你需要获取满足某些条件的前导“连续”元素片段时，这种行为非常强大。

### 工作原理

想象一下从传感器日志中读取温度。
你想要获取一天开始时所有保持在 30°C 以下的读数。
一旦读数达到 30 或更高，你就会停止，你不在乎后面温度是否会再次下降。
这正是 `TakeWhile` 所做的事情：它从头部开始提取元素，并在遇到第一个不符合条件的元素时退出。

至关重要的是，`TakeWhile` 具有**两个重载**：

- `TakeWhile(Func<T, bool> predicate)`：接收每个元素
- `TakeWhile(Func<T, int, bool> predicate)`：接收每个元素**及其索引**

当你的条件依赖于元素的位置或其与相邻元素的关系时，带索引的重载至关重要。

### 语法

```csharp
// 基本重载：谓词只接收元素
sequence.TakeWhile(element => condition)

// 带索引的重载：谓词接收元素及其从零开始的索引
sequence.TakeWhile((element, index) => conditionUsingIndex)
```

### 示例

```csharp
// 当单词较短（长度 <= 4）时持续获取
string[] words = { "hi", "the", "cat", "elephant", "go" };
var shortWords = words.TakeWhile(w => w.Length <= 4);
// 结果：["hi", "the", "cat"]
// "elephant" 不满足条件，因此永远不会到达 "go"

// 当每个数字都是偶数时持续获取
int[] nums = { 2, 4, 6, 7, 8, 10 };
var evens = nums.TakeWhile(n => n % 2 == 0);
// 结果：[2, 4, 6]
// 7 是奇数 → 停止。8 和 10 被忽略。

// 带索引的重载：当值等于 index * 10 时持续获取元素
int[] scores = { 0, 10, 20, 25, 40 };
var matching = scores.TakeWhile((score, i) => score == i * 10);
// 结果：[0, 10, 20]
// 在索引 3 处，score 25 != 30，因此停止。
```

### 核心要点：TakeWhile 与 Where

| 方法 | 扫描整个序列？ | 保持顺序？ | 提前停止？ |
| --- | --- | --- | --- |
| `Where` | 是 | 是 | 否 |
| `TakeWhile` | 否 - 在第一次失败时停止 | 是 | 是 |

这种区别对正确性和性能都很重要。
如果你的数据是有序的或按序列排列的，并且你想要一个连续的前缀部分，`TakeWhile` 就是正确的工具。

### 使用带索引的重载比较相邻元素

当你需要将每个元素与前一个元素进行比较时，带索引的重载允许你通过索引引用原始集合。
第一个元素（索引 0）通常会无条件通过，因为前面没有元素可供比较。

```csharp
// 当每个字符按字母顺序都位于前一个字符之后时持续获取
char[] letters = { 'a', 'c', 'f', 'd', 'z' };
var ascending = letters.TakeWhile((ch, i) => i == 0 || ch > letters[i - 1]);
// 结果：['a', 'c', 'f']
// 'd' < 'f' → 停止
```

### 你的任务

编写一个方法，接收一个整数数组，并返回每个元素都**严格大于**前一个元素的前导部分。
一旦某个元素小于或等于它前面的元素，就停止提取。

例如：

- `[1, 3, 5, 4, 7, 8]` → 序列在 1、3、5 递增。
  接着 4 ≤ 5，因此停止。
  结果：`[1, 3, 5]`
- `[10, 20, 30, 40]` → 整个过程严格递增。
  结果：`[10, 20, 30, 40]`
- `[5, 5, 6]` → 5 不严格大于 5，因此只提取第一个元素。
  结果：`[5]`

### 方法签名

```csharp
public static int[] TakeWhileIncreasing(int[] numbers)
```

### 预期结果

```scss
TakeWhileIncreasing([1, 3, 5, 4, 7, 8]) -> [1, 3, 5]
TakeWhileIncreasing([10, 20, 30, 40]) -> [10, 20, 30, 40]
TakeWhileIncreasing([5, 5, 6]) -> [5]
TakeWhileIncreasing([9, 3, 7]) -> [9]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] TakeWhileIncreasing(int[] numbers)
    {
        // 使用带索引的重载：第一个元素无条件通过，之后每个元素都必须严格大于前一个元素
        return numbers.TakeWhile((x, i) => i == 0 || x > numbers[i - 1]).ToArray();
    }
}
```
