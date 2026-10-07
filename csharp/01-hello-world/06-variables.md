### C# 中的变量

变量是用于存储数据值的容器。
你可以通过指定其类型并为其命名来声明一个变量。

### 声明变量

```csharp
// 语法：type variableName = value;
int age = 25;
bool isActive = true;
double price = 9.99;
```

### 常见数据类型

| 类型 | 说明 | 示例 |
| --- | --- | --- |
| `int` | 整数 | `42` |
| `double` | 小数 | `3.14` |
| `bool` | True 或 false | `true` |
| `string` | 文本/字符 | `"Hello"` |

### 变量命名规则

```csharp
// 有效的变量名
int playerScore = 100;
bool isGameOver = false;
int totalItems = 5;

// 无效 - 不能以数字开头
// int 1stPlace = 1;  // 错误！

// 无效 - 不能使用保留字
// int class = 5;  // 错误！
```

### 基本数学运算

你可以对数字进行运算：

```csharp
int a = 10;
int b = 3;

int sum = a + b;       // 13
int difference = a - b; // 7
int product = a * b;    // 30
int quotient = a / b;   // 3（整数除法）
```

### 什么是方法？

**方法**（method）是一个用于执行特定任务的可复用代码块。
可以把它想象成一个食谱：你给它配料（输入），它按照指令操作，并给你一个结果（输出）。

```csharp
// 这是一个接收一个数字并返回其两倍的方法
public static int DoubleNumber(int number)
{
    // { } 里面的代码就是这个方法要做的事
    int result = number * 2;
    return result;  // 把结果返回
}
```

**解析方法签名：**

- `public static` - 暂时不用担心这些，它们是必需的关键字
- `int` - **返回类型** - 该方法返回的值的类型
- `DoubleNumber` - 方法的**名称**
- `(int number)` - **参数** - 方法接收的输入

### `return` 关键字

`return` 关键字用于从方法中返回一个值。
可以把它想象成回答一个问题：

```csharp
// 有人问：“5 的两倍是多少？”
// 方法回答：10

public static int DoubleNumber(int number)
{
    int doubled = number * 2;
    return doubled;  // 这就是答案！
}
```

当方法具有返回类型（如 `int`）时，它**必须**使用 `return` 返回该类型的值。

### 你的任务

完成接收一个数字并返回其两倍（乘以 2）的方法。
你需要：

1. 创建一个 `int` 变量来存储结果
2. 将 `number` 参数乘以 2
3. 使用 `return` 将结果返回

### 方法签名

```csharp
public static int DoubleNumber(int number)
```

### 预期结果

```
DoubleNumber(5) -> 10
DoubleNumber(3) -> 6
```

### 解答

```csharp
using System;

public class Solution
{
    public static int DoubleNumber(int number)
    {
        // 创建一个变量来存储结果，并将数字乘以 2
        int result = number * 2;
        // 返回结果
        return result;
    }
}
```
