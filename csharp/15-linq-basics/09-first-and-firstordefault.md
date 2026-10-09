### First 和 FirstOrDefault

`First()` 和 `FirstOrDefault()` 用于从集合中检索第一个元素，可选择通过条件进行筛选。
关键区别在于它们如何处理空结果。

### First() - 为空时抛出异常

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 获取第一个元素
int first = numbers.First();  // 返回 1

// 获取第一个匹配的元素
int firstEven = numbers.First(n => n % 2 == 0);  // 返回 2

// 危险：如果没有匹配项，会抛出 InvalidOperationException！
int firstBig = numbers.First(n => n > 100);  // 抛出异常！
```

### FirstOrDefault() - 安全的替代方案

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 如果没有匹配项，返回默认值（int 为 0，引用类型为 null）
int firstBig = numbers.FirstOrDefault(n => n > 100);  // 返回 0

var names = new List<string> { "Alice", "Bob" };
string firstZ = names.FirstOrDefault(n => n.StartsWith("Z"));  // 返回 null
```

### 何时使用哪一个

| 方法 | 适用场景 | 空结果 |
| --- | --- | --- |
| `First()` | 确定存在匹配项时 | 抛出异常 |
| `FirstOrDefault()` | 匹配项可能不存在时 | 返回默认值 |

### 使用 ?? 处理 Null

```csharp
// 使用空合并运算符提供自定义默认值
string result = names.FirstOrDefault(n => n.Length > 10) ?? "Not found";
```

### 你的任务

在列表中查找长度大于或等于指定最小长度的第一个名称（name）。
如果没有名称符合条件，则返回字符串 `"No match found"`。

### 方法签名

```csharp
public static string GetFirstLongName(List<string> names, int minLength)
```

### 预期结果

```
GetFirstLongName(["Al", "Bob", "Catherine"], 5) -> "Catherine"
GetFirstLongName(["Al", "Bob", "Cat"], 10) -> "No match found"
GetFirstLongName(["Alexander", "Bob"], 5) -> "Alexander"
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static string GetFirstLongName(List<string> names, int minLength)
    {
        // 返回第一个长度 >= minLength 的名称
        // 如果没有名称符合条件，则返回 "No match found"
        return names.FirstOrDefault(n => n.Length >= minLength) ?? "No match found";
    }
}
```
