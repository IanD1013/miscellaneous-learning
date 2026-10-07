### int 类型

`int` 类型用于存储整数，包括正数和负数，但不包含小数。
它是一个 **32 位有符号整数**，这意味着它使用 32 位（4 字节）的内存来存储数值。

### 声明 int 变量

```csharp
// 在一行中声明并赋值
int age = 25;
int year = 2024;

// 先声明，稍后赋值
int score;
score = 100;
```

### 正数和负数

```csharp
int temperature = -10;    // 负数
int altitude = 8848;      // 正数
int balance = 0;          // 零也是有效的
```

### 使用 int 进行基本数学运算

```csharp
int a = 10;
int b = 3;
int sum = a + b;          // 13
int difference = a - b;   // 7
int product = a * b;      // 30
```

### int 范围（32 位）

因为 `int` 是 32 位有符号整数，所以它可以存储以下范围内的值：

| 属性 | 值 |
| --- | --- |
| 大小 | 32 位（4 字节） |
| 最小值 | -2,147,483,648 |
| 最大值 | 2,147,483,647 |

你可以在代码中使用 `int.MinValue` 和 `int.MaxValue` 来访问这些限制。

### 你的任务

完成以下四个方法：

1. `GetAge()` - 声明一个设为 25 的 int 变量 `age`，并将其返回
2. `GetYear()` - 声明一个设为 2024 的 int 变量 `year`，并将其返回
3. `GetTemperature()` - 声明一个设为 -5 的 int 变量 `temperature`，并将其返回
4. `AddNumbers(int a, int b)` - 返回两个参数的和

### 方法签名

```csharp
public static int GetAge()
public static int GetYear()
public static int GetTemperature()
public static int AddNumbers(int a, int b)
```

### 预期结果

```
GetAge() -> 25
GetYear() -> 2024
GetTemperature() -> -5
AddNumbers(10, 5) -> 15
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetAge()
    {
        // 声明一个名为 age 的 int 变量，赋值为 25
        int age = 25;
        // 返回 age 变量
        return age;
    }
    
    public static int GetYear()
    {
        // 声明一个名为 year 的 int 变量，赋值为 2024
        int year = 2024;
        // 返回 year 变量
        return year;
    }
    
    public static int GetTemperature()
    {
        // 声明一个名为 temperature 的 int 变量，赋值为 -5
        int temperature = -5;
        // 返回 temperature 变量
        return temperature;
    }
    
    public static int AddNumbers(int a, int b)
    {
        // 返回 a 与 b 的和
        return a + b;
    }
}
```
