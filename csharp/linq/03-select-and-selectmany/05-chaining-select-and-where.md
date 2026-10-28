### 链式调用 Where 和 Select - 先过滤，后转换

在 LINQ 中，你经常需要同时对集合进行**过滤**和对其元素进行**转换**。
链式调用这些操作的顺序至关重要，不仅关乎正确性，还关乎效率。
首先使用 `Where` 进行过滤可以减少进入 `Select` 等后续操作的元素数量，这意味着总共执行的转换次数会更少。

### 工作原理

可以把它想象成一条装配流水线。
如果你只需要将红色的汽车漆成蓝色，那么**先挑出红色的汽车**（过滤），然后再对它们进行涂漆（转换）会高效得多，而不是先把每一辆车都漆成蓝色，然后再试图找出哪些原本是红色的。

在 LINQ 中：

- **`Where`** 充当关卡：它会对每个元素计算条件，并且只允许符合条件的元素通过。
- **`Select`** 充当转换器：它获取每个元素并生成其新形式。

当你在 `Select` 之前链式调用 `Where` 时，`Select` 只会处理通过过滤的元素。
如果你颠倒顺序，`Select` 将转换*每一个*元素，然后 `Where` 会丢弃其中的某些转换结果，造成不必要的工作浪费。

### 语法

```csharp
// 通用模式：过滤 → 转换 → 具体化
collection
    .Where(item => /* 布尔条件 */)
    .Select(item => /* 转换表达式 */)
    .ToArray();  // 或 .ToList()
```

### 示例

```csharp
// 示例 1：获取偶数的平方
int[] numbers = { 1, 2, 3, 4, 5, 6 };
int[] result = numbers
    .Where(n => n % 2 == 0)    // 保留：2, 4, 6
    .Select(n => n * n)         // 生成：4, 16, 36
    .ToArray();
// result: [4, 16, 36]

// 示例 2：获取活跃用户的格式化名称
string[] users = { "alice:active", "bob:inactive", "carol:active" };
string[] active = users
    .Where(u => u.EndsWith(":active"))       // 保留 alice 和 carol 的条目
    .Select(u => u.Split(':')[0].ToUpper())
    .ToArray();
// active: ["ALICE", "CAROL"]

// 示例 3：低效写法（顺序颠倒）- 先转换所有元素，再丢弃
int[] inefficient = numbers
    .Select(n => n * n)         // 先对全部 6 个数字求平方
    .Where(n => n % 2 == 0)     // 然后再过滤，但奇数的平方白算了！
    .ToArray();
// 这样可以运行，但对那些最终被丢弃的元素做了不必要的计算
```

### 常用模式

| 模式 | 描述 |
| --- | --- |
| `.Where(...).Select(...)` | 先过滤后转换，**推荐** |
| `.Where(...).Select(...).ToArray()` | 过滤、转换并具体化为数组 |
| `.Where(...).Select(...).ToList()` | 过滤、转换并具体化为列表 |
| `.Select(...).Where(...)` | 先转换后过滤，可行但效率较低 |

### 常用参考

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `Where(predicate)` | 按条件过滤元素 | `.Where(x => x > 5)` |
| `Select(transform)` | 将每个元素投影为新形式 | `.Select(x => x * 2)` |
| `ToArray()` | 将结果转换为 `string[]` 或 `int[]` | `.ToArray()` |
| `string.ToUpper()` | 返回字符串的大写版本 | `"hello".ToUpper()` → `"HELLO"` |
| `string.Length` | 返回字符串中的字符数 | `"hello".Length` → `5` |

### 你的任务

编写一个接收单词数组和最小长度的方法。
它应该：

1. **过滤**单词，仅保留长度**至少**为 `minLength` 的单词
2. 将过滤留下的单词**转换**为大写
3. 以 `string[]` 形式返回结果

确保按正确的顺序链式调用这些操作：先过滤，后转换。

### 方法签名

```csharp
public static string[] GetUpperCaseLongWords(string[] words, int minLength)
```

### 预期结果

```css
GetUpperCaseLongWords(["cat", "butterfly", "dog", "elephant"], 4) -> ["BUTTERFLY", "ELEPHANT"]
GetUpperCaseLongWords(["hi", "hello", "hey"], 3) -> ["HELLO", "HEY"]
GetUpperCaseLongWords(["a", "bb", "ccc"], 5) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] GetUpperCaseLongWords(string[] words, int minLength)
    {
        return words
            // 先过滤：只保留长度至少为 minLength 的单词
            .Where(w => w.Length >= minLength)
            // 再转换：转为大写
            .Select(w => w.ToUpper())
            .ToArray();
    }
}
```
