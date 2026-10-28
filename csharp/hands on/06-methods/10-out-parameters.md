### out 关键字

`out` 关键字允许方法通过传递变量来返回多个值，方法会对这些变量进行赋值。
与 `ref` 不同，`out` 参数在传递前不需要初始化。

### out 与 ref

```csharp
// ref：变量在传递前必须初始化
int refVar = 5;
SomeMethod(ref refVar);  // 可以读取并修改 refVar

// out：变量不需要初始化
int outVar;
SomeMethod(out outVar);  // 方法必须为 outVar 赋值
```

### 主要区别

| 特性 | ref | out |
| --- | --- | --- |
| 调用前必须初始化 | 是 | 否 |
| 方法必须为其赋值 | 否 | 是 |
| 可以读取传入的值 | 是 | 否（未定义） |
| 用途 | 修改现有值 | 返回额外的值 |

### 使用 out 参数

```csharp
// 带 out 参数的方法
public static bool TryParse(string input, out int result)
{
    // out 参数必须在返回前赋值
    result = 0;  // 赋默认值
    
    if (int.TryParse(input, out int parsed))
    {
        result = parsed;
        return true;
    }
    return false;
}

// 调用该方法
if (TryParse("42", out int value))
{
    Console.WriteLine(value);  // 42
}
```

### 内联声明

C# 允许在调用方法时内联声明 `out` 变量：

```csharp
// 旧写法
int quotient;
int remainder;
Divide(10, 3, out quotient, out remainder);

// 现代内联写法
Divide(10, 3, out int quotient, out int remainder);
```

### 你的任务

创建一个 `Divide` 方法，该方法执行整数除法，并使用 `out` 参数返回商和余数。

- 如果除法成功，返回 `true`
- 如果除数为零，返回 `false`（避免除以零）
- 当除数为零时，将商和余数均设为 0
- 查看 `DivisionHelper.cs` 文件中的辅助方法以格式化结果

### 方法签名

```csharp
public static bool Divide(int dividend, int divisor, out int quotient, out int remainder)
```

### 预期结果

```csharp
Divide(10, 3, out q, out r) -> true, q=3, r=1
Divide(17, 5, out q, out r) -> true, q=3, r=2
Divide(10, 0, out q, out r) -> false, q=0, r=0
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool Divide(int dividend, int divisor, out int quotient, out int remainder)
    {
        // 除数为零时，两个 out 参数都设为 0 并返回 false
        if (divisor == 0)
        {
            quotient = 0;
            remainder = 0;
            return false;
        }

        // 用 out 参数同时返回商和余数
        quotient = dividend / divisor;
        remainder = dividend % divisor;
        return true;
    }
    
    // 这个包装方法用于测试 - 不要修改
    public static string DivideAndFormat(int dividend, int divisor)
    {
        bool success = Divide(dividend, divisor, out int quotient, out int remainder);
        return DivisionHelper.FormatResult(success, quotient, remainder);
    }
}
```
