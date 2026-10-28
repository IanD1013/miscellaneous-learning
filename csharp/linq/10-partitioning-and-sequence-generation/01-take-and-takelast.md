### 使用 Take 和 TakeLast 对序列进行分区

在处理集合时，你经常需要从序列的任一端提取元素：前几个元素、后几个元素，或者两者兼有。
LINQ 提供了两个互补的方法来实现这一点：`Take` 和 `TakeLast`。
在展示最近活动、对结果进行分页或比较数据集的开头和结尾等任务中，它们都是必不可少的工具。

### 工作原理

`Take(n)` 从开头遍历序列并生成前 `n` 个元素。
一旦生成了 `n` 个元素，它就会停止，序列的其余部分绝不会被评估。
`TakeLast(n)` 则相反：它只生成序列末尾的 `n` 个元素。

这两种方法都能优雅地处理边缘情况。
如果序列包含的元素少于 `n` 个，它们只会返回所有可用元素，不会抛出异常，也不会添加任何填充。

### 语法

```csharp
IEnumerable<T> result = source.Take(count);
IEnumerable<T> result = source.TakeLast(count);
```

两者都返回 `IEnumerable<T>`，因此你可以将它们与其他 LINQ 方法链式调用，或者将它们转换为数组或列表。

### 示例

```csharp
// 从前端获取元素
string[] cities = { "London", "Paris", "Berlin", "Tokyo", "Sydney" };
var firstTwo = cities.Take(2); // ["London", "Paris"]

// 从后端获取元素
var lastThree = cities.TakeLast(3); // ["Berlin", "Tokyo", "Sydney"]

// 当 n 超过长度时，将返回所有元素
int[] scores = { 95, 88 };
var topFive = scores.Take(5); // [95, 88] - 仅有 2 个可用
var bottomFive = scores.TakeLast(5); // [95, 88] - 仅有 2 个可用

// 获取零个元素将返回空序列
var none = cities.Take(0); // []

// 合并两端的结果
double[] temps = { 18.5, 20.1, 22.3, 19.8, 17.6 };
var edges = temps.Take(1).Concat(temps.TakeLast(1)); // [18.5, 17.6]
```

### 实用参考

| 方法 | 描述 |
| --- | --- |
| `Take(n)` | 返回前 `n` 个元素 |
| `TakeLast(n)` | 返回后 `n` 个元素 |
| `Concat(other)` | 将一个序列追加到另一个序列末尾 |
| `ToArray()` | 将 `IEnumerable<T>` 转换为数组 |

### 你的任务

编写一个方法，接收一个整数数组和一个数量 `n`，然后返回一个新数组，其中包含输入数组的前 `n` 个元素，后跟后 `n` 个元素。

请注意，相对于数组长度而言，当 `n` 足够大时，某些元素可能会同时出现在“前半部分”和“后半部分”组中，这是符合预期的行为。

### 方法签名

```csharp
public static int[] TakeFirstAndLast(int[] numbers, int n)
```

### 预期结果

```scss
TakeFirstAndLast([1, 2, 3, 4, 5, 6, 7, 8], 2) -> [1, 2, 7, 8]
TakeFirstAndLast([10, 20, 30, 40, 50], 3) -> [10, 20, 30, 30, 40, 50]
TakeFirstAndLast([5], 1) -> [5, 5]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] TakeFirstAndLast(int[] numbers, int n)
    {
        // 前 n 个元素后接后 n 个元素
        return numbers.Take(n).Concat(numbers.TakeLast(n)).ToArray();
    }
}
```
