### 带类型模式的 Switch

switch 语句中的类型模式匹配允许你根据对象的运行时类型进行分支处理，同时提取出一个带类型的变量以供该分支使用。

### 基本语法

```csharp
switch (obj)
{
    case int number:
        Console.WriteLine($"It's an integer: {number}");
        break;
    case string text:
        Console.WriteLine($"It's a string: {text}");
        break;
    default:
        Console.WriteLine("Unknown type");
        break;
}
```

### 与 If-Else 链的对比

```csharp
// 之前：使用 is 和类型转换的冗长 if-else
if (obj is int)
{
    int n = (int)obj;
    // 使用 n
}
else if (obj is string)
{
    string s = (string)obj;
    // 使用 s
}

// 之后：使用类型模式的简洁 switch
switch (obj)
{
    case int n:    // 类型检查 + 变量合二为一
        // 直接使用 n
        break;
    case string s:
        // 直接使用 s
        break;
}
```

### 处理 Null

```csharp
switch (value)
{
    case null:           // 显式的 null 分支
        return "Nothing";
    case string s:
        return s;
    default:
        return "Other";
}
```

### 实用的字符串方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| ToUpper() | 转换为大写 | "hello".ToUpper() → "HELLO" |
| :F2 格式 | 将 double 格式化为保留 2 位小数 | $"{3.14159:F2}" → "3.14" |

### 你的任务

编写一个方法，使用带有类型模式的 switch 语句来处理不同的对象类型：

- `int` → 返回 `"Integer: {value}"`
- `double` → 返回 `"Double: {value}"`（格式化为保留 2 位小数）
- `string` → 返回 `"String: {value}"`（转换为大写）
- `bool` → 返回 `"Boolean: {value}"`
- `null` → 返回 `"Null value"`
- 任何其他类型 → 返回 `"Unknown type"`

### 方法签名

```csharp
public static string HandleObject(object value)
```

### 预期结果

```
HandleObject(42) -> "Integer: 42"
HandleObject(3.14159) -> "Double: 3.14"
HandleObject("hello") -> "String: HELLO"
HandleObject(true) -> "Boolean: True"
HandleObject(null) -> "Null value"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string HandleObject(object value)
    {
        // 使用带类型模式的 switch 语句按类型分支
        switch (value)
        {
            case int i:
                return $"Integer: {i}";
            case double d:
                return $"Double: {d:F2}";
            case string s:
                return $"String: {s.ToUpper()}";
            case bool b:
                return $"Boolean: {b}";
            case null:
                return "Null value";
            default:
                return "Unknown type";
        }
    }
}
```
