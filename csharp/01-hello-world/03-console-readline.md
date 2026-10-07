### Console.ReadLine

`Console.ReadLine()` 读取用户输入的一行文本并将其作为字符串返回。
它会等待用户按下 Enter 键，然后返回用户输入的全部内容。

### 基本用法

```csharp
string input = Console.ReadLine();
Console.WriteLine(input);
```

程序会在 `Console.ReadLine()` 处暂停，直到用户输入内容并按下 Enter 键。
用户输入的任何内容都会存储在变量中。

### 将输入存储在变量中

```csharp
// 读取并存储到变量中
string name = Console.ReadLine();

// 现在你可以使用这个变量
Console.WriteLine(name);
```

### 你的任务

编写一个方法：

1. 使用 `Console.ReadLine()` 读取用户的名字
2. 将其存储在一个 string 变量中
3. 使用 `Console.WriteLine()` 打印该名字

### 方法签名

```csharp
public static void GreetUser()
```

### 预期结果

```
Input: Alice
Output: Alice
```

### 解答

```csharp
using System;

public class Solution
{
    public static void GreetUser()
    {
        // 使用 Console.ReadLine() 读取用户的名字
        string name = Console.ReadLine();
        // 然后使用 Console.WriteLine() 打印该名字
        Console.WriteLine(name);
    }
}
```
