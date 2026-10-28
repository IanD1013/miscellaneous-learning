### `Where` 的带索引重载

你已经熟悉了 LINQ 的 `Where` 方法，用于根据条件筛选序列。
但如果你的筛选逻辑不仅取决于每个元素的*值*，还取决于它在序列中的*位置*呢？
LINQ 提供了 `Where` 的第二个重载，同时为你提供元素及其从零开始的索引，因此你可以编写具有位置感知能力的筛选器。

这在很多场景下非常有用，例如从导入的数据中每隔一行提取一行、跳过已知位置的表头项，或者根据项目在列表中的位置应用交替逻辑。

### 工作原理

标准的 `Where` 接受一个带有一个参数（元素）的谓词（predicate）：

```csharp
.Where(element => condition)
```

**带索引的重载**接受一个带有两个参数（元素及其从 0 开始的位置）的谓词：

```csharp
.Where((element, index) => condition)
```

`index` 参数会自动递增计数，第一个元素为 `0`，第二个元素为 `1`，依此类推。
你可以将它与元素本身一起在任何布尔表达式中使用。

### 语法

```csharp
IEnumerable<T> Where<T>(Func<T, int, bool> predicate)
```

Lambda 表达式 `(element, index) => ...` 必须返回 `true` 以保留元素或返回 `false` 以排除它，就像常规的 `Where` 一样，但现在你可以使用索引了。

### 示例

```csharp
// 只保留奇数位置（1, 3, 5, ...）的元素
int[] scores = { 90, 85, 78, 92, 64, 88 };
var oddPositioned = scores.Where((score, i) => i % 2 != 0).ToArray();
// 结果: [85, 92, 88]

// 使用索引跳过前 3 个元素
string[] colors = { "red", "green", "blue", "yellow", "purple" };
var afterThird = colors.Where((color, i) => i >= 3).ToArray();
// 结果: ["yellow", "purple"]

// 保留值的长度与其位置相等的元素
string[] tags = { "", "x", "ab", "dog", "four" };
var matched = tags.Where((tag, i) => tag.Length == i).ToArray();
// 结果: ["", "x", "ab", "dog", "four"]，全部匹配！
```

请注意每个示例是如何将索引与不同的逻辑结合起来的。
核心关键在于 lambda 中的第二个参数始终是位置，你可以根据需要随意使用它。

### 常见模式

| 模式 | Lambda | 描述 |
| --- | --- | --- |
| 每第 N 个元素 | `(el, i) => i % N == 0` | 保留位置为 0, N, 2N, ... 的元素 |
| 跳过前 K 个 | `(el, i) => i >= K` | 丢弃前 K 个元素 |
| 位置范围 | `(el, i) => i >= start && i < end` | 按索引保留切片 |
| 结合值与位置 | `(el, i) => el > threshold && i < limit` | 同时根据值和索引进行筛选 |

### 你的任务

编写一个方法，接受一个字符串数组，并仅返回位于**偶数位置**（索引 0、2、4……）的单词。
使用 `Where` 的带索引重载来实现此功能。

- 空数组应返回空数组。
- 单元素数组应返回该元素（索引 0 为偶数）。

### 方法签名

```csharp
public static string[] FilterEvenIndexed(string[] words)
```

### 预期结果

```css
FilterEvenIndexed(["a", "b", "c", "d", "e"]) -> ["a", "c", "e"]
FilterEvenIndexed(["hello", "world"]) -> ["hello"]
FilterEvenIndexed([]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FilterEvenIndexed(string[] words)
    {
        // 使用带索引的 Where，只保留索引为偶数的元素
        return words.Where((word, i) => i % 2 == 0).ToArray();
    }
}
```
