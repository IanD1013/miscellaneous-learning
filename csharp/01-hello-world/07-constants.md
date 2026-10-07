### C# 中的常量

常量是在定义后无法更改的值。
使用 `const` 关键字来声明在整个程序运行期间保持不变的值。

### 声明常量

```csharp
const double SpeedOfLight = 299792458.0;
const int MaxRetries = 3;
const string AppName = "MyApplication";
```

### 常量与变量

| 特性 | 常量 (`const`) | 变量 |
| --- | --- | --- |
| 是否可更改 | 否 | 是 |
| 必须赋值时机 | 声明时 | 可以稍后 |
| 编译期 | 编译时已知值 | 可以为运行时值 |

```csharp
const int MaxScore = 100;    // 不能更改
int currentScore = 0;         // 可以更改
currentScore = 50;            // 没问题
// MaxScore = 200;            // 错误：不能给 const 赋值
```

### 命名规范

C# 常量通常使用 **PascalCase**：

```csharp
const double Pi = 3.14159;
const int DaysInWeek = 7;
const string DefaultGreeting = "Hello";
```

### 从另一个类访问静态成员

当常量（或任何静态成员）定义在单独的类中时，你可以使用**类名**后跟一个**点**和**成员名称**来访问它们。
这被称为**点表示法**。

```csharp
// 在 MathConstants 类中：
public static class MathConstants
{
    public const double Pi = 3.14159;
    public const int DaysInWeek = 7;
}

// 在另一个类中使用这些常量：
double circleConstant = MathConstants.Pi;     // 返回 3.14159
int days = MathConstants.DaysInWeek;          // 返回 7
```

**为什么能这样使用？**

- `const` 关键字使该值成为类的**静态成员**（常量隐式为静态）
- 静态成员属于**类本身**，而不是任何实例
- 你可以使用 `ClassName.MemberName` 语法访问静态成员

```csharp
// 这种模式适用于所有静态成员：
int result = Math.Max(5, 10);           // 内置的 Math 类
string text = String.Empty;              // 内置的 String 类
double pi = MathConstants.Pi;            // 我们自定义的类
```

### 你的任务

`MathConstants.cs` 文件包含三个有用的常量。
你的任务是使用类名访问并返回每个常量的值：

1. **GetCircleConstant**：返回 `MathConstants.Pi` 的值
2. **GetDaysInWeek**：返回 `MathConstants.DaysInWeek` 的值
3. **GetHoursInDay**：返回 `MathConstants.HoursInDay` 的值

查看 `MathConstants.cs` 文件（点击标签页）以了解可用的常量。

### 方法签名

```csharp
public static double GetCircleConstant()
public static int GetDaysInWeek()
public static int GetHoursInDay()
```

### 预期结果

```
GetCircleConstant() -> 3.14159
GetDaysInWeek() -> 7
GetHoursInDay() -> 24
```

### 解答

`Main.cs`

```csharp
using System;

public class Solution
{
    // 使用 MathConstants 类中的常量

    public static double GetCircleConstant()
    {
        // 返回 MathConstants 中 Pi 的值
        return MathConstants.Pi;
    }

    public static int GetDaysInWeek()
    {
        // 返回 MathConstants 中一周的天数
        return MathConstants.DaysInWeek;
    }

    public static int GetHoursInDay()
    {
        // 返回 MathConstants 中一天的小时数
        return MathConstants.HoursInDay;
    }
}
```
