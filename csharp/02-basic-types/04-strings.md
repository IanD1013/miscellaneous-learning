### C# 中的字符串

字符串是用于表示文本的字符序列。
字符串是编程中最常用的数据类型之一。

### 声明字符串

```csharp
// 使用 string 关键字（推荐）
string name = "Alice";
string city = "New York";

// 字符串可以包含字母、数字、空格和特殊字符
string message = "Order #12345 confirmed!";
```

### 字符串与其他类型

与数值类型（`int`、`double`、`decimal`）不同，字符串保存用双引号括起来的文本数据。

```csharp
int age = 25;           // 数字 - 不加引号
double price = 19.99;   // 数字 - 不加引号
string name = "Bob";    // 文本 - 需要双引号
```

### 打印字符串

使用 `Console.WriteLine()` 将字符串打印到控制台。

```csharp
string greeting = "Hello!";
Console.WriteLine(greeting);  // 打印：Hello!

// 你也可以直接打印字符串字面量
Console.WriteLine("Goodbye!");  // 打印：Goodbye!
```

### 你的任务

创建一个名为 `greeting` 的字符串变量，其值为 `"Hello, World!"`，并将其打印到控制台。

### 方法签名

```csharp
public static void PrintGreeting()
```

### 预期输出

```
Hello, World!
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintGreeting()
    {
        // 第 1 步：定义一个名为 greeting 的字符串变量，值为 "Hello, World!"
        string greeting = "Hello, World!";

        // 第 2 步：将 greeting 打印到控制台
        Console.WriteLine(greeting);
    }
}
```
