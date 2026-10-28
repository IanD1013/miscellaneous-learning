### 可空值类型

在 C# 中，诸如 `int`、`bool` 和 `double` 等值类型通常不能为 `null`。
可空值类型语法（`int?`）允许这些类型同时持有一个 `null` 值，这在值可能缺失或未定义时非常有用。

### 声明可空值类型

```csharp
// 普通 int - 不能为 null
int regularNumber = 42;

// 可空 int - 可以为 null，也可以持有一个值
int? nullableNumber = 42;
int? anotherNullable = null;
```

### 检查是否存在值

可空类型具有两个重要的属性：

```csharp
int? age = 25;

// 如果变量包含值，HasValue 返回 true
bool hasAge = age.HasValue;  // true

// Value 返回实际的值（如果为 null 则抛出异常！）
int actualAge = age.Value;   // 25

int? unknown = null;
bool hasUnknown = unknown.HasValue;  // false
```

### 与 null 进行比较

```csharp
int? score = 100;

// 你也可以直接与 null 进行比较
if (score != null)
{
    Console.WriteLine("Score exists: " + score);
}

// 这等同于使用 HasValue
if (score.HasValue)
{
    Console.WriteLine("Score exists: " + score.Value);
}
```

### 常用属性

| 属性 | 描述 | 示例 |
| --- | --- | --- |
| HasValue | 如果不为 null 则返回 true | `myInt?.HasValue` → `true` 或 `false` |
| Value | 获取该值（如果为 null 则抛出异常） | `myInt?.Value` → 实际的 int 值 |

### 你的任务

编写一个方法，接收一个可空整数并检查它是否具有值。
返回一个字符串，指明该值是否存在以及具体是什么。

### 方法签名

```csharp
public static string CheckNullableValue(int? number)
```

### 预期结果

```
CheckNullableValue(42) -> "Has value: 42"
CheckNullableValue(null) -> "No value"
CheckNullableValue(0) -> "Has value: 0"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CheckNullableValue(int? number)
    {
        // 检查可空 int 是否具有值
        // 如果有值，返回 "Has value: X"，其中 X 为该值
        // 如果没有值，返回 "No value"
        if (number.HasValue)
        {
            return "Has value: " + number.Value;
        }

        return "No value";
    }
}
```
