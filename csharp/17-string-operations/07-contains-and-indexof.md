### Contains 和 IndexOf

这两个字符串方法常结合使用，用于在字符串中进行搜索。
`Contains()` 检查子字符串是否存在，而 `IndexOf()` 则告诉你它具体在什么位置。

### Contains 方法

```csharp
string message = "Hello World";
bool hasHello = message.Contains("Hello");  // True
bool hasGoodbye = message.Contains("Goodbye");  // False
bool hasWorld = message.Contains("World");  // True
```

`Contains()` 返回一个布尔值，非常适合用于条件判断。

### IndexOf 方法

```csharp
string message = "Hello World";
int helloPos = message.IndexOf("Hello");  // 0 (从索引 0 开始)
int worldPos = message.IndexOf("World");  // 6 (从索引 6 开始)
int notFound = message.IndexOf("Goodbye");  // -1 (未找到)
```

`IndexOf()` 返回子字符串起始处的从零开始的索引，如果未找到则返回 `-1`。

### 区分大小写

默认情况下，这两个方法都是区分大小写的：

```csharp
string text = "Hello World";
text.Contains("hello");  // False (小写的 'h')
text.IndexOf("WORLD");   // -1 (大写)
```

### 常用变体

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| Contains(string) | 检查子字符串是否存在 | "abc".Contains("b") → True |
| IndexOf(string) | 首次出现的位置 | "abcabc".IndexOf("b") → 1 |
| LastIndexOf(string) | 最后一次出现的位置 | "abcabc".LastIndexOf("b") → 4 |

### 你的任务

编写一个方法，在一段文本字符串中搜索指定的单词。
首先检查文本中是否包含该单词，如果包含，则返回该单词起始的位置。
如果未找到该单词，则返回 `-1`。

### 方法签名

```csharp
public static int FindWordPosition(string text, string word)
```

### 预期结果

```
FindWordPosition("Hello World", "World") -> 6
FindWordPosition("The quick brown fox", "quick") -> 4
FindWordPosition("Hello World", "Goodbye") -> -1
```

### 解答

```csharp
using System;

public class Solution
{
    public static int FindWordPosition(string text, string word)
    {
        // 如果找到该单词，返回它的位置；否则返回 -1
        if (text.Contains(word))
        {
            return text.IndexOf(word);
        }
        
        return -1;
    }
}
```
