### For 循环

当您确切知道要迭代多少次时，可以使用 `for` 循环。
它将初始化、条件判断和迭代合并到一行中。

### For 循环语法

```csharp
for (initializer; condition; iterator)
{
    // 每次迭代要执行的代码
}
```

**三个部分：**

- **初始化器（Initializer）**：在循环开始前执行一次（例如 `int i = 0`）
- **条件（Condition）**：在每次迭代前进行检查；为 `true` 时循环继续
- **迭代器（Iterator）**：在每次迭代后执行（例如 `i++`）

### 示例

```csharp
// 打印 0 到 4
for (int i = 0; i < 5; i++)
{
    Console.WriteLine(i);
}

// 打印 5 到 1（递减计数）
for (int i = 5; i >= 1; i--)
{
    Console.WriteLine(i);
}

// 打印 2 到 10 的偶数
for (int i = 2; i <= 10; i += 2)
{
    Console.WriteLine(i);
}
```

### For 循环与 While 循环对比

| For 循环 | While 循环 |
| --- | --- |
| 最适合已知迭代次数的情况 | 最适合未知迭代次数的情况 |
| 初始化、条件和迭代器集中在一处 | 这些部分是分开的 |
| `for (int i = 0; i < 5; i++)` | `int i = 0; while (i < 5) { ... i++; }` |

### 您的任务

编写一个方法，使用 `for` 循环打印数字 1 到 10，每个数字占一行。

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
6
7
8
9
10
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintNumbers()
    {
        // 使用 for 循环打印数字 1 到 10，每个数字占一行
        for (int i = 1; i <= 10; i++)
        {
            Console.WriteLine(i);
        }
    }
}
```
