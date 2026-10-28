### 在 LINQ 中使用 StringComparer 对字符串进行排序

在 C# 中对字符串进行排序时，`OrderBy` 的默认行为使用的是**序号比较（ordinal comparison）**，这意味着它是根据字符的 Unicode 数值进行排序的。
这会产生一个出人意料的结果：所有大写字母（`A`–`Z`，Unicode 65–90）都会排在所有小写字母（`a`–`z`，Unicode 97–122）**之前**。
因此，在默认排序中 `"Zebra"` 会出现在 `"apple"` 之前，这并不是大多数用户期望的字母顺序。

要实现不区分大小写的字母顺序排序，你可以将 **`StringComparer`** 作为第二个参数传递给 `OrderBy`。

### 工作原理

LINQ 的 `OrderBy` 方法有一个接受 `IComparer<T>` 的重载。
`StringComparer` 类提供了几个内置比较器，用于控制两个字符串的比较方式：

| 比较器 | 行为 |
| --- | --- |
| `StringComparer.Ordinal` | 默认值 - 区分大小写，基于 Unicode 数值 |
| `StringComparer.OrdinalIgnoreCase` | 忽略字母大小写，仍然使用 Unicode 排序规则 |
| `StringComparer.CurrentCulture` | 区分大小写，遵循当前区域性（culture）的排序规则 |
| `StringComparer.CurrentCultureIgnoreCase` | 忽略大小写，遵循特定区域性的排序规则 |

当比较器认为两个字符串相等时（例如在不区分大小写的比较下的 `"apple"` 和 `"Apple"`），它们在输入中的原始顺序会被保留，因为 `OrderBy` 是一种**稳定排序（stable sort）**。

### 语法

```csharp
// 默认的区分大小写排序
var sorted = collection.OrderBy(item => item);

// 传入 StringComparer 进行自定义比较
var sorted = collection.OrderBy(item => item, StringComparer.SomeComparer);
```

### 示例

```csharp
// 默认的序号排序 - 大写字母排在前面
var cities = new[] { "paris", "Berlin", "amsterdam", "Cairo" };
var defaultSort = cities.OrderBy(c => c).ToArray();
// 结果：["Berlin", "Cairo", "amsterdam", "paris"]
// 注意：B (66) 和 C (67) 排在 a (97) 和 p (112) 之前

// 不区分大小写的序号排序 - 真正的字母顺序
var betterSort = cities.OrderBy(c => c, StringComparer.OrdinalIgnoreCase).ToArray();
// 结果：["amsterdam", "Berlin", "Cairo", "paris"]
// 现在无论大小写都按字母顺序排序

// 区分区域性的不区分大小写排序
var culturalSort = cities.OrderBy(c => c, StringComparer.CurrentCultureIgnoreCase).ToArray();
// 结果：["amsterdam", "Berlin", "Cairo", "paris"]
// 这里结果相同，但对于特定区域的字符（例如 ö、ñ）会有所不同
```

### 查看差异

```csharp
var names = new[] { "eve", "Alice", "bob", "Dave", "carol" };

// 默认：["Alice", "Dave", "bob", "carol", "eve"]
var caseSensitive = names.OrderBy(n => n).ToArray();

// 不区分大小写：["Alice", "bob", "carol", "Dave", "eve"]
var caseInsensitive = names.OrderBy(n => n, StringComparer.OrdinalIgnoreCase).ToArray();
```

注意默认排序是如何先将所有以大写字母开头的名字归为一组，而不区分大小写的排序则会生成真正的字母顺序。

### 你的任务

编写一个方法，接收一个字符串数组，并返回按**字母顺序**（忽略大小写）排序后的数组。
输出中应保留每个单词的原始大小写，仅排序顺序不区分大小写。

排序时使用序号不区分大小写（ordinal case-insensitive）比较。

### 方法签名

```csharp
public static string[] SortCaseInsensitive(string[] words)
```

### 预期结果

```css
SortCaseInsensitive(["Banana", "apple", "Cherry", "date"]) -> ["apple", "Banana", "Cherry", "date"]
SortCaseInsensitive(["Zoo", "alpha", "BETA"]) -> ["alpha", "BETA", "Zoo"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] SortCaseInsensitive(string[] words)
    {
        // 使用序号不区分大小写的比较器排序，保留单词原始大小写
        return words.OrderBy(w => w, StringComparer.OrdinalIgnoreCase).ToArray();
    }
}
```
