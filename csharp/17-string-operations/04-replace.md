### Replace 方法

`Replace()` 方法将指定字符串的所有匹配项替换为另一个字符串。
它常用于文本转换、清理输入以及格式化输出。

### 基本用法

```csharp
string text = "Hello World";
string result = text.Replace("World", "C#");
// result = "Hello C#"

// 替换所有匹配项
string repeated = "cat cat cat";
string changed = repeated.Replace("cat", "dog");
// changed = "dog dog dog"
```

### 关键特性

```csharp
// Replace 区分大小写
string text = "Hello HELLO hello";
string result = text.Replace("Hello", "Hi");
// result = "Hi HELLO hello" (仅替换完全匹配项)

// 如果未找到 oldValue，则返回原始字符串
string unchanged = "apple".Replace("orange", "banana");
// unchanged = "apple"

// 可以替换为空字符串来实现移除
string cleaned = "a-b-c".Replace("-", "");
// cleaned = "abc"
```

### Replace 与其他字符串方法对比

| 方法 | 用途 | 返回值 |
| --- | --- | --- |
| Replace() | 替换文本 | 包含替换内容的新字符串 |
| Substring() | 提取部分文本 | 字符串的一部分 |
| Trim() | 移除空白字符 | 移除了前导/尾随空格的字符串 |

### 你的任务

编写一个方法，接收一个句子，并将其中出现的所有特定单词替换为一个新单词。
替换操作应区分大小写（仅完全匹配）。

### 方法签名

```csharp
public static string ReplaceWord(string sentence, string oldWord, string newWord)
```

### 预期结果

```
ReplaceWord("The cat sat on the cat mat", "cat", "dog") -> "The dog sat on the dog mat"
ReplaceWord("Hello World", "World", "C#") -> "Hello C#"
ReplaceWord("aaa", "a", "b") -> "bbb"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string ReplaceWord(string sentence, string oldWord, string newWord)
    {
        // 区分大小写地替换所有匹配项
        return sentence.Replace(oldWord, newWord);
    }
}
```
