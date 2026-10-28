### 避免 LINQ 中的 N+1 查找反模式

在大量使用 LINQ 的 C# 代码中，最常见的性能陷阱之一就是 **N+1 查找模式**：在循环或另一个 LINQ 投影内部执行线性搜索（`Where`、`FirstOrDefault` 或嵌套查询）。
这会悄无声息地将一个*看起来*简单的操作变成具有 **O(N × M)** 时间复杂度的操作，其中 N 是正在迭代的元素数量，M 是正在搜索的集合大小。
在包含数千个元素的生产代码中，这可能会比预期慢上数个数量级。

### 反模式是如何发生的

考虑两个并行数组：一个包含员工 ID，另一个包含他们的薪资。
你想要查找部分员工的薪资。
一种朴素的做法是在投影内部嵌套搜索：

```csharp
// ❌ 反模式：O(N × M)，对每一个键都做一次线性搜索
var results = requestedIds
    .Select(id => allIds
        .Where(x => x == id)   // 对每个 requestedId 都扫描一遍 allIds
        .Select((x, i) => salaries[i])
        .FirstOrDefault())
    .ToArray();
```

对于针对 10,000 条记录查询 1,000 个请求 ID 的情况，这最多会执行 **1000 万次**比较。
修复方法是预先构建一个索引结构，以实现每次查找 **O(1)** 的访问时间。

### 修复方法：先构建 Dictionary

`Dictionary<TKey, TValue>` 提供常数时间的查找。
构建它只需一次性消耗 O(M) 的开销，随后的每次查找都是 O(1)，从而使总开销变为 **O(N + M)** 而不是 O(N × M)。

### 语法

```csharp
// 从集合构建 dictionary
Dictionary<TKey, TValue> map = collection.ToDictionary(
    item => item.KeyProperty,    // 键选择器
    item => item.ValueProperty   // 值选择器
);

// 使用 TryGetValue 安全查找
if (map.TryGetValue(someKey, out var result))
{
    // 使用 result
}
```

### 示例

```csharp
// 示例 1：将产品代码映射到价格
string[] codes = { "WDG", "GDT", "CBL" };
decimal[] prices = { 9.99m, 24.99m, 4.50m };

var priceMap = codes
    .Select((code, i) => new { Code = code, Price = prices[i] })
    .ToDictionary(x => x.Code, x => x.Price);

// O(1) 查找：
decimal widgetPrice = priceMap["WDG"]; // 9.99

// 示例 2：使用 Zip 从并行数组构建查找表
var zipped = codes.Zip(prices, (c, p) => (Code: c, Price: p));
var priceMap2 = zipped.ToDictionary(x => x.Code, x => x.Price);

// 示例 3：带回退值的安全查找
string[] wanted = { "GDT", "XYZ" };
var results = wanted
    .Select(w => priceMap.TryGetValue(w, out var p) ? p : -1m)
    .ToArray();
// results: [24.99, -1]
```

### 常见模式

| 模式 | 时间复杂度 | 何时使用 |
| --- | --- | --- |
| 循环内的 `list.Where(x => x.Id == target)` | O(N × M) | **绝不**用于重复查找 |
| `ToDictionary` + 索引查找 | O(N + M) | 唯一键，每个键对应一个值 |
| `ToLookup` + 索引查找 | O(N + M) | 重复键，每个键对应多个值 |
| `HashSet` + `Contains` | O(N + M) | 仅用于存在性检查 |

### 常用参考

| 方法 | 描述 |
| --- | --- |
| `ToDictionary(keySelector, valueSelector)` | 从序列构建 `Dictionary`；遇到重复键时抛出异常 |
| `TryGetValue(key, out value)` | 如果键存在则返回 `true` 并设置 `value`；避免抛出 `KeyNotFoundException` |
| `Select((item, index) => ...)` | 同时提供元素索引及其值的重载 |
| `Zip(other, resultSelector)` | 逐个元素配对来自两个序列的元素 |

### 你的任务

编写一个接收三个参数的方法：

- `keys`：一个字符串数组，表示需要查找的键
- `allKeys`：包含所有可用键的数组（保证唯一）
- `allValues`：并行的整数值数组（与 `allKeys` 长度相同，其中 `allValues[i]` 对应 `allKeys[i]`）

返回一个 `int[]`，其中每个元素是与 `keys` 中对应键关联的值。
如果在 `allKeys` 中未找到某个键，则在该位置返回 `-1`。
结果必须保持 `keys` 的原有顺序。

**性能要求：** 你的解决方案必须预先构建一个 dictionary 并执行 O(1) 查找，不要在投影内使用嵌套搜索。

### 方法签名

```csharp
public static int[] BatchLookup(string[] keys, string[] allKeys, int[] allValues)
```

### 预期结果

```css
BatchLookup(["b", "a", "c"], ["a", "b", "c", "d"], [10, 20, 30, 40]) -> [20, 10, 30]
BatchLookup(["x"], ["a", "b"], [1, 2]) -> [-1]
BatchLookup(["a", "a"], ["a"], [42]) -> [42, 42]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int[] BatchLookup(string[] keys, string[] allKeys, int[] allValues)
    {
        // 预先构建键到值的 dictionary，只需 O(M)
        Dictionary<string, int> map = allKeys
            .Select((key, i) => new { Key = key, Value = allValues[i] })
            .ToDictionary(x => x.Key, x => x.Value);

        // 按 keys 的顺序做 O(1) 查找，找不到时返回 -1
        return keys
            .Select(k => map.TryGetValue(k, out var v) ? v : -1)
            .ToArray();
    }
}
```
