### 静态方法

静态方法属于类本身，而不是属于任何特定的实例。
你可以直接通过类名调用它们，而无需先创建对象。

### 调用静态方法与实例方法

```csharp
// 静态方法 - 在类上调用
double result = Math.Sqrt(16);  // 不需要创建 Math 对象
int max = Math.Max(5, 10);

// 实例方法 - 需要一个对象
string text = "hello";
string upper = text.ToUpper();  // 在字符串实例上调用
```

### 何时使用静态方法

静态方法非常适合用于满足以下条件的工具类操作：

- 不需要访问实例数据
- 仅使用传入的参数执行计算
- 提供在整个应用程序中共享的辅助功能

```csharp
public class StringHelper
{
    public static bool IsNullOrEmpty(string value)
    {
        return value == null || value.Length == 0;
    }
    
    public static string Reverse(string input)
    {
        char[] chars = input.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }
}

// 用法 - 不需要实例！
bool empty = StringHelper.IsNullOrEmpty("");
string reversed = StringHelper.Reverse("hello");
```

### 常用的 Math 类静态方法

| 方法 | 描述 | 示例 |
| --- | --- | --- |
| Math.PI | π 常量 | 3.14159... |
| Math.Sqrt(x) | 平方根 | Math.Sqrt(16) = 4 |
| Math.Pow(x, y) | 幂运算 x^y | Math.Pow(2, 3) = 8 |
| Math.Round(x, n) | 四舍五入到 n 位小数 | Math.Round(3.456, 2) = 3.46 |

### 你的任务

在 `MathUtilities` 类中创建一个静态工具方法 `CalculateCircleArea`，用于根据给定的半径计算圆的面积。

**公式：** 面积 = π × radius²

使用 `Math.PI` 获取圆周率的值。

### 方法签名

```csharp
public static double CalculateCircleArea(double radius)
```

### 预期结果

```
MathUtilities.CalculateCircleArea(1.0) -> 3.14
MathUtilities.CalculateCircleArea(5.0) -> 78.54
MathUtilities.CalculateCircleArea(0.0) -> 0.0
```

### 解答

```csharp
using System;

public class MathUtilities
{
    // 创建一个计算圆面积的静态方法
    // 公式：π × radius²
    // 使用 Math.PI 获取圆周率的值
    public static double CalculateCircleArea(double radius)
    {
        return Math.PI * radius * radius;
    }
}
```
