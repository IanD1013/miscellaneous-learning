### 多行注释

多行注释允许你编写跨越多行的注释。
使用它们来解释复杂的逻辑，或临时禁用代码块。

### 语法

```csharp
/* 这是一条
   多行注释。
   它可以跨越很多行。 */
```

### 单行注释与多行注释

```csharp
// 单行注释 - 适合简短的备注
int x = 5; // 也可以写在行尾

/* 多行注释非常适合：
   - 解释算法
   - 临时禁用代码块 */
```

### 常见用途

| 用例 | 示例 |
| --- | --- |
| 方法文档 | `/* Calculates total price */` |
| 参数 | `/* a - first value, b - second */` |
| 禁用代码 | `/* Console.WriteLine("debug"); */` |

### return 关键字

`return` 关键字有两个作用：

1. **立即退出方法** - `return` 之后的代码不会执行
2. **将值返回给调用方** - 该值成为方法调用的结果

```csharp
public static int Double(int x)
{
    return x * 2;  // 返回翻倍后的值
}

int result = Double(5);  // result 现在是 10
```

`return` 后面的类型必须与方法的返回类型匹配（例如，`int` 方法必须返回一个 `int`）。

### 你的任务

`Calculate` 方法将两个数字相加，并使用 `return` 返回结果。
在**方法上方**（外部，而不是内部）添加一个恰当的多行注释，用于说明：

- 该方法的作用
- 参数是什么
- 它的返回值是什么

该方法已经可以正常工作 - 你只需要为其添加文档说明！

### 方法签名

```csharp
public static int Calculate(int a, int b)
```

### 预期结果

```
Calculate(2, 3) -> 5
Calculate(0, 0) -> 0
Calculate(-1, 1) -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    /* Calculate 方法：将两个整数相加。
       参数：a - 第一个整数，b - 第二个整数
       返回值：a 与 b 的和 */
    public static int Calculate(int a, int b)
    {
        return a + b;
    }
}
```
