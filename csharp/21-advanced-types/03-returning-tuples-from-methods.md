### 从方法返回元组

元组非常适合用于需要返回多个相关值而无需创建自定义类的方法。

### 为什么返回元组？

传统上，返回多个值需要创建一个类或使用 `out` 参数：

```csharp
// 使用 out 参数的旧方法
public static void GetStats(int[] arr, out int min, out int max)
{
    min = arr.Min();
    max = arr.Max();
}

// 元组方法 - 更简洁！
public static (int Min, int Max) GetStats(int[] arr)
{
    return (arr.Min(), arr.Max());
}
```

### 声明返回类型

在方法签名中使用包含类型（以及可选名称）的圆括号：

```csharp
// 未命名的元组返回
public static (int, int) Divide(int a, int b)
{
    return (a / b, a % b);  // 商和余数
}

// 命名的元组返回 - 可读性更高
public static (int Quotient, int Remainder) Divide(int a, int b)
{
    return (a / b, a % b);
}
```

### 使用返回值

```csharp
var result = Divide(10, 3);
Console.WriteLine(result.Quotient);  // 3
Console.WriteLine(result.Remainder); // 1

// 或者使用解构
var (q, r) = Divide(10, 3);
```

### 你的任务

编写一个方法，查找整数数组中的最小值和最大值，并将它们作为具名元组返回。

该方法应该：

- 接收一个整数数组
- 返回一个包含 `Min` 和 `Max` 具名元素的元组
- 找出数组中的最小值和最大值

### 方法签名

```csharp
public static (int Min, int Max) FindMinMax(int[] numbers)
```

### 预期结果

```
FindMinMax([1, 5, 3, 9, 2]) -> (1, 9)
FindMinMax([7]) -> (7, 7)
FindMinMax([-5, 0, 5]) -> (-5, 5)
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static (int Min, int Max) FindMinMax(int[] numbers)
    {
        return (numbers.Min(), numbers.Max());
    }
}
```
