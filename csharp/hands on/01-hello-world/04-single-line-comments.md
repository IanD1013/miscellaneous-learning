### 单行注释

注释是代码中的说明性文字，计算机在运行时会忽略它们。
注释能帮助你和其他程序员理解代码的功能。

### 编写注释

在 C# 中，单行注释以 `//` 开头。
该行中 `//` 之后的所有内容都会被忽略。

```csharp
// 这是一条注释 - 计算机会忽略它
Console.WriteLine("Hello"); // 你也可以在行尾添加注释
```

### 为什么要使用注释？

- **解释代码**：描述复杂逻辑的作用
- **留下备忘**：提醒自己为什么要这样写
- **停用代码**：无需删除代码即可暂时停止其运行

```csharp
// 计算圆的面积
double area = 3.14 * radius * radius;

// Console.WriteLine("Debug message"); // 这一行不会运行
```

### 注释掉代码

你可以“注释掉”代码来暂时停用它：

```csharp
Console.WriteLine("This prints");
// Console.WriteLine("This does NOT print");
```

### 你的任务

修改代码以实现：

1. 保留描述性注释（它们只是说明笔记）
2. **注释掉**最后一个 `Console.WriteLine`，使其不再执行

输出应仅显示 "Hello, World!" 和数字 8。

### 预期输出

```
Hello, World!
8
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintWithComments()
    {
        // 向控制台打印问候语
        Console.WriteLine("Hello, World!");

        // 计算 5 加 3 的和并打印结果
        int result = 5 + 3;
        Console.WriteLine(result);

        // 已注释掉，这一行不会运行
        // Console.WriteLine("This should NOT print");
    }
}
```
