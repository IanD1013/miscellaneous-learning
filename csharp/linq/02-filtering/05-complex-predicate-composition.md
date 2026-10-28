### 使用 LINQ Where 构建复合过滤谓词

在实际应用中，你很少只通过单一条件来过滤数据。
更多时候，你需要组合多个规则：查找所有处于活跃状态**且**消费超过 $100 的客户，或者检索所有有库存**或**处于预订状态的产品。
LINQ 的 `Where` 方法接收一个 lambda 谓词，而该谓词可以像任何 C# 布尔表达式一样复杂：使用 `&&`（AND）、`||`（OR）组合条件，调用字符串方法，执行数学运算等等。

### 工作原理

`Where` 方法会对序列中的每个元素评估一个谓词（一个返回 `bool` 的函数）。
只有谓词返回 `true` 的元素才会包含在结果中。
因为谓词只是一个常规的 C# 表达式，所以你可以使用以下任意组合：

- **逻辑运算符**：`&&`（两个条件都必须为 true）、`||`（至少一个必须为 true）、`!`（取反）
- **比较运算符**：`==`、`!=`、`>`、`<`、`>=`、`<=`
- **字符串方法**：`.StartsWith()`、`.Contains()`、`.ToLower()`、`.Length` 等
- **数学运算**：`%`（取模）、`Math.Abs()`、算术比较
- **圆括号**：用于控制求值顺序，就像在普通数学中一样

所有这些都写在**单个 `Where` 调用内部**，你无需为多个条件链式调用多个 `Where`。

### 语法

```csharp
// 单个条件
var result = source.Where(item => condition);

// 使用 AND 的复合谓词
var result = source.Where(item => conditionA && conditionB);

// 使用 OR 的复合谓词
var result = source.Where(item => conditionA || conditionB);

// 混合使用 AND、OR 和分组
var result = source.Where(item => (conditionA || conditionB) && conditionC);
```

### 示例

```csharp
int[] numbers = { 1, 12, 23, 34, 45, 56, 67 };

// 保留大于 10 并且为偶数的数字
int[] result1 = numbers.Where(n => n > 10 && n % 2 == 0).ToArray();
// result1: [12, 34, 56]

// 保留小于 5 或者大于 60 的数字
int[] result2 = numbers.Where(n => n < 5 || n > 60).ToArray();
// result2: [1, 67]

string[] cities = { "Austin", "Boston", "Atlanta", "Denver", "Anchorage" };

// 保留以 "A" 开头（不区分大小写）并且超过 6 个字符的城市
string[] result3 = cities.Where(c => char.ToLower(c[0]) == 'a' && c.Length > 6).ToArray();
// result3: ["Atlanta", "Anchorage"]

// 保留包含 "on" 或者以 "er" 结尾的城市
string[] result4 = cities.Where(c => c.Contains("on") || c.EndsWith("er")).ToArray();
// result4: ["Boston", "Denver"]
```

### 常见模式

| 模式 | 示例 |
| --- | --- |
| 两个条件使用 AND | `x => x.Age >= 18 && x.IsActive` |
| 两个条件使用 OR | `x => x.Status == "new" || x.Status == "pending"` |
| 组合取反 | `x => !x.IsDeleted && x.Price > 0` |
| 字符串比较（不区分大小写） | `x => char.ToLower(x[0]) == 'b'` |
| 长度检查 | `x => x.Name.Length >= 3` |

### 实用参考

| 方法 / 运算符 | 描述 | 示例 |
| --- | --- | --- |
| `char.ToLower(c)` | 将字符转换为小写 | `char.ToLower('A')` → `'a'` |
| `char.ToUpper(c)` | 将字符转换为大写 | `char.ToUpper('a')` → `'A'` |
| `string.Length` | 获取字符数 | `"hello".Length` → `5` |
| `string[0]` | 访问第一个字符 | `"hello"[0]` → `'h'` |
| `.Where(predicate)` | 根据布尔条件过滤元素 | 参见上方示例 |
| `.ToArray()` | 将结果转换回数组 | 返回 `string[]` 时需要 |

### 你的任务

编写一个方法，使用带有复合谓词的**单个 `Where` 调用**来过滤单词数组。
该方法接收：

- `words`：要过滤的字符串数组
- `minLength`：可接受的最小长度（包含此长度）
- `startChar`：单词必须以此字符开头（不区分大小写比较）

仅返回同时满足**两个**条件的单词，并保持它们的原始顺序。

注意边界情况：如果数组为空怎么办？
如果没有单词同时符合这两个条件怎么办？

### 方法签名

```csharp
public static string[] FilterByMultipleCriteria(string[] words, int minLength, char startChar)
```

### 预期结果

```less
FilterByMultipleCriteria(["cat", "apple", "ant", "ball", "amazing"], 4, 'a') -> ["apple", "amazing"]
FilterByMultipleCriteria(["Dog", "deer", "Dove", "duck"], 4, 'd') -> ["deer", "Dove", "duck"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] FilterByMultipleCriteria(string[] words, int minLength, char startChar)
    {
        // 单个 Where：长度至少为 minLength，并且首字符（不区分大小写）与 startChar 相同
        return words
            .Where(w => w.Length >= minLength && char.ToLower(w[0]) == char.ToLower(startChar))
            .ToArray();
    }
}
```
