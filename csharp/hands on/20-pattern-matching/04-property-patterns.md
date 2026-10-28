### 属性模式 (Property Patterns)

属性模式允许你使用 `{ PropertyName: pattern }` 语法根据对象的属性值进行匹配。
这对于无需显式访问属性即可编写富有表现力的条件非常强大。

### 基本语法

```csharp
// 匹配精确的属性值
if (person is { Name: "Alice" })
    Console.WriteLine("Found Alice!");

// 结合关系模式进行匹配
if (person is { Age: >= 18 })
    Console.WriteLine("Adult");

// 组合多个属性
if (person is { Age: >= 21, IsEmployed: true })
    Console.WriteLine("Employed adult 21+");
```

### Switch 中的属性模式

```csharp
string result = order switch
{
    { Total: 0 } => "Empty order",
    { Total: < 50 } => "Small order",
    { Total: >= 50, IsPriority: true } => "Priority large order",
    { Total: >= 50 } => "Large order",
    _ => "Unknown"
};
```

### 属性中的关系模式

| 模式 | 含义 |
| --- | --- |
| `{ Age: 18 }` | 恰好 18 |
| `{ Age: < 18 }` | 小于 18 |
| `{ Age: >= 65 }` | 65 岁或以上 |
| `{ IsActive: true }` | 布尔值检查 |

### 你的任务

根据 `Person` 的属性对其进行分类：

- 如果 `Age` 小于 18，返回 `"Minor"`
- 如果 `Age` 大于或等于 65，返回 `"Senior"`
- 如果 `IsEmployed` 为 `true`（且年龄在 18-64 岁），返回 `"Working Adult"`
- 如果 `IsEmployed` 为 `false`（且年龄在 18-64 岁），返回 `"Unemployed Adult"`

请在 switch 表达式中使用属性模式。
`Person` 类已在 `Person.cs` 中提供。

### 方法签名

```csharp
public static string ClassifyPerson(Person person)
```

### 预期结果

```
ClassifyPerson(new Person("Tim", 10, false)) -> "Minor"
ClassifyPerson(new Person("Alice", 30, true)) -> "Working Adult"
ClassifyPerson(new Person("Bob", 70, false)) -> "Senior"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ClassifyPerson(Person person)
    {
        // 在 switch 表达式中使用属性模式，从上到下依次匹配
        return person switch
        {
            { Age: < 18 } => "Minor",
            { Age: >= 65 } => "Senior",
            { IsEmployed: true } => "Working Adult",
            _ => "Unemployed Adult"
        };
    }
}
```
