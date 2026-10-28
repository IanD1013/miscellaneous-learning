### LINQ 管道实践：链式转换

实际开发中的数据处理很少只涉及单个操作。
开发者经常会将多个 LINQ 方法链接成一个**管道（pipeline）**：每一个步骤都会对流经它的数据进行细化、重塑或过滤。
掌握这种模式对于编写富有表现力且易读的 C# 代码至关重要。

本次终极挑战综合了你学过的五个核心 LINQ 方法：`SelectMany`、`Where`、`Select`、`Distinct` 和 `OrderBy`。

### 管道的工作原理

每个 LINQ 方法接收一个序列并生成一个新序列。
因为它们都操作 `IEnumerable<T>`，所以你可以使用点（`.`）操作符将它们链接起来。
上一步的输出会成为下一步的输入，就像水流过一系列过滤器一样。

```css
源数据 → 扁平化 → 过滤 → 转换 → 去重 → 排序 → 结果
```

顺序非常重要。
在转换之前进行过滤意味着你根据原始值进行过滤；在转换之后过滤则意味着你根据转换后的值进行过滤。

### 各方法快速回顾

| 方法 | 用途 | 示例 |
| --- | --- | --- |
| `SelectMany` | 将嵌套集合扁平化为单个序列 | `orders.SelectMany(o => o.Items)` |
| `Where` | 保留满足条件的元素 | `nums.Where(n => n > 0)` |
| `Select` | 转换每个元素 | `names.Select(n => n.Trim())` |
| `Distinct` | 移除重复元素 | `tags.Distinct()` |
| `OrderBy` | 按升序对元素排序 | `cities.OrderBy(c => c)` |

### 语法

```csharp
var result = source
    .SelectMany(item => item.GetSubItems())   // 扁平化
    .Where(sub => sub.IsValid)                 // 过滤
    .Select(sub => sub.Name)                   // 投影
    .Distinct()                                // 去重
    .OrderBy(name => name)                     // 排序
    .ToArray();                                // 具体化
```

### 示例

假设你有一个客户记录列表，每条记录包含多个电子邮件地址：

```csharp
string[][] emailGroups = {
    new[] { "alice@work.com", "alice@home.com" },
    new[] { "bob@work.com", "alice@work.com" }
};

var domains = emailGroups
    .SelectMany(group => group)                    // 扁平化为单个电子邮件
    .Where(email => email.Contains("@work"))       // 只保留工作邮箱
    .Select(email => email.Split('@')[1])          // 提取域名部分
    .Distinct()                                     // 移除重复的域名
    .OrderBy(d => d)                                // 按字母顺序排序
    .ToArray();
// 结果：["work.com"]
```

另一个示例：处理食谱中的配料列表：

```csharp
string[] recipes = { "flour sugar eggs", "sugar butter eggs flour" };

var ingredients = recipes
    .SelectMany(r => r.Split(' '))   // 扁平化为单个配料
    .Where(i => i.Length > 4)        // 保留超过 4 个字符的配料
    .Select(i => i.ToUpper())        // 转为大写
    .Distinct()                      // 不要重复项
    .OrderBy(i => i)                 // 排序
    .ToArray();
// 结果：["BUTTER", "FLOUR", "SUGAR"]
```

### 分割字符串

`string.Split` 方法将字符串分割为子字符串数组。
最常用的重载是按指定字符分割：

```csharp
string sentence = "hello world today";
string[] words = sentence.Split(' ');
// words: ["hello", "world", "today"]
```

### 你的任务

编写一个方法，接收一个句子数组并通过五步 LINQ 管道处理它们：

1. **扁平化（Flatten）** - 将每个句子拆分成单个单词（按空格分割）
2. **过滤（Filter）** - 仅保留长度为 3 个字符或以上的单词
3. **转换（Transform）** - 将每个单词转换为大写
4. **去重（Deduplicate）** - 移除所有重复的单词
5. **排序（Sort）** - 将剩余的单词按字母顺序升序排列

将最终结果作为 `string[]` 返回。

### 方法签名

```csharp
public static string[] TransformPipeline(string[] sentences)
```

### 预期结果

```css
TransformPipeline(["the quick brown fox", "jumps over lazy dogs"]) -> ["BROWN", "DOGS", "FOX", "JUMPS", "LAZY", "OVER", "QUICK", "THE"]
TransformPipeline(["I am a cat", "I am a dog"]) -> ["CAT", "DOG"]
TransformPipeline(["hello world", "hello earth"]) -> ["EARTH", "HELLO", "WORLD"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] TransformPipeline(string[] sentences)
    {
        return sentences
            .SelectMany(s => s.Split(' '))   // 扁平化：拆分成单个单词
            .Where(w => w.Length >= 3)       // 过滤：只保留长度至少为 3 的单词
            .Select(w => w.ToUpper())        // 转换：转为大写
            .Distinct()                      // 去重
            .OrderBy(w => w)                 // 排序：按字母顺序升序
            .ToArray();
    }
}
```
