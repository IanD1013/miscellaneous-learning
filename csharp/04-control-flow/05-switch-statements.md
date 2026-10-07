### Switch 语句

`switch` 语句将单个值与一组常量选项列表进行比较，并运行匹配的分支。
当一个变量可以具有多个已知值（例如菜单选项、状态码、月份数字）时，它是惯用的选择，因为它的可读性比一长串 `else if` 比较更加清晰。

### 工作原理

括号中的值只会被计算一次，然后自上而下与每个 `case` 标签进行比较。
当标签匹配时，其下方的语句会一直运行，直到该分支被 `break`（离开 switch）或 `return`（离开整个方法）结束。
如果没有匹配项，则会运行 `default` 分支，如果没有 `default`，switch 将不执行任何操作。

### 关于花括号的说明

`switch` 块本身始终需要花括号 `{ }`，但各个 `case` 分支**不**需要，`case` 标签及其语句本身就作为一个分支。
这与适用于 `if`/`else` 的规则相同：当一个分支仅包含**一条**语句时，花括号是可选的。

```csharp
// 省略花括号 - 合法，因为每个分支都只有一条语句
if (temperature > 30)
    Console.WriteLine("Hot");
else
    Console.WriteLine("Not hot");

// 一旦某个分支有多于一条语句，就必须使用花括号
if (temperature > 30)
{
    Console.WriteLine("Hot");
    Console.WriteLine("Drink water");
}
```

为了安全性和一致性，许多团队仍然会在所有地方添加花括号。
无论你选择哪种风格，请在一个代码块内保持一致，在同一个语句中混合使用单行和多行分支会使代码更难于浏览。
下面的示例始终将每条语句放在独立的一行上。

### 语法

```csharp
switch (expression)
{
    case constant1:
        // constant1 对应的语句
        break;
    case constant2:
        // constant2 对应的语句
        break;
    default:
        // 没有任何匹配时执行的语句
        break;
}
```

### 示例

```csharp
// 示例 1：根据交通信号灯颜色打印消息
switch (light)
{
    case "green":
        Console.WriteLine("Go");
        break;
    case "amber":
        Console.WriteLine("Prepare to stop");
        break;
    case "red":
        Console.WriteLine("Stop");
        break;
    default:
        Console.WriteLine("Unknown signal");
        break;
}
```

```csharp
// 示例 2：赋一个值，然后在 switch 之后使用它
string meaning;

switch (grade)
{
    case 'A':
        meaning = "Excellent";
        break;
    case 'B':
        meaning = "Good";
        break;
    case 'C':
        meaning = "Average";
        break;
    default:
        meaning = "Unknown";
        break;
}

Console.WriteLine(meaning);
```

### 使用 return 代替 break

在返回某个值的方法内部，分支可以直接 `return`。
`return` 已经退出了方法，因此其后的 `break` 将无法执行且无法通过编译，两者只能选其一，绝不能同时使用：

```csharp
public static string DescribeStatus(int status)
{
    switch (status)
    {
        case 1:
            return "Active";
        case 2:
            return "Suspended";
        default:
            return "Unknown";
    }
}
```

### 实用参考

| 组件 | 用途 | 是否必需？ |
| --- | --- | --- |
| `case` | 声明要匹配的常量值 | 是，至少一个 |
| `break` | 结束分支并退出 switch | 是，除非分支执行了 `return` 或 `throw` |
| `return` | 结束分支并退出整个方法 | `break` 的替代方案 |
| `default` | 当没有 `case` 匹配时运行 | 可选，但建议使用 |

### 你的任务

编写一个方法，将星期几的数字转换为对应的星期名称，其中星期一为 1，星期日为 7。
任何其他数字，即负数、零或大于 7 的数字，都必须输出文本 `Invalid day`。
使用 `switch` 语句而不是 `if`/`else if` 链，并保持格式一致。

### 方法签名

```csharp
public static string GetDayName(int dayNumber)
```

### 预期结果

```
GetDayName(1) -> "Monday"
GetDayName(3) -> "Wednesday"
GetDayName(7) -> "Sunday"
GetDayName(0) -> "Invalid day"
GetDayName(8) -> "Invalid day"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetDayName(int dayNumber)
    {
        // 每个分支直接 return，因此不需要 break
        switch (dayNumber)
        {
            case 1:
                return "Monday";
            case 2:
                return "Tuesday";
            case 3:
                return "Wednesday";
            case 4:
                return "Thursday";
            case 5:
                return "Friday";
            case 6:
                return "Saturday";
            case 7:
                return "Sunday";
            default:
                // 负数、零或大于 7 的数字
                return "Invalid day";
        }
    }
}
```
