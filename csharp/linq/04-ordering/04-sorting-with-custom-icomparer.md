### 在 LINQ 排序运算符中使用自定义比较器

LINQ 的 `OrderBy` 方法通常与简单的键选择器（如 `x => x.Length` 或 `x => x.Name`）一起使用。
但有时你需要的排序逻辑不仅限于选择单个键，你可能需要以更细致的方式比较两个元素。
对于这些情况，`OrderBy` 有一个接收 `IComparer<T>` 的重载，让你可以完全控制两个元素之间的比较方式。

### 工作原理

`IComparer<T>` 是一个只包含单个方法 `Compare(T x, T y)` 的接口。
它返回：

- 一个**负数**：如果 `x` 应该排在 `y` 之前
- **零**：如果它们被视为相等
- 一个**正数**：如果 `x` 应该排在 `y` 之后

当你向 `OrderBy` 传递一个比较器时，LINQ 会使用它来代替默认的比较逻辑。
该排序是**稳定**的，这意味着比较结果相等的元素将保留输入中的原始相对顺序。

### 语法

```csharp
// 使用自定义比较器的 OrderBy
collection.OrderBy(element => element, customComparer)
```

你并不总是需要编写一个完整的类来实现 `IComparer<T>`。
C# 提供了一个便捷的工厂方法：

```csharp
// 使用 lambda 内联创建比较器
var comparer = Comparer<T>.Create((x, y) => /* 比较逻辑 */);
```

Lambda 表达式接收两个元素，并且必须按照负数/零/正数的约定返回一个 `int`。

### 示例

```csharp
// 按绝对值对整数排序
int[] numbers = { -5, 3, -1, 4, -2 };
var absComparer = Comparer<int>.Create((a, b) =>
    Math.Abs(a).CompareTo(Math.Abs(b)));
var sorted = numbers.OrderBy(n => n, absComparer).ToArray();
// 结果：[-1, -2, 3, 4, -5]
// 注意：-1 和 -2 的绝对值都很小；-1 原本就排在前面（稳定排序）

// 按长度对字符串排序，长度相同时按字母顺序
string[] cities = { "Rome", "Paris", "Tokyo", "Lima" };
var lengthThenAlpha = Comparer<string>.Create((a, b) =>
{
    int result = a.Length.CompareTo(b.Length);
    return result != 0 ? result : string.Compare(a, b, StringComparison.Ordinal);
});
var sortedCities = cities.OrderBy(c => c, lengthThenAlpha).ToArray();
// 结果：["Lima", "Rome", "Paris", "Tokyo"]
```

### 核心概念

- 大多数内置类型（`int`、`char`、`string`）都提供了 `CompareTo`，并返回比较器所需的负数/零/正数模式。
- C# 中的 `char` 可以直接进行比较：`'a'.CompareTo('z')` 返回一个负数，因为 `'a'` 排在 `'z'` 之前。
- 你可以使用 `s[s.Length - 1]` 访问字符串的最后一个字符。
- 带有比较器的 `OrderBy` 会将**自身**元素（元素本身）作为键传递，因为比较器会处理所有的比较逻辑。

### 你的任务

编写一个方法，接收一个字符串数组并按其**最后一个字符**按升序排序。
使用带有通过 `Comparer<string>.Create(...)` 创建的自定义比较器的 `OrderBy`。
由于 `OrderBy` 执行稳定排序，最后一个字符相同的单词应保留其原始相对顺序。

### 方法签名

```csharp
public static string[] SortByLastChar(string[] words)
```

### 预期结果

```css
SortByLastChar(["apple", "banana", "cherry", "date"]) -> ["banana", "apple", "date", "cherry"]
SortByLastChar(["red", "blue", "green"]) -> ["red", "blue", "green"]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static string[] SortByLastChar(string[] words)
    {
        // 自定义比较器：比较两个字符串的最后一个字符
        var lastCharComparer = Comparer<string>.Create((a, b) =>
            a[a.Length - 1].CompareTo(b[b.Length - 1]));

        // 把元素本身作为键，交给比较器处理比较逻辑（稳定排序）
        return words.OrderBy(w => w, lastCharComparer).ToArray();
    }
}
```
