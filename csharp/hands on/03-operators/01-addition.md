### 加法运算符

`+` 运算符将两个值相加。
它是 C# 中最基础的算术运算符之一。

### 基本用法

```csharp
int sum = 5 + 3;      // sum = 8
int total = 10 + 20;  // total = 30
int result = 0 + 7;   // result = 7
```

### 变量相加

你可以将变量、字面量或两者混合相加：

```csharp
int a = 15;
int b = 25;
int sum = a + b;      // sum = 40
int mixed = a + 10;   // mixed = 25
```

### 处理负数

加法运算符可以与负数无缝配合使用：

```csharp
int result1 = 5 + (-3);   // result1 = 2
int result2 = -10 + -5;   // result2 = -15
int result3 = -7 + 7;     // result3 = 0
```

### 你的任务

创建一个方法，该方法接收两个整数，并使用 `+` 运算符返回它们的和。

### 方法签名

```csharp
public static int Add(int a, int b)
```

### 预期结果

```
Add(2, 3) -> 5
Add(10, 20) -> 30
Add(-5, 5) -> 0
```

### 解答

```csharp
using System;

public class Solution
{
    public static int Add(int a, int b)
    {
        // 使用 + 运算符返回两数之和
        return a + b;
    }
}
```
