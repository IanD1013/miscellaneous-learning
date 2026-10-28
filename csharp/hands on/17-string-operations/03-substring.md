### Substring

`Substring()` 方法用于从指定位置开始截取字符串的一部分。
它对于解析文本、提取代码以及操作字符串数据至关重要。

### 基本用法

```csharp
string greeting = "Hello, World!";

// 从索引 0 开始截取长度为 5 的子字符串
string first = greeting.Substring(0, 5);  // "Hello"

// 从索引 7 截取到末尾
string rest = greeting.Substring(7);       // "World!"
```

### 两种重载

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `Substring(startIndex)` | 从 startIndex 到末尾 | `"Hello".Substring(2)` → `"llo"` |
| `Substring(startIndex, length)` | 截取指定长度 | `"Hello".Substring(0, 3)` → `"Hel"` |

### 重要注意事项

```csharp
string word = "Hi";

// 这会抛出 ArgumentOutOfRangeException！
// string result = word.Substring(0, 5);  // 只有 2 个字符可用

// 截取前务必检查长度
if (word.Length >= 5)
{
    string safe = word.Substring(0, 5);
}
```

### 你的任务

编写一个方法，从字符串中截取前 5 个字符。
如果字符串少于 5 个字符，则返回整个字符串。

### 方法签名

```csharp
public static string GetFirstFiveCharacters(string text)
```

### 预期结果

```
GetFirstFiveCharacters("HelloWorld") -> "Hello"
GetFirstFiveCharacters("Programming") -> "Progr"
GetFirstFiveCharacters("Hi") -> "Hi"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetFirstFiveCharacters(string text)
    {
        // 少于 5 个字符时返回整个字符串
        if (text.Length < 5)
        {
            return text;
        }
        
        // 截取前 5 个字符
        return text.Substring(0, 5);
    }
}
```
