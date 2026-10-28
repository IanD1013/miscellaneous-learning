### LINQ 中的 Single 和 SingleOrDefault

在处理集合时，有时你在设计上就已经知道某个查询应该返回**恰好一个**元素：不是零个，不是两个，就是仅仅一个。
LINQ 专门为此契约提供了两个操作符：`Single` 和 `SingleOrDefault`。
它们比 `First` 或 `FirstOrDefault` 更加严格，因为它们强制执行唯一性，能够捕获本可能被忽略的重复匹配 bug。

### 它们的工作原理

**`Single(predicate)`** 扫描集合中与谓词匹配的元素。
如果找到恰好一个匹配项，它将返回该元素。
如果找到 **0** 个匹配项，它会抛出 `InvalidOperationException`。
如果找到**多于一个**匹配项，它也会抛出 `InvalidOperationException`。
这是一个严格的契约：“必须恰好存在一个”。

**`SingleOrDefault(predicate)`** 在“零匹配”的情况下稍微宽容一些。
如果找到恰好一个匹配项，它将返回该元素。
如果找到 **0** 个匹配项，它会返回该类型的**默认值**（`int` 为 `0`，引用类型为 `null`，`bool` 为 `false` 等）。
但是，如果找到**多于一个**匹配项，它仍然会抛出 `InvalidOperationException`。
它的契约是：“最多只能存在一个”。

### 语法

```csharp
// 零个或多个匹配项时抛出异常
var result = collection.Single(item => condition);

// 零个匹配项时返回默认值，多个匹配项时抛出异常
var result = collection.SingleOrDefault(item => condition);
```

### 示例

```csharp
// 示例 1：查找唯一的管理员用户
var users = new[] { "alice", "bob", "admin", "carol" };
string admin = users.Single(u => u == "admin"); // "admin"

// 示例 2：查找一个可能存在的 VIP 客户
var customers = new[] { "Regular", "Regular", "Regular" };
string vip = customers.SingleOrDefault(c => c == "VIP"); // null（没有匹配项，string 的默认值）

// 示例 3：对整数使用 Single
var ids = new[] { 10, 20, 30, 40 };
int found = ids.Single(id => id > 25 && id < 35); // 30（恰好一个匹配项）

// 示例 4：对整数使用 SingleOrDefault
var scores = new[] { 88, 92, 75, 100 };
int perfect = scores.SingleOrDefault(s => s > 100); // 0（没有匹配项，int 的默认值）

// 示例 5：这会抛出异常（THROW），因为有多个元素匹配
// var nums = new[] { 5, 10, 15, 20 };
// int result = nums.Single(n => n > 8); // InvalidOperationException！（10、15、20 都匹配）
```

### 何时使用哪一个

| 操作符 | 零匹配 | 一个匹配 | 多个匹配 |
| --- | --- | --- | --- |
| `Single` | ❌ 抛出异常 | ✅ 返回元素 | ❌ 抛出异常 |
| `SingleOrDefault` | ✅ 返回默认值 | ✅ 返回元素 | ❌ 抛出异常 |

当你的逻辑保证存在匹配项且在不存在时希望抛出错误时，使用 `Single`。
当不存在匹配项是一个有效场景，但重复项仍然属于 bug 时，使用 `SingleOrDefault`。

### 你的任务

编写一个方法，该方法接收一个整数数组，并返回数组中的**唯一负数**；如果没有负数，则返回 `0`。
你可以假设输入中绝不会包含超过一个负数。

### 方法签名

```csharp
public static int GetOnlyNegative(int[] numbers)
```

### 预期结果

```scss
GetOnlyNegative([1, 2, -3, 4, 5]) -> -3
GetOnlyNegative([1, 2, 3])        -> 0
GetOnlyNegative([10, -7, 20])     -> -7
GetOnlyNegative([])                -> 0
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int GetOnlyNegative(int[] numbers)
    {
        // 最多只有一个负数：找到则返回它，没有则返回默认值 0
        return numbers.SingleOrDefault(n => n < 0);
    }
}
```
