### 避免死循环

当循环条件永远不会变为 false 时，就会发生死循环（无限循环），导致程序一直运行下去（或直到崩溃）。

### 为什么循环会变成死循环

```csharp
// 有问题 - counter 从不改变，所以 counter <= 5 始终为 true
int counter = 1;
while (counter <= 5)
{
    Console.WriteLine(counter);
    // 缺少：counter++;
}

// 已修复 - counter 递增，最终使 counter <= 5 变为 false
int counter = 1;
while (counter <= 5)
{
    Console.WriteLine(counter);
    counter++;  // 这确保了循环会终止！
}
```

### 终止规则

每个 while 循环的主体内部都需要包含能使其逐步接近退出条件的操作：

| 循环类型 | 必须改变的内容 | 示例 |
| --- | --- | --- |
| 递增计数 | 增加计数器 | `counter++` |
| 递减计数 | 减少计数器 | `counter--` |
| 搜索 | 更新搜索位置 | `index++` |
| 基于输入 | 读取新输入 | `input = Console.ReadLine()` |

### 常见错误

```csharp
// 错误 1：忘记更新变量
int i = 0;
while (i < 10)
{
    Console.WriteLine(i);
    // 糟糕！i 从不改变
}

// 错误 2：更新方向错误
int i = 0;
while (i < 10)
{
    Console.WriteLine(i);
    i--;  // 方向反了！
}

// 错误 3：条件永远不会为 false
int x = 5;
while (x > 0)
{
    Console.WriteLine(x);
    x++;  // x 越来越大，永远不会到达 0
}
```

### 你的任务

初始代码中包含一个会无限运行下去的错误 while 循环。
通过添加缺失的代码行来修复它，确保循环最终能够终止。

该循环应打印数字 1 到 5，每行一个数字。

### 方法签名

```csharp
public static void FixInfiniteLoop()
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
    public static void FixInfiniteLoop()
    {
        // 这个循环原本有问题，会永远运行下去！
        // 修复它，使其从 1 数到 5 后停止
        
        int counter = 1;
        
        while (counter <= 5)
        {
            Console.WriteLine(counter);
            // 补上缺失的递增，使循环最终终止
            counter++;
        }
    }
}
```
