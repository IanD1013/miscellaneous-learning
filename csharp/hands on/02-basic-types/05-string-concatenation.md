### 字符串拼接

字符串拼接（String concatenation）是使用 `+` 运算符将两个或多个字符串连接在一起的过程。
这是在 C# 中构建字符串最基础的方法之一。

### 基本字符串拼接

```csharp
string greeting = "Hello" + " " + "World";
// 结果："Hello World"

string first = "John";
string last = "Doe";
string fullName = first + " " + last;
// 结果："John Doe"
```

### 字符串与数字拼接

当将字符串与数字进行拼接时，C# 会自动将数字转换为字符串：

```csharp
int score = 100;
string message = "Your score is: " + score;
// 结果："Your score is: 100"

double price = 19.99;
string priceTag = "Price: $" + price;
// 结果："Price: $19.99"
```

### 构建多部分字符串

```csharp
string name = "Alice";
int age = 25;
string city = "London";

string bio = name + " is " + age + " years old and lives in " + city + ".";
// 结果："Alice is 25 years old and lives in London."
```

### 你的任务

编写一个方法，接收名字（first name）、姓氏（last name）和年龄（age），然后打印三行内容：

1. 全名（名字 + 空格 + 姓氏）
2. 问候语：`Hello, [fullName]!`
3. 年龄信息：`[fullName] is [age] years old.`

### 方法签名

```csharp
public static void PrintConcatenation(string firstName, string lastName, int age)
```

### 预期输出

调用 `PrintConcatenation("John", "Doe", 30)` 时输出：

```
John Doe
Hello, John Doe!
John Doe is 30 years old.
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintConcatenation(string firstName, string lastName, int age)
    {
        // 1. 全名（firstName + 空格 + lastName）
        string fullName = firstName + " " + lastName;
        Console.WriteLine(fullName);
        // 2. 带名字的问候语
        Console.WriteLine("Hello, " + fullName + "!");
        // 3. 带年龄的信息，数字与字符串拼接时会自动转换为字符串
        Console.WriteLine(fullName + " is " + age + " years old.");
    }
}
```
