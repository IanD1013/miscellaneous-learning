### 隐式转换

当你将一种类型的值赋给兼容的更大类型的变量时，隐式转换会自动发生，且不会丢失任何数据。

### 隐式转换的工作原理

```csharp
int wholeNumber = 42;
double decimalNumber = wholeNumber;  // 隐式转换：42 变为 42.0

int small = 100;
long big = small;  // int 转 long 同样是隐式的

float f = 3.14f;
double d = f;  // float 转 double 是隐式的
```

### 为什么它是安全的

当不会丢失数据时，隐式转换是允许的。
`int` 可以保存从 -2,147,483,648 到 2,147,483,647 的值。
`double` 可以保存大得多的值以及小数，因此任何 `int` 都可以安全地放入 `double` 中。

```csharp
// 安全：double 可以保存任何 int 值
int age = 25;
double ageAsDouble = age;  // 25.0

// 不允许隐式转换（会丢失小数精度）
double price = 19.99;
int priceAsInt = price;  // 编译错误！
```

### 常见的隐式转换

| 源类型 | 目标类型 | 示例 |
| --- | --- | --- |
| int | long | `long x = 100;` |
| int | float | `float x = 100;` |
| int | double | `double x = 100;` |
| float | double | `double x = 3.14f;` |
| char | int | `int x = 'A';` (65) |

### 你的任务

编写一个方法，接收一个 `int` 参数，并通过隐式转换将其作为 `double` 返回。
只需将 int 赋值给 double 变量并返回即可。

### 方法签名

```csharp
public static double ConvertToDouble(int number)
```

### 预期结果

```
ConvertToDouble(42) -> 42.0
ConvertToDouble(-10) -> -10.0
ConvertToDouble(0) -> 0.0
```

### 解答

```csharp
using System;

public class Solution
{
    public static double ConvertToDouble(int number)
    {
        // 将 int 赋值给 double 变量，发生隐式转换
        double result = number;
        return result;
    }
}
```
