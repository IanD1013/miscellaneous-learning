### 方法重载（Method Overloading）

方法重载允许你创建多个同名但参数不同的方法。
编译器会根据你传递的参数来决定调用哪一个方法。

### 为什么要使用重载？

重载可以让你的代码更加直观。
无需分别创建 `AddTwoNumbers()` 和 `AddThreeNumbers()`，你只需创建一个能接收不同数量参数的 `Add()` 即可。

### 工作原理

```csharp
// 两个同名但参数数量不同的方法
public static int Multiply(int a, int b)
{
    return a * b;
}

public static int Multiply(int a, int b, int c)
{
    return a * b * c;
}

// 编译器根据实参选择正确的版本
int result1 = Multiply(2, 3);       // 调用第一个版本：6
int result2 = Multiply(2, 3, 4);    // 调用第二个版本：24
```

### 重载规则

| 有效差异 | 示例 |
| --- | --- |
| 参数数量 | `Add(int a, int b)` 与 `Add(int a, int b, int c)` |
| 参数类型 | `Print(int x)` 与 `Print(string x)` |
| 参数类型的顺序 | `Process(int a, string b)` 与 `Process(string a, int b)` |

**注意：** 仅返回值类型不同**不足以**构成有效的方法重载。

### 你的任务

创建两个重载的 `Add` 方法：

1. `Add(int a, int b)` - 返回两个整数的和
2. `Add(int a, int b, int c)` - 返回三个整数的和

### 方法签名

```csharp
public static int Add(int a, int b)
public static int Add(int a, int b, int c)
```

### 预期结果

```
Add(5, 3) -> 8
Add(1, 2, 3) -> 6
Add(-5, 5) -> 0
Add(10, 20, 30) -> 60
```

### 解答

```csharp
using System;

public class Solution
{
    // 接收 2 个整数并返回它们之和的 Add 方法
    public static int Add(int a, int b)
    {
        return a + b;
    }
    
    // 接收 3 个整数并返回它们之和的重载 Add 方法
    public static int Add(int a, int b, int c)
    {
        return a + b + c;
    }
}
```
