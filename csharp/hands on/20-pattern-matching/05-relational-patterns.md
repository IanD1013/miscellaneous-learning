### 关系模式

关系模式允许你在模式匹配表达式中直接使用 `<`、`>`、`<=` 和 `>=` 运算符将值与常量进行比较。
这可以创建清晰、易读的基于范围的逻辑。

### 基本语法

```csharp
// 在 switch 表达式中使用关系模式
string result = number switch
{
    < 0 => "Negative",
    0 => "Zero",
    > 0 => "Positive"
};

// 与特定值进行比较
string grade = score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 60 => "D",
    < 60 => "F"
};
```

### 模式求值顺序

模式是从上到下进行求值的，因此请将更具体的模式放在前面：

```csharp
// 顺序很重要！限制更严格的模式放在前面
string temp = celsius switch
{
    < -40 => "Extreme Cold",
    < 0 => "Freezing",
    < 20 => "Cool",
    < 30 => "Warm",
    >= 30 => "Hot"
};
```

### 模式中的关系运算符

| 运算符 | 含义 | 示例 |
| --- | --- | --- |
| `<` | 小于 | `< 10` 匹配 9, 0, -5 |
| `>` | 大于 | `> 10` 匹配 11, 100 |
| `<=` | 小于或等于 | `<= 10` 匹配 10, 5, -3 |
| `>=` | 大于或等于 | `>= 10` 匹配 10, 15, 100 |

### 你的任务

创建一个方法，在 switch 表达式中使用关系模式将一个人的年龄划分为不同的人生阶段。

**年龄分类：**

- 负数年龄 → `"Invalid"`
- 0-1（2 岁以下）→ `"Infant"`
- 2-12（13 岁以下）→ `"Child"`
- 13-19（20 岁以下）→ `"Teenager"`
- 20-64（65 岁以下）→ `"Adult"`
- 65 岁及以上 → `"Senior"`

### 方法签名

```csharp
public static string CategorizeAge(int age)
```

### 预期结果

```
CategorizeAge(-5) -> "Invalid"
CategorizeAge(1) -> "Infant"
CategorizeAge(10) -> "Child"
CategorizeAge(16) -> "Teenager"
CategorizeAge(35) -> "Adult"
CategorizeAge(70) -> "Senior"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CategorizeAge(int age)
    {
        // 在 switch 中使用关系模式对年龄进行分类
        // 分类："Invalid"、"Infant"、"Child"、"Teenager"、"Adult"、"Senior"
        return age switch
        {
            < 0 => "Invalid",
            < 2 => "Infant",
            < 13 => "Child",
            < 20 => "Teenager",
            < 65 => "Adult",
            >= 65 => "Senior"
        };
    }
}
```
