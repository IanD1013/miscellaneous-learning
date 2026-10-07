### If 语句

`if` 语句允许你在条件为 true 时才执行代码。
它是编程中进行决策的基础。

### 基本语法

```csharp
if (condition)
{
    // 仅当 condition 为 true 时代码才会运行
}
```

条件的求值结果必须是一个 `bool`（true 或 false）。
花括号 `{ }` 定义了要执行的代码块。

### 比较运算符

使用这些运算符来创建条件：

| 运算符 | 含义 | 示例 |
| --- | --- | --- |
| `>` | 大于 | `5 > 3` 为 true |
| `<` | 小于 | `2 < 7` 为 true |
| `>=` | 大于或等于 | `5 >= 5` 为 true |
| `<=` | 小于或等于 | `3 <= 4` 为 true |
| `==` | 等于 | `5 == 5` 为 true |
| `!=` | 不等于 | `5 != 3` 为 true |

### 示例

```csharp
int age = 18;
if (age >= 18)
{
    Console.WriteLine("You are an adult");
}

int temperature = 30;
if (temperature > 25)
{
    Console.WriteLine("It's hot outside");
}
```

### 你的任务

编写一个方法，检查一个数字是否为正数（大于 0）。
如果是，打印消息 `The number is positive`。
如果该数字是零或负数，则不打印任何内容。

### 方法签名

```csharp
public static void CheckPositive(int number)
```

### 预期结果

```
CheckPositive(5)   -> 打印 "The number is positive"
CheckPositive(100) -> 打印 "The number is positive"
CheckPositive(0)   -> 不打印任何内容
CheckPositive(-3)  -> 不打印任何内容
```

### 解答

```csharp
using System;

public class Solution
{
    public static void CheckPositive(int number)
    {
        // 仅当 number 大于 0 时打印 "The number is positive"
        if (number > 0)
        {
            Console.WriteLine("The number is positive");
        }
    }
}
```
