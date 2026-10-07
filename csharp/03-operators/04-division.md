### 除法运算符

除法运算符 `/` 用于计算一个数除以另一个数。
与整数除法不同，使用 `double` 会保留小数精度。

### 基本用法

```csharp
double result1 = 10.0 / 2.0;  // result1 = 5.0
double result2 = 7.0 / 2.0;   // result2 = 3.5
double result3 = 1.0 / 4.0;   // result3 = 0.25
```

### 整数除法与 Double 除法

在对整数进行除法运算时，C# 会截断小数部分。
使用 `double` 则会保留小数部分。

```csharp
int intResult = 7 / 2;        // intResult = 3（被截断！）
double doubleResult = 7.0 / 2.0;  // doubleResult = 3.5（被保留）
```

### 特殊情况

```csharp
double divByZero = 5.0 / 0.0;     // 结果：Infinity
double zeroNumerator = 0.0 / 5.0; // 结果：0
double negResult = -10.0 / 4.0;   // 结果：-2.5
```

### 你的任务

实现一个方法，计算第一个数除以第二个数并返回结果。

### 方法签名

```csharp
public static double Divide(double a, double b)
```

### 预期结果

```
Divide(10.0, 2.0) -> 5.0
Divide(7.0, 2.0) -> 3.5
Divide(15.0, 4.0) -> 3.75
```

### 解答

```csharp
using System;

public class Solution
{
    public static double Divide(double a, double b)
    {
        // 两个 double 相除，保留小数部分
        return a / b;
    }
}
```
