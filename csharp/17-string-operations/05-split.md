### Split 方法

`Split()` 方法根据指定的分隔符将字符串分割为子字符串数组。
它在解析 CSV 数据、处理用户输入以及将文本拆分为易于管理的部分时至关重要。

### 基本用法

```csharp
string sentence = "Hello World";
string[] words = sentence.Split(' ');  // 按空格分割
// words[0] = "Hello", words[1] = "World"

string csv = "apple,banana,cherry";
string[] fruits = csv.Split(',');  // 按逗号分割
// fruits = ["apple", "banana", "cherry"]
```

### 分割选项

```csharp
// 按多个字符分割
string data = "one;two,three";
string[] parts = data.Split(';', ',');  // ["one", "two", "three"]

// 按字符串分隔符分割
string text = "red--blue--green";
string[] colors = text.Split("--");  // ["red", "blue", "green"]
```

### 访问数组元素

```csharp
string[] words = sentence.Split(' ');
Console.WriteLine(words[0]);      // 第一个单词
Console.WriteLine(words.Length);  // 单词数量

// 遍历所有单词
foreach (string word in words)
{
    Console.WriteLine(word);
}
```

### 你的任务

编写一个方法，接收一个句子并将每个单词打印在单独的一行上。
使用 `Split()` 方法将句子拆分为单词（按空格分割），然后打印每个单词。

### 方法签名

```csharp
public static void PrintWords(string sentence)
```

### 预期结果

```
PrintWords("Hello World") prints:
Hello
World

PrintWords("C# is fun") prints:
C#
is
fun
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintWords(string sentence)
    {
        // 将句子拆分为单词，并将每个单词打印在新的一行上
        string[] words = sentence.Split(' ');
        
        foreach (string word in words)
        {
            Console.WriteLine(word);
        }
    }
}
```
