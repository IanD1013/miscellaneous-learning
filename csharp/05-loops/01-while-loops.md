### While 循环

while 循环只要条件保持为 true，就会重复执行一段代码块。
当你不知道确切需要迭代多少次时，可以使用它。

### 基本语法

```csharp
while (condition)
{
    // 要执行的代码
}
```

循环会在每次迭代**之前**检查条件。
如果初始条件为 false，则循环体永远不会执行。

### 循环的组成部分

```csharp
int counter = 1;        // 1. 初始化计数器变量
while (counter <= 3)    // 2. 每次迭代前检查条件
{
    Console.WriteLine(counter);  // 3. 循环体
    counter++;                   // 4. 更新计数器（至关重要！）
}
// 输出：1, 2, 3（每个占一行）
```

### 常见模式

```csharp
// 递增计数
int i = 0;
while (i < 5)
{
    Console.WriteLine(i);
    i++;
}

// 递减计数
int j = 5;
while (j > 0)
{
    Console.WriteLine(j);
    j--;
}
```

### 无限循环警告

```csharp
// 危险：这会永远运行下去！
int x = 1;
while (x <= 5)
{
    Console.WriteLine(x);
    // 缺少 x++ 意味着 x 始终为 1！
}
```

请务必确保你的循环条件最终会变为 false。

### 你的任务

编写一个使用 while 循环打印数字 1 到 5 的方法，每个数字占一行。

### 方法签名

```csharp
public static void PrintNumbers()
```

### 预期输出

```
1
2
3
4
5
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintNumbers()
    {
        // 使用 while 循环打印数字 1 到 5
        int counter = 1;
        while (counter <= 5)
        {
            Console.WriteLine(counter);
            counter++;
        }
    }
}
```
