### Parse 方法

Parse 方法将值的字符串表示形式转换为其对应的数据类型。
当你有需要转换为数字的用户输入或文本数据时，可以使用它们。

### 基本用法

```csharp
// int.Parse 将字符串转换为整数
int number = int.Parse("42");      // number = 42
int negative = int.Parse("-15");   // negative = -15

// double.Parse 将字符串转换为 double
double price = double.Parse("19.99");  // price = 19.99
double pi = double.Parse("3.14159");   // pi = 3.14159
```

### Parse 与 Convert

```csharp
// 对于有效字符串，两者的结果类似
int fromParse = int.Parse("100");        // 100
int fromConvert = Convert.ToInt32("100"); // 100

// 关键区别：Convert 能优雅地处理 null
int fromConvertNull = Convert.ToInt32(null); // 返回 0
int fromParseNull = int.Parse(null);         // 抛出异常！
```

### 重要提示：Parse 会抛出异常

如果字符串不是有效的数字，Parse 方法会抛出 `FormatException`：

```csharp
int.Parse("hello");   // FormatException！
int.Parse("12.5");    // FormatException！（int.Parse 中包含小数）
int.Parse("");        // FormatException！（空字符串）
```

### 常用的 Parse 方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| int.Parse(s) | 字符串转整数 | int.Parse("42") = 42 |
| double.Parse(s) | 字符串转 double | double.Parse("3.14") = 3.14 |
| bool.Parse(s) | 字符串转布尔值 | bool.Parse("True") = true |
| long.Parse(s) | 字符串转 long | long.Parse("999999999") |

### 你的任务

实现一个方法，使用 `int.Parse()` 接收包含数字的字符串并将其作为整数返回。

### 方法签名

```csharp
public static int ParseStringToInt(string numberString)
```

### 预期结果

```
ParseStringToInt("42") -> 42
ParseStringToInt("-15") -> -15
ParseStringToInt("0") -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    public static int ParseStringToInt(string numberString)
    {
        // 使用 int.Parse 将字符串转换为整数
        return int.Parse(numberString);
    }
}
```
