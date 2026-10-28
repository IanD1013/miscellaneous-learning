### 使用 LINQ Where 和字符串谓词过滤字符串

LINQ 的 `Where` 方法是一个强大的工具，用于根据你在 lambda 表达式中定义的条件来过滤集合。
在处理字符串集合时，你可以在 lambda 谓词中调用**任何字符串方法**：`StartsWith`、`EndsWith`、`Contains`、`ToUpper`、`ToLower`，甚至是字符级检查，如 `char.IsDigit` 或 `char.IsUpper`。
这让你可以表达丰富且可读性强的过滤逻辑，而无需编写手动循环。

### 工作原理

`Where` 接收一个 lambda 表达式，该表达式接收每个元素并返回 `true` 或 `false`。
结果中仅包含 lambda 返回 `true` 的元素。
由于每个元素都是一个 `string`，因此你可以在谓词内部访问完整的 `System.String` API。

### 语法

```csharp
string[] result = collection
    .Where(item => item.SomeStringMethod(...))
    .ToArray();
```

谓词可以使用 `&&`（与）或 `||`（或）组合多个条件：

```csharp
.Where(item => item.Length > 3 && item.Contains("x"))
```

### 示例

过滤以 "ton" 结尾的城市名称：

```csharp
string[] cities = { "Houston", "Boston", "Denver", "Hamilton" };
string[] result = cities
    .Where(c => c.EndsWith("ton", StringComparison.OrdinalIgnoreCase))
    .ToArray();
// result: ["Houston", "Boston", "Hamilton"]
```

过滤包含数字的产品代码：

```csharp
string[] codes = { "AB-X", "C3PO", "HELLO", "R2D2" };
string[] result = codes
    .Where(c => c.Any(ch => char.IsDigit(ch)))
    .ToArray();
// result: ["C3PO", "R2D2"]
```

过滤以大写字母开头的名称：

```csharp
string[] names = { "alice", "Bob", "charlie", "Diana" };
string[] result = names
    .Where(n => char.IsUpper(n[0]))
    .ToArray();
// result: ["Bob", "Diana"]
```

### 实用参考

| 方法 / 属性 | 说明 | 示例 |
| --- | --- | --- |
| `StartsWith(string)` | 检查字符串是否以某个值开头 | `"hello".StartsWith("he")` → `true` |
| `EndsWith(string)` | 检查字符串是否以某个值结尾 | `"hello".EndsWith("lo")` → `true` |
| `Contains(string)` | 检查字符串是否包含子字符串 | `"hello".Contains("ell")` → `true` |
| `ToLower()` / `ToUpper()` | 转换大小写 | `"Hi".ToLower()` → `"hi"` |
| `char.IsLetter(c)` | 检查字符是否为字母 | `char.IsLetter('A')` → `true` |
| `string[0]` | 访问第一个字符 | `"apple"[0]` → `'a'` |

### 你的任务

编写一个方法，接收一个单词数组，并仅返回**以元音字母开头**（a, e, i, o, u）的单词。
检查必须是**不区分大小写**的，因此以 `'A'` 或 `'a'` 开头的单词均符合条件。
将匹配的单词按原始顺序作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] GetVowelStarters(string[] words)
```

### 预期结果

```css
GetVowelStarters(["apple", "banana", "orange", "grape", "avocado"]) -> ["apple", "orange", "avocado"]
GetVowelStarters(["Ice", "Fire", "Earth", "Water"]) -> ["Ice", "Earth"]
GetVowelStarters(["sky", "cloud", "rain"]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] GetVowelStarters(string[] words)
    {
        // 把首字符转为小写，再检查它是否是元音字母
        return words.Where(w => "aeiou".Contains(char.ToLower(w[0]))).ToArray();
    }
}
```
