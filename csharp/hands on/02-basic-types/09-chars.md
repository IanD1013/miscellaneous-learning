### C# 中的 Char

`char` 表示单个 Unicode 字符。
字符串可以包含多个字符，而 `char` 恰好只包含一个字符。
在处理来自字符串或键盘输入的单个字符时，可以使用 `char`。

### 声明 Char

```csharp
char letter = 'A';       // char 字面量使用单引号
char digit = '7';
char symbol = '@';
char newline = '\n';     // 转义序列同样适用
```

### Char 与 String 的对比

| 类型 | 语法 | 示例 | 长度 |
| --- | --- | --- | --- |
| `char` | 单引号 | `'A'` | 始终为 1 |
| `string` | 双引号 | `"A"` | 0 或更多 |

```csharp
char c = 'H';           // 单个字符
string s = "H";         // 只有一个字符的字符串
string empty = "";      // 有效 - 空字符串
// char empty = '';     // 错误 - char 必须恰好包含一个字符
```

### 常用的 Char 方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| `char.IsLetter(c)` | 是否为字母？ | `char.IsLetter('A')` → `True` |
| `char.IsDigit(c)` | 是否为数字 0-9？ | `char.IsDigit('5')` → `True` |
| `char.IsUpper(c)` | 是否为大写？ | `char.IsUpper('a')` → `False` |
| `char.IsLower(c)` | 是否为小写？ | `char.IsLower('a')` → `True` |
| `char.ToUpper(c)` | 转换为大写 | `char.ToUpper('a')` → `'A'` |
| `char.ToLower(c)` | 转换为小写 | `char.ToLower('A')` → `'a'` |

### 你的任务

编写一个方法，接收一个字符并打印关于该字符的四行信息：

1. 字符本身
2. 它是否为字母（`True` 或 `False`）
3. 它是否为数字（`True` 或 `False`）
4. 它是否为大写（`True` 或 `False`）

### 方法签名

```csharp
public static void PrintCharInfo(char c)
```

### 预期输出

```
PrintCharInfo('A') prints:
A
True
False
True

PrintCharInfo('7') prints:
7
False
True
False
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintCharInfo(char c)
    {
        // 打印字符本身
        Console.WriteLine(c);
        // 打印它是否为字母
        Console.WriteLine(char.IsLetter(c));
        // 打印它是否为数字
        Console.WriteLine(char.IsDigit(c));
        // 打印它是否为大写
        Console.WriteLine(char.IsUpper(c));
    }
}
```
