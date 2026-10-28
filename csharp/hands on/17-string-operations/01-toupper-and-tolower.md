### ToUpper 和 ToLower

这些字符串方法将字符串中的所有字符转换为大写或小写字母，这对于标准化文本输入或格式化输出非常有用。

### 基本用法

```csharp
string name = "Hello World";
string upper = name.ToUpper();  // "HELLO WORLD"
string lower = name.ToLower();  // "hello world"
```

### 原始字符串保持不变

C# 中的字符串是不可变的（immutable），这意味着这些方法会返回一个新字符串，而不会修改原始字符串。

```csharp
string original = "MixedCase";
string result = original.ToUpper();
// original 仍然是 "MixedCase"
// result 是 "MIXEDCASE"
```

### 常见用例

| 方法 | 用例 | 示例 |
| --- | --- | --- |
| ToUpper() | 用于比较的标准化 | "yes".ToUpper() == "YES" |
| ToLower() | 规范化用户输入 | "Email@Test.COM".ToLower() |
| ToUpper() | 显示标题 | 将 "title".ToUpper() 用于标题 |

### 你的任务

实现两个方法：

1. `ConvertToUpperCase` - 打印转换为大写的输入文本
2. `ConvertToLowerCase` - 打印转换为小写的输入文本

### 方法签名

```csharp
public static void ConvertToUpperCase(string text)
public static void ConvertToLowerCase(string text)
```

### 预期结果

```
ConvertToUpperCase("Hello") -> prints: HELLO
ConvertToLowerCase("Hello") -> prints: hello
ConvertToUpperCase("C# Programming") -> prints: C# PROGRAMMING
```

### 解答

```csharp
using System;

public class Solution
{
    public static void ConvertToUpperCase(string text)
    {
        // 将文本转换为大写并打印
        Console.WriteLine(text.ToUpper());
    }
    
    public static void ConvertToLowerCase(string text)
    {
        // 将文本转换为小写并打印
        Console.WriteLine(text.ToLower());
    }
}
```
