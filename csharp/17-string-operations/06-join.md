### String.Join 方法

`string.Join()` 方法将字符串数组组合成单个字符串，并在每个元素之间插入指定的分隔符。
它是 `Split()` 的逆操作，通常用于构建 CSV 行、创建格式化输出或重构句子。

### 基本用法

```csharp
string[] fruits = { "apple", "banana", "cherry" };

// 用逗号连接
string csv = string.Join(",", fruits);        // "apple,banana,cherry"

// 用空格连接
string sentence = string.Join(" ", fruits);   // "apple banana cherry"

// 用自定义分隔符连接
string piped = string.Join(" | ", fruits);   // "apple | banana | cherry"
```

### Join 与 Split

```csharp
// Split 将字符串拆分为数组
string text = "one,two,three";
string[] parts = text.Split(',');  // ["one", "two", "three"]

// Join 将数组组合成字符串
string result = string.Join("-", parts);  // "one-two-three"
```

### 边界情况

```csharp
string[] empty = { };
string result1 = string.Join(",", empty);     // "" (空字符串)

string[] single = { "hello" };
string result2 = string.Join(",", single);    // "hello" (不添加分隔符)

string[] withEmpty = { "a", "", "c" };
string result3 = string.Join("-", withEmpty); // "a--c" (保留空元素)
```

### 你的任务

实现一个使用指定分隔符连接单词数组的方法。
这对于创建句子、CSV 数据或任何格式化字符串输出都非常有用。

### 方法签名

```csharp
public static string JoinWords(string[] words, string separator)
```

### 预期结果

```
JoinWords(["Hello", "World"], " ") -> "Hello World"
JoinWords(["a", "b", "c"], ",") -> "a,b,c"
JoinWords(["one"], "-") -> "one"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string JoinWords(string[] words, string separator)
    {
        // 使用指定分隔符连接所有单词
        return string.Join(separator, words);
    }
}
```
