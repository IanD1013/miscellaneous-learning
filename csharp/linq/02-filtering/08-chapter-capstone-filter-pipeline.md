### 过滤管道 - 组合多个 LINQ 操作

现实世界中的数据很少只需要单次转换。
你几乎总是需要将多个操作链接在一起：移除不符合条件的项，通过第二个条件进一步缩小范围，然后对剩余的内容进行排序。
LINQ 的 Fluent API 正是为此设计的：每个方法都返回一个 `IEnumerable<T>`，并直接传递给下一个方法。

### 工作原理

可以把它想象成水流经管道中的一系列过滤器。
第一个过滤器滤除大杂质，第二个过滤器滤除较小的颗粒，最后一个阶段对剩余的部分进行排序。
每个 LINQ 方法都充当一个阶段：它接收一个序列，应用一条规则，并将结果传递给下游。

### 语法

```csharp
// 链式调用 LINQ 操作的通用模式
var result = source
    .Where(item => /* 第一个条件 */)
    .Where(item => /* 第二个条件 */)
    .OrderBy(item => /* 排序键 */)
    .ToArray();
```

你可以根据需要链接任意数量的 `.Where()` 调用。
每一个都会进一步缩小集合的范围。

### 示例

```csharp
// 示例 1：按范围过滤数字，然后降序排序
int[] numbers = { 15, 3, 42, 7, 28, 1, 99 };
int[] result = numbers
    .Where(n => n >= 10)       // 保留 15, 42, 28, 99
    .Where(n => n < 50)        // 保留 15, 42, 28
    .OrderByDescending(n => n)  // 42, 28, 15
    .ToArray();

// 示例 2：先按人口再按大洲过滤城市，并按字母顺序排序
string[] cities = { "Tokyo", "toronto", "Berlin", "Tbilisi", "Oslo" };
string[] tCities = cities
    .Where(c => c.Length > 4)
    .Where(c => char.ToLower(c[0]) == 't')
    .OrderBy(c => c, StringComparer.OrdinalIgnoreCase)
    .ToArray();
// 结果: ["Tbilisi", "Tokyo", "toronto"]
```

### 不区分大小写的比较

当不区分大小写比较字符时，`char.ToLower()` 或 `char.ToUpper()` 会在比较之前将两边转换为相同的大小写：

```csharp
char.ToLower('A') == char.ToLower('a')  // true
```

对于不区分大小写的排序，将 `StringComparer.OrdinalIgnoreCase` 传递给 `OrderBy` 可以确保 `"apple"` 和 `"Avocado"` 自然地排在一起，而不是所有大写字母都排在小写字母之前。

### 常用参考

| 方法 | 说明 |
| --- | --- |
| `.Where(predicate)` | 保留谓词返回 true 的元素 |
| `.OrderBy(keySelector)` | 按选定的键升序排序 |
| `.OrderBy(key, comparer)` | 使用自定义比较器升序排序 |
| `StringComparer.OrdinalIgnoreCase` | 忽略字母大小写的比较器 |
| `char.ToLower(c)` | 将字符转换为小写 |
| `string.Length` | 返回字符串中的字符数 |

### 你的任务

编写一个方法，对一个单词数组依次应用**三个过滤/排序阶段**：

1. **长度过滤** - 仅保留长度**至少**为 `minLength` 的单词。
2. **首字符过滤** - 在剩余的单词中，仅保留**首字符**与 `requiredStart` 匹配（不区分大小写）的单词。
3. **字母排序** - **按字母顺序**（忽略大小写）对剩余的单词进行排序。

将最终结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] FilterPipeline(string[] words, int minLength, char requiredStart)
```

### 预期结果

```less
FilterPipeline(["apple", "Avocado", "banana", "apricot", "cherry", "Almond"], 5, 'a')
  -> ["Almond", "apple", "apricot", "Avocado"]

FilterPipeline(["Cat", "car", "cider", "COOL"], 3, 'c')
  -> ["car", "Cat", "cider", "COOL"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FilterPipeline(string[] words, int minLength, char requiredStart)
    {
        return words
            .Where(w => w.Length >= minLength)                               // 长度过滤
            .Where(w => char.ToLower(w[0]) == char.ToLower(requiredStart))   // 首字符过滤（不区分大小写）
            .OrderBy(w => w, StringComparer.OrdinalIgnoreCase)               // 按字母顺序排序（忽略大小写）
            .ToArray();
    }
}
```
