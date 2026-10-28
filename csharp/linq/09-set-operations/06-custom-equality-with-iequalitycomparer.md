### 在 LINQ 集合操作符中使用自定义相等性比较器

LINQ 的集合操作符，`Distinct`、`Union`、`Intersect` 和 `Except`，都是使用 `IEqualityComparer<T>` 来确定元素是否相等的。
默认情况下，它们使用 `EqualityComparer<T>.Default`，对于字符串来说，这意味着区分大小写的序号比较。
当你的业务领域需要不同的相等性语义（例如不区分大小写的匹配、仅比较某些属性、基于容差的数值相等性）时，你可以向这些操作符中的任何一个提供自定义比较器。

### 工作原理

每个集合操作符都有一个重载，接受一个 `IEqualityComparer<T>` 作为第二个参数。
比较器定义了两件事：如何测试两个元素之间的相等性，以及如何为某个元素计算哈希码。
当你传入一个比较器时，操作符会使用它来代替默认的比较逻辑。
这意味着如果你的比较器忽略大小写，`"Hello"` 和 `"hello"` 就可以被视为同一个元素。

### 语法

```csharp
// 任意集合操作符搭配比较器的通用模式
sequence.Distinct(comparer)
sequence1.Union(sequence2, comparer)
sequence1.Intersect(sequence2, comparer)
sequence1.Except(sequence2, comparer)
```

### 示例

```csharp
// 示例 1：对两个邮箱列表进行不区分大小写的并集
string[] teamA = { "alice@co.com", "Bob@co.com" };
string[] teamB = { "ALICE@co.com", "carol@co.com" };
var allEmails = teamA.Union(teamB, StringComparer.OrdinalIgnoreCase);
// 结果：{ "alice@co.com", "Bob@co.com", "carol@co.com" }
// 注意：Union 会保留首次出现时的大小写

// 示例 2：不区分大小写的交集
string[] requested = { "READ", "Write", "DELETE" };
string[] allowed   = { "read", "write" };
var granted = requested.Intersect(allowed, StringComparer.OrdinalIgnoreCase);
// 结果：{ "READ", "Write" }

// 示例 3：不区分大小写的 Except（差集）
string[] allTags   = { "CSharp", "LINQ", "dotnet", "csharp" };
string[] banned    = { "csharp" };
var filtered = allTags.Except(banned, StringComparer.OrdinalIgnoreCase);
// 结果：{ "LINQ", "dotnet" }
```

### 内置的字符串比较器

`StringComparer` 类提供了几个现成的比较器：

| 比较器 | 行为 |
| --- | --- |
| `StringComparer.Ordinal` | 区分大小写，二进制比较 |
| `StringComparer.OrdinalIgnoreCase` | 不区分大小写，二进制比较 |
| `StringComparer.CurrentCulture` | 区分大小写，受区域文化影响 |
| `StringComparer.CurrentCultureIgnoreCase` | 不区分大小写，受区域文化影响 |
| `StringComparer.InvariantCultureIgnoreCase` | 不区分大小写，独立于区域文化 |

对于大多数不关心区域文化的编程场景（如标识符、标签、代码），`OrdinalIgnoreCase` 是最佳选择，它既快速又可预测。

### 关于集合操作符的重要细节

当 `Distinct` 遇到重复项时，它会保留**第一个**出现的元素并丢弃后面的元素。
这意味着保留下来的元素的大小写取决于输入的顺序。
如果无论输入顺序如何你都需要一致的输出格式，则需要在去重后进行规范化。

### 你的任务

编写一个方法，接收一个单词数组，并返回一个去重后的数组，其中仅大小写不同的单词被视为相同。
返回的数组应包含每个唯一的**小写**单词，并按**字母顺序**排序。

例如：

- 输入 `["Apple", "apple", "BANANA"]` → 去重后的单词（忽略大小写）为 `Apple` 和 `BANANA`，然后转换为小写并排序 → `["apple", "banana"]`

### 方法签名

```csharp
public static string[] DistinctIgnoreCase(string[] words)
```

### 预期结果

```css
DistinctIgnoreCase(["Apple", "apple", "BANANA", "banana", "Cherry"]) -> ["apple", "banana", "cherry"]
DistinctIgnoreCase(["hello", "HELLO", "Hello"]) -> ["hello"]
DistinctIgnoreCase(["Zebra", "alpha", "ALPHA", "zebra", "Mango"]) -> ["alpha", "mango", "zebra"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] DistinctIgnoreCase(string[] words)
    {
        // 使用不区分大小写的比较器去重，然后转换为小写并按字母顺序排序
        return words
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .Select(w => w.ToLower())
            .OrderBy(w => w)
            .ToArray();
    }
}
```
