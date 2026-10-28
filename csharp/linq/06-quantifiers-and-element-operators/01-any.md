### LINQ 中的 `Any` 量词

在处理集合时，最常见的问题之一是：*“是否至少有一个元素满足某个条件？”*
与其手动编写循环并跟踪布尔标志，LINQ 提供了 `Any()`，这是一个量词方法，可以通过单次且富有表现力的调用来回答这个问题。

### 工作原理

`Any()` 有两种形式：

1. **无参数** - `sequence.Any()` 如果序列包含**至少一个元素**（即非空），则返回 `true`。
2. **带谓词（predicate）** - `sequence.Any(predicate)` 如果**至少有一个元素**满足给定条件，则返回 `true`。

这两种形式都支持**短路求值**（short-circuit）：一旦找到符合条件的元素，它们就会立即停止遍历。
如果第一个元素就匹配，则绝不会检查集合中的其余元素。
这使得 `Any()` 即使在大型集合上，只要较早出现匹配项，也能保持高效。

### 语法

```csharp
// 集合中是否包含任何元素？
bool hasElements = collection.Any();

// 是否至少有一个元素满足该条件？
bool hasMatch = collection.Any(element => condition);
```

谓词是一个 lambda 表达式，它接收一个元素并返回一个 `bool`。

### 示例

```csharp
// 检查温度列表中是否有高于沸点的读数
int[] temps = { 85, 99, 101, 76 };
bool hasBoiling = temps.Any(t => t > 100);  // true (101 > 100)

// 检查是否有学生的姓名以 'Z' 开头
string[] students = { "Alice", "Ben", "Clara" };
bool hasZ = students.Any(s => s.StartsWith("Z"));  // false

// 检查集合是否非空
List<string> items = new List<string>();
bool hasItems = items.Any();  // false (空列表)

items.Add("widget");
bool hasItemsNow = items.Any();  // true
```

### 短路求值实战

假设一个包含 100 万个元素的集合，其中第二个元素满足条件。
`Any()` 会检查元素 0，然后检查元素 1，发现匹配项，并立即返回 `true`，而不会检查剩下的 999,998 个元素。
相比之下，`Count(predicate) > 0` 或 `Where(predicate).Count() > 0` 等方法则会不必要地遍历**整个**集合。

### 常见模式

| 模式 | 用途 |
| --- | --- |
| `list.Any()` | 检查集合是否非空 |
| `list.Any(x => x == target)` | 检查是否存在特定值 |
| `list.Any(x => x > threshold)` | 检查是否有任何值超过阈值 |
| `list.Any(x => x.Contains("keyword"))` | 检查是否有任何字符串包含子字符串 |

### 你的任务

编写一个方法，用于判断整数数组中是否包含**至少一个负数**。
如果有任何元素为负数，则返回 `true`，否则返回 `false`。

请考虑以下情况：

- 正数和负数混合的数组
- 全部为正数的数组
- 空数组（没有任何元素）
- 每个元素都是负数的数组
- 包含零的数组（零不是负数）

### 方法签名

```csharp
public static bool HasNegative(int[] numbers)
```

### 预期结果

```scss
HasNegative([1, 2, -3, 4])  -> True
HasNegative([1, 2, 3])      -> False
HasNegative([])              -> False
HasNegative([-1, -2, -3])   -> True
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static bool HasNegative(int[] numbers)
    {
        // 只要有一个元素小于 0 就返回 true，空数组返回 false
        return numbers.Any(n => n < 0);
    }
}
```
