### 使用返回值

当方法返回一个值时，你可以将其存储在变量中，或者直接在表达式中使用它。
这让你可以通过简单且可复用的方法构建复杂的逻辑。

### 存储返回值

```csharp
// 将返回值存储在变量中
int result = SomeMethod(5);
Console.WriteLine(result);

// 在后续计算中使用该变量
int doubled = result * 2;
```

### 直接使用返回值

```csharp
// 直接在表达式中使用返回值
int total = SomeMethod(5) * 10;

// 将返回值传递给另一个方法
int final = AnotherMethod(SomeMethod(5));
```

### 链式方法调用

```csharp
// 方法可以使用其他方法的返回值
public static int Square(int n)
{
    return n * n;
}

public static int SumOfSquares(int a, int b)
{
    return Square(a) + Square(b);
}
```

### 你的任务

创建两个方法：

1. **Add** - 接收两个整数并返回它们的和
2. **Calculate** - 接收三个整数 (a, b, c) 并返回 `Add(a, b) * c`

关键是在 `Calculate` 内部调用 `Add` 方法并使用其返回值。

### 方法签名

```csharp
public static int Add(int x, int y)
public static int Calculate(int a, int b, int c)
```

### 预期结果

```
Calculate(2, 3, 4) -> 20   // (2 + 3) * 4 = 20
Calculate(5, 5, 2) -> 20   // (5 + 5) * 2 = 20
Calculate(0, 10, 5) -> 50  // (0 + 10) * 5 = 50
```

### 解答

```csharp
using System;

public class Solution
{
    // 第 1 步：创建 Add 方法，接收两个整数并返回它们的和
    public static int Add(int x, int y)
    {
        return x + y;
    }
    
    // 第 2 步：在计算中使用 Add 方法的返回值
    // 计算：Add(a, b) 乘以 c
    public static int Calculate(int a, int b, int c)
    {
        // 调用 Add 并使用它的结果
        return Add(a, b) * c;
    }
}
```
