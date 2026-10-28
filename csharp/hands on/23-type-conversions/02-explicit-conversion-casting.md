### 显式转换（强制类型转换 / Casting）

显式转换（Explicit conversion），也称为强制类型转换（casting），在将较大类型转换为较小类型，或在可能发生数据丢失的不兼容类型之间进行转换时是必需的。

### 为什么需要强制类型转换

与隐式转换（自动发生）不同，显式转换要求你明确告诉编译器：“我知道这可能会丢失数据，但无论如何都要执行转换。”

```csharp
double price = 19.99;
int wholePrice = (int)price;  // 需要显式强制转换 - 结果为 19
```

### 强制转换语法

在值的前面加上放在圆括号中的目标类型：

```csharp
(targetType)value

// 示例：
double d = 9.7;
int i = (int)d;        // i = 9（截断，而不是四舍五入！）

long bigNumber = 1000L;
int smaller = (int)bigNumber;  // 如果值能放入 int 则可行
```

### 截断与四舍五入

**重要提示：** 转换为 `int` 会截断（移除）小数部分，**不会**进行四舍五入！

```csharp
double a = 3.9;
int x = (int)a;  // x = 3（不是 4！）

double b = -2.7;
int y = (int)b;  // y = -2（向零截断）
```

### 隐式转换与显式转换

| 转换 | 示例 | 类型 |
| --- | --- | --- |
| int → double | `double d = 5;` | 隐式（安全） |
| double → int | `int i = (int)5.9;` | 显式（可能丢失数据） |
| long → int | `int i = (int)bigNum;` | 显式（可能溢出） |

### 你的任务

实现一个方法，接收一个 `double` 值并返回其强制转换为 `int` 后的结果。
观察小数部分是如何被截断的。

### 方法签名

```csharp
public static int CastToInt(double value)
```

### 预期结果

```
CastToInt(3.14) -> 3
CastToInt(9.99) -> 9
CastToInt(-2.7) -> -2
```

### 解答

```csharp
using System;

public class Solution
{
    public static int CastToInt(double value)
    {
        // 显式强制转换为 int，小数部分会向零截断
        return (int)value;
    }
}
```
