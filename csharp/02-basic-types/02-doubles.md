### double 类型

`double` 是一种用于存储小数值的 64 位浮点数。
当需要表示诸如温度、测量值或科学常数等小数时，可以使用它。

### 声明 double 变量

```csharp
// 声明一个 double 变量并赋值
double temperature = 36.5;
double pi = 3.14159;
double negativeValue = -273.15;
```

### double 与 int

整数（`int`）只能保存没有小数部分的整数。
当你需要小数精度的数值时，请使用 `double`。

```csharp
int wholeNumber = 36;        // 不允许小数
double preciseValue = 36.5;  // 小数值会被保留
```

### 使用小数点

为 double 赋值时，包含小数点可以使你的意图更加明确：

```csharp
double exactValue = 100.0;   // 清晰：这是一个 double
double fraction = 0.5;       // 小数值完全可用
double negative = -40.0;     // 负小数也可以
```

### 你的任务

创建以 `double` 值返回重要温度和科学常数的方法。
每个方法都应声明一个 `double` 变量，赋予指定的值，并将其返回。

### 方法签名

```csharp
public static double GetBoilingPointFahrenheit()   // 返回 212.0
public static double GetFreezingPointFahrenheit()  // 返回 32.0
public static double GetAbsoluteZeroCelsius()      // 返回 -273.15
public static double GetPi()                       // 返回 3.14159
public static double GetBodyTemperatureCelsius()   // 返回 37.0
```

### 预期结果

```
GetBoilingPointFahrenheit() -> 212.0
GetFreezingPointFahrenheit() -> 32.0
GetAbsoluteZeroCelsius() -> -273.15
GetPi() -> 3.14159
GetBodyTemperatureCelsius() -> 37.0
```

### 解答

```csharp
using System;

public class Solution
{
    public static double GetBoilingPointFahrenheit()
    {
        // 水的沸点是 212.0 华氏度
        double boilingPoint = 212.0;
        return boilingPoint;
    }

    public static double GetFreezingPointFahrenheit()
    {
        // 水的冰点是 32.0 华氏度
        double freezingPoint = 32.0;
        return freezingPoint;
    }

    public static double GetAbsoluteZeroCelsius()
    {
        // 绝对零度是 -273.15 摄氏度
        double absoluteZero = -273.15;
        return absoluteZero;
    }

    public static double GetPi()
    {
        // Pi 约等于 3.14159
        double pi = 3.14159;
        return pi;
    }

    public static double GetBodyTemperatureCelsius()
    {
        // 人体正常体温是 37.0 摄氏度
        double bodyTemperature = 37.0;
        return bodyTemperature;
    }
}
```
