### ToDictionary - 构建键值查找

当你有一个元素序列并且需要通过某个属性进行快速的 O(1) 查找时，LINQ 的 `ToDictionary` 方法只需一次调用即可将该序列转换为 `Dictionary<TKey, TValue>`。
这比手动循环并插入条目要更具可读性且更加简洁，并且这是一个你会经常使用的模式，例如通过 ID 映射数据库记录、按名称为配置项建立索引，或从内存集合构建缓存。

### 工作原理

`ToDictionary` 遍历源序列中的每个元素，并应用两个选择器函数：

1. **键选择器**（Key Selector） - 从每个元素中提取或计算字典的键
2. **元素选择器**（Element Selector） - 从每个元素中提取或计算字典的值

如果任意两个元素产生了**相同的键**，在运行时将会抛出 `ArgumentException`。
这是一个重要的保证：该方法强制唯一性，而不是静默覆盖条目。

### 语法

```csharp
// 完整签名
Dictionary<TKey, TValue> result = source.ToDictionary(
    element => /* 键表达式 */,
    element => /* 值表达式 */
);

// 如果元素本身就是值，可以省略第二个选择器：
Dictionary<TKey, TSource> result = source.ToDictionary(
    element => /* 键表达式 */
);
```

### 示例

```csharp
// 将国家代码映射到国家名称
var countries = new[] { ("US", "United States"), ("DE", "Germany"), ("JP", "Japan") };
var lookup = countries.ToDictionary(c => c.Item1, c => c.Item2);
// lookup["DE"] => "Germany"

// 将产品映射到其价格
var products = new[] { ("Keyboard", 49.99), ("Mouse", 29.99), ("Monitor", 299.99) };
var priceMap = products.ToDictionary(p => p.Item1, p => p.Item2);
// priceMap["Mouse"] => 29.99

// 重复的键会导致异常！
var items = new[] { "apple", "banana", "apple" };
// items.ToDictionary(x => x, x => x.Length);  // 抛出 ArgumentException！
```

### 使用生成的字典

一旦你拥有了一个 `Dictionary<TKey, TValue>`，就可以遍历它的键值对、对它们进行排序以及转换：

```csharp
// 遍历并格式化
var scores = new Dictionary<string, int> { ["Alice"] = 95, ["Bob"] = 87 };
foreach (var kvp in scores.OrderBy(kvp => kvp.Key))
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出：Alice: 95
//       Bob: 87
```

### 常用参考

| 方法 / 属性 | 描述 |
| --- | --- |
| `.ToDictionary(keySelector, valueSelector)` | 从序列创建字典 |
| `.OrderBy(kvp => kvp.Key)` | 按键对字典条目进行排序 |
| `.Select(kvp => ...)` | 转换每个键值对 |
| `kvp.Key` / `kvp.Value` | 访问 `KeyValuePair` 的键或值 |

### 你的任务

编写一个方法，接收一个包含**唯一**单词的数组，构建一个将每个单词映射到其字符长度的字典，然后将这些条目按单词**字母升序排序**，并以 `"word=length"` 格式的字符串数组形式返回。

例如，给定 `["cat", "dog", "elephant"]`，字典将包含 `{"cat": 3, "dog": 3, "elephant": 8}`，排序后的输出将为 `["cat=3", "dog=3", "elephant=8"]`。

### 方法签名

```csharp
public static string[] BuildLengthMap(string[] words)
```

### 预期结果

```css
BuildLengthMap(["cat", "dog", "elephant"]) -> ["cat=3", "dog=3", "elephant=8"]
BuildLengthMap(["hello"]) -> ["hello=5"]
BuildLengthMap([]) -> []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static string[] BuildLengthMap(string[] words)
    {
        // 构建 单词 -> 长度 的字典
        Dictionary<string, int> lengthMap = words.ToDictionary(w => w, w => w.Length);

        // 按键字母升序排序，并格式化为 "word=length"
        return lengthMap
            .OrderBy(kvp => kvp.Key)
            .Select(kvp => $"{kvp.Key}={kvp.Value}")
            .ToArray();
    }
}
```
