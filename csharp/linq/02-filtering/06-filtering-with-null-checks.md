### 使用 LINQ Where 安全过滤可空值

在处理实际数据时，集合中经常会包含 `null` 或空值，它们可能来自数据库查询、用户输入或 API 响应。
如果在 `Where` 谓词中盲目访问元素的属性或方法而没有预先检查 `null`，程序将会因抛出 `NullReferenceException` 而崩溃。
学会防范这些值是一项基本的防御性编程技能。

### 工作原理

LINQ 的 `Where` 方法会遍历序列中的每个元素，并且仅保留谓词返回 `true` 的元素。
当元素可能为 `null` 时，谓词本身必须在对该元素执行任何其他操作**之前**处理这种可能性。
如果你尝试对 `null` 引用调用 `.Length`、`.ToUpper()` 或任何其他成员，运行时将立即抛出异常。

核心要点：**你的谓词负责确保安全性**。
`Where` 方法不会自动跳过 null，它会将每个元素（包括 null）都传递给你的谓词。

### 语法

```csharp
// 带 null 安全的过滤通用模式
sequence.Where(element => element != null && /* 其他条件 */)
```

C# 还为常见的 null 检查场景提供了便捷的辅助方法：

```csharp
string.IsNullOrEmpty(s)      // 如果 s 为 null 或者 s 为 "" 则为 true
string.IsNullOrWhiteSpace(s) // 如果 s 为 null、"" 或者仅包含空白字符则为 true
```

### 示例

```csharp
// 示例 1：从可空数组中过滤掉 null 整数
int?[] scores = { 95, null, 82, null, 71 };
int?[] validScores = scores.Where(s => s != null).ToArray();
// 结果: { 95, 82, 71 }

// 示例 2：只保留非 null、非空的城市名称
string[] cities = { "Paris", null, "", "Tokyo", null, "Lima" };
string[] realCities = cities.Where(c => !string.IsNullOrEmpty(c)).ToArray();
// 结果: { "Paris", "Tokyo", "Lima" }

// 示例 3：没有 null 防护时会发生什么（危险！）
string[] names = { "Alice", null, "Bob" };
// 这会在遇到 null 元素时崩溃：
// names.Where(n => n.Length > 3).ToArray(); // NullReferenceException!

// 安全版本：
string[] longNames = names.Where(n => n != null && n.Length > 3).ToArray();
// 结果: { "Alice" }
```

### 常见模式

| 模式 | 作用 |
| --- | --- |
| `x != null` | 检查引用不为 null |
| `string.IsNullOrEmpty(x)` | 如果 `x` 为 `null` 或 `""` 则返回 `true` |
| `string.IsNullOrWhiteSpace(x)` | 如果 `x` 为 `null`、`""` 或仅包含空白字符则返回 `true` |
| `!condition` | 取反，用于**保留**不为 null/空的元素 |

### 你的任务

编写一个方法，接收一个字符串数组（可能包含 `null` 值和空字符串），并返回一个仅包含**非 null**且**非空**元素的新数组。
必须保留剩余元素的顺序。

### 方法签名

```csharp
public static string[] RemoveNulls(string[] items)
```

### 预期结果

```css
RemoveNulls(["hello", null, "world", "", "!"]) -> ["hello", "world", "!"]
RemoveNulls([null, null, null]) -> []
RemoveNulls(["a", "b", "c"]) -> ["a", "b", "c"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] RemoveNulls(string[] items)
    {
        // 只保留既不是 null 也不是空字符串的元素
        return items.Where(s => !string.IsNullOrEmpty(s)).ToArray();
    }
}
```
