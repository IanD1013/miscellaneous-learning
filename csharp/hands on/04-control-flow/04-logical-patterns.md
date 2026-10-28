### 使用 `is`、`and`、`or`、`not` 的逻辑模式

C# 模式匹配允许你使用模式组合器来组合多个条件。
在与**编译时常量**进行比较时，它们可以让你的代码更具可读性。

### 重要提示：仅适用于编译时常量

带有 `is` 的模式匹配仅适用于在编译时已知的值：

```csharp
// ✅ 可行 - 0 和 1 是编译时常量
if (number is 0 or 1) { }

// ❌ 无法编译 - 变量不是常量
int min = 0;
int max = 10;
if (number is > min and < max) { }  // 报错！

// ✅ 对于变量，使用传统运算符
if (number > min && number < max) { }  // 可行！
```

### `or` 模式组合器

```csharp
// 如果 number 等于这些常量值中的任意一个则匹配
if (number is 1 or 2 or 3)
{ 
    Console.WriteLine("One, two, or three");
}

// 可用于常量关系模式
if (number is < 0 or > 100)
{
    Console.WriteLine("Out of range");
}
```

### `and` 模式组合器

```csharp
// 如果 number 在某个范围内（常量边界）则匹配
if (number is > 0 and < 10)
{
    Console.WriteLine("Between 1 and 9");
}

// 组合多个常量条件
if (number is >= 1 and <= 100 and not 50)
{
    Console.WriteLine("1-100, but not 50");
}
```

### `not` 模式组合器

```csharp
// 如果不等于某个常量值则匹配
if (number is not 0)
{
    Console.WriteLine("Not zero");
}

// 对关系模式求反
if (number is not > 0)
{
    Console.WriteLine("Zero or negative");
}
```

### 何时使用模式匹配与布尔运算符

| 场景 | 使用模式匹配 | 使用布尔运算符 |
| --- | --- | --- |
| 与字面量比较 (1, 2, "hello") | ✅ `x is 1 or 2` | `x == 1 \|\| x == 2` |
| 与 const 常量值比较 | ✅ `x is MyConst` | `x == MyConst` |
| 与变量比较 | ❌ 无法编译 | ✅ `x > min && x < max` |
| 动态边界 | ❌ 无法编译 | ✅ 使用 `&&` 和 `\|\|` |

### 你的任务

编写一个方法，在适用的地方使用模式匹配，根据以下规则对整数进行分类：

- 如果数字是 0 或 1，返回 `"edge"`（结合使用 `is` 和 `or`）
- 如果数字在 2 到 9 之间（包含 2 和 9），返回 `"small positive"`（结合使用 `is` 和 `and`）
- 如果数字不大于 0，返回 `"non-positive"`（结合使用 `is` 和 `not`）
- 如果数字在 10 到 100 之间（包含 10 和 100），返回 `"medium"`
- 对于所有其他数字，返回 `"large"`

### 方法签名

```csharp
public static string ClassifyNumber(int number)
```

### 预期结果

```
ClassifyNumber(0) -> "edge"
ClassifyNumber(1) -> "edge"
ClassifyNumber(5) -> "small positive"
ClassifyNumber(-5) -> "non-positive"
ClassifyNumber(50) -> "medium"
ClassifyNumber(200) -> "large"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ClassifyNumber(int number)
    {
        // 0 或 1：使用 is 和 or
        if (number is 0 or 1)
        {
            return "edge";
        }
        // 2 到 9（包含两端）：使用 is 和 and
        else if (number is >= 2 and <= 9)
        {
            return "small positive";
        }
        // 不大于 0：使用 is 和 not
        else if (number is not > 0)
        {
            return "non-positive";
        }
        // 10 到 100（包含两端）
        else if (number is >= 10 and <= 100)
        {
            return "medium";
        }
        // 其他所有数字
        else
        {
            return "large";
        }
    }
}
```
