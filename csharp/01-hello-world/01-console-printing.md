### Console.WriteLine

`Console.WriteLine()` 是在 C# 中向控制台显示文本的方式。
每次调用都会在新的一行输出。

### 基本用法

```csharp
Console.WriteLine("Hello, World!");
// 输出：Hello, World!

Console.WriteLine("First line");
Console.WriteLine("Second line");
// 输出：
// First line
// Second line
```

### 变量与字符串

**变量**是一个用来存储值的具名容器。
可以把它想象成一个贴有标签的盒子，你可以把东西放进去，之后可以通过它的名称取出来。

**字符串**是一种用于保存文本的数据类型，即任何由双引号包裹的字符序列，如字母、数字或符号。

```csharp
string name = "Alex";           // 创建一个名为 'name' 的变量，保存文本 "Alex"
string favoriteColor = "Blue";  // 创建一个名为 'favoriteColor' 的变量，保存 "Blue"
```

语法解析：

- `string` - 数据类型（告诉 C# 该变量将保存文本）
- `name` - 变量名（由你指定，尽量让它具有描述性！）
- `=` - 赋值运算符（将值存入变量中）
- `"Alex"` - 值（用双引号包裹的实际文本）

### 打印变量

你可以通过传入变量名（不带引号）来打印存储在变量中的值：

```csharp
string greeting = "Welcome!";
Console.WriteLine(greeting);
// 输出：Welcome!

string city = "London";
Console.WriteLine(city);
// 输出：London
```

**重要提示：** 打印变量时，变量名周围不要加引号：

```csharp
Console.WriteLine(name);    // 打印变量的值：Alex
Console.WriteLine("name");  // 打印字面文本：name
```

### WriteLine 与 Write

| 方法 | 说明 |
| --- | --- |
| `Console.WriteLine()` | 打印文本并换行 |
| `Console.Write()` | 打印文本但保留在同一行 |

```csharp
Console.Write("Hello ");
Console.Write("World");
// 输出：Hello World（在同一行）

Console.WriteLine("Hello");
Console.WriteLine("World");
// 输出：
// Hello
// World
```

### 理解代码结构

在 C# 中，代码组织在**类**（class）和**方法**（method）中：

- **类**（Class）：将相关代码组织在一起的容器。在本练习中，`Solution` 是类名。可以把它想象成保存代码的文件夹。
- **方法**（Method）：执行特定任务的代码块。`PrintNameAndColor` 是方法名。方法就像食谱，它们包含执行某项任务的指令。

```csharp
public class Solution           // 这是类
{
    public static void PrintNameAndColor()  // 这是方法
    {
        // 代码写在方法内部
    }
}
```

目前，你只需知道代码应该写在方法内部（花括号 `{ }` 之间）。
稍后你将学习更多关于类和方法的知识！

### 你的任务

已经为你提供了两个字符串变量：`name` 和 `favoriteColor`。
使用 `Console.WriteLine()` 来完成以下任务：

1. 在一行中打印名字
2. 在另一行中打印喜欢的颜色

### 方法签名

```csharp
public static void PrintNameAndColor()
```

### 预期输出

```
Alex
Blue
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintNameAndColor()
    {
        // 这些字符串已经为你提供
        string name = "Alex";
        string favoriteColor = "Blue";

        // 在一行中打印名字
        Console.WriteLine(name);
        // 在另一行中打印喜欢的颜色
        Console.WriteLine(favoriteColor);
    }
}
```
