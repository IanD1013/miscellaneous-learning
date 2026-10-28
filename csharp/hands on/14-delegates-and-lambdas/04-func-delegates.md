### Func 委托

`Func` 是一个内置的泛型委托类型，用于**有返回值**的方法。
`Action` 用于 void 方法，而 `Func` 将其最后一个类型参数作为返回类型。

### 声明与类型参数

```csharp
// Func<TResult> - 无参数，返回 TResult
Func<int> getNumber = () => 42;

// Func<T, TResult> - 一个 T 类型的参数，返回 TResult
Func<string, int> getLength = s => s.Length;

// Func<T1, T2, TResult> - 两个参数，返回 TResult
Func<int, int, int> add = (a, b) => a + b;

// 最多支持 16 个输入参数
Func<int, int, int, int> addThree = (a, b, c) => a + b + c;
```

### Func 对比 Action

| 委托 | 返回值 | 示例 |
| --- | --- | --- |
| `Action` | void（无） | `Action<string>` - 接收 string，无返回值 |
| `Func` | 一个值 | `Func<string, int>` - 接收 string，返回 int |

```csharp
// Action - 执行操作，无返回值
Action<string> print = msg => Console.WriteLine(msg);

// Func - 计算并返回一个值
Func<int, int> square = x => x * x;
int result = square(5); // 25
```

### 将 Func 用作参数

```csharp
// 只有当输入和输出类型相同时，才能将函数应用于它自己的输出，
// 因此一个类型参数就能同时涵盖两者
public static T ApplyTwice<T>(T value, Func<T, T> func)
{
    return func(func(value));
}

// 用法：
Func<int, int> doubleIt = x => x * 2;
int result = ApplyTwice(5, doubleIt); // 20
```

### 你的任务

实现一个计算器方法，该方法接收两个整数和一个 `Func<int, int, int>` 操作，然后返回将该操作应用于这两个数字的结果。

这种模式允许你在不更改方法签名的情况下传入不同的数学运算（加法、减法、乘法等）。

### 方法签名

```csharp
public static int Calculate(int a, int b, Func<int, int, int> operation)
```

### 预期结果

```
Calculate(10, 5, (a, b) => a + b) -> 15
Calculate(10, 5, (a, b) => a - b) -> 5
Calculate(10, 5, (a, b) => a * b) -> 50
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Calculate(int a, int b, Func<int, int, int> operation)
    {
        // 将操作应用于两个数字并返回结果
        return operation(a, b);
    }
}
```
