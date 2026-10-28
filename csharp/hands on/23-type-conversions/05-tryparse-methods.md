### TryParse 方法

TryParse 方法尝试将字符串转换为特定类型，并返回一个指示成功或失败的布尔值，而不会抛出异常。

### 为什么使用 TryParse？

```csharp
// 转换失败时 Parse 会抛出异常
int value = int.Parse("abc");  // FormatException！

// TryParse 返回 false 而不是抛出异常
bool success = int.TryParse("abc", out int value);  // success = false, value = 0
```

### out 参数

TryParse 使用 `out` 参数来返回转换后的值：

```csharp
// 使用 out 内联声明变量
if (int.TryParse("42", out int number))
{
    Console.WriteLine(number);
  // 42
}

// 或者预先声明
int result;
bool parsed = int.TryParse("100", out result);
```

### 常用的 TryParse 方法

| 类型 | 方法 | 示例 |
| --- | --- | --- |
| int | int.TryParse() | int.TryParse("5", out int i) |
| double | double.TryParse() | double.TryParse("3.14", out double d) |
| bool | bool.TryParse() | bool.TryParse("true", out bool b) |
| DateTime | DateTime.TryParse() | DateTime.TryParse("2024-01-01", out DateTime dt) |

### Parse 与 TryParse

```csharp
// 当你确定字符串有效时使用 Parse
int age = int.Parse(validatedInput);

// 当字符串可能无效时使用 TryParse
if (int.TryParse(userInput, out int age))
{
    // 使用解析后的值
}
else
{
    // 优雅地处理无效输入
}
```

### 你的任务

创建一个安全地将字符串解析为整数的方法。
如果解析成功，返回解析后的值。
如果解析失败（无效格式、null 或空字符串），则返回提供的默认值。

### 方法签名

```csharp
public static int SafeParseToInt(string input, int defaultValue)
```

### 预期结果

```
SafeParseToInt("42", 0) -> 42
SafeParseToInt("abc", -1) -> -1
SafeParseToInt("", 100) -> 100
```

### 解答

```csharp
using System;

public class Solution
{
    public static int SafeParseToInt(string input, int defaultValue)
    {
        // 解析成功则返回解析后的值，否则返回默认值
        if (int.TryParse(input, out int number))
        {
            return number;
        }
        return defaultValue;
    }
}
```
