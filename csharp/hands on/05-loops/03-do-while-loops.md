### Do-While 循环

do-while 循环在检查条件之前会**至少执行一次**其主体。
这非常适合需要先执行某项操作，然后再决定是否继续的场景。

### 语法

```csharp
do
{
    // 代码至少执行一次
} while (condition);
```

### While 与 Do-While

```csharp
// While 循环 - 可能永远不会执行
int x = 10;
while (x < 5)
{
    Console.WriteLine("This never prints");
}

// Do-while 循环 - 总是至少执行一次
int y = 10;
do
{
    Console.WriteLine("This prints once!");
} while (y < 5);
```

### 计数器控制的 Do-While

当你需要至少执行一次迭代时，do-while 循环非常适合与计数器配合使用：

```csharp
int count = 1;
do
{
    Console.WriteLine($"Count: {count}");
    count++;
} while (count <= 3);
// 打印：Count: 1, Count: 2, Count: 3
```

### 常见使用场景

| 使用场景 | 为什么使用 Do-While？ |
| --- | --- |
| 菜单系统 | 必须至少显示一次菜单 |
| 重试逻辑 | 必须至少尝试操作一次 |
| 游戏循环 | 必须至少运行一帧 |
| 数据处理 | 必须至少处理一个项目 |

### 你的任务

使用 do-while 循环正好显示 3 次菜单。
每次迭代应：

1. 显示菜单标题 `=== MENU ===`
2. 显示三个菜单选项
3. 显示当前的迭代次数

当计数器小于或等于 3 时，循环应继续执行。

### 菜单格式（每次迭代）

```
=== MENU ===
1. Exit
2. Say Hello
3. Say Goodbye
Iteration: [number]
```

### 方法签名

```csharp
public static void DisplayMenu()
```

### 预期输出

```
=== MENU ===
1. Exit
2. Say Hello
3. Say Goodbye
Iteration: 1
=== MENU ===
1. Exit
2. Say Hello
3. Say Goodbye
Iteration: 2
=== MENU ===
1. Exit
2. Say Hello
3. Say Goodbye
Iteration: 3
```

### 解答

```csharp
using System;

public class Solution
{
    public static void DisplayMenu()
    {
        // 计数器从 1 开始，do-while 保证菜单至少显示一次
        int counter = 1;
        do
        {
            Console.WriteLine("=== MENU ===");
            Console.WriteLine("1. Exit");
            Console.WriteLine("2. Say Hello");
            Console.WriteLine("3. Say Goodbye");
            Console.WriteLine($"Iteration: {counter}");
            counter++;
        } while (counter <= 3);
    }
}
```
