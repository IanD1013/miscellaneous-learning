### Trim 方法

`Trim()` 系列方法用于移除字符串中的空白字符。
这对于清理用户输入和处理文本数据至关重要。

### Trim()

移除字符串开头和结尾的空白字符。

```csharp
string messy = "   Hello World   ";
string clean = messy.Trim();  // "Hello World"

string tabs = "\t\tData\t\t";
string cleanTabs = tabs.Trim();  // "Data"
```

### TrimStart() 和 TrimEnd()

仅从字符串的单侧移除空白字符。

```csharp
string text = "   Hello   ";

string trimmedStart = text.TrimStart();  // "Hello   "
string trimmedEnd = text.TrimEnd();      // "   Hello"
string trimmedBoth = text.Trim();        // "Hello"
```

### 哪些属于空白字符？

| 字符 | 描述 |
| --- | --- |
| 空格 | 普通空格字符 |
| \t | 制表符（Tab） |
| \n | 换行符 |
| \r | 回车符 |

### Trim 与手动移除的对比

```csharp
// Trim 仅从两端移除，不会移除内部的空格
string text = "  Hello   World  ";
string trimmed = text.Trim();  // "Hello   World" (内部空格被保留)
```

### 你的任务

编写一个方法，通过移除所有前导和尾随空白字符来清理字符串。
字符串内部的内容应保持不变。

### 方法签名

```csharp
public static string CleanupText(string text)
```

### 预期结果

```
CleanupText("   Hello   ") -> "Hello"
CleanupText("\t\tWorld\n\n") -> "World"
CleanupText("  No Extra Spaces  ") -> "No Extra Spaces"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string CleanupText(string text)
    {
        // 移除前导和尾随空白字符
        return text.Trim();
    }
}
```
