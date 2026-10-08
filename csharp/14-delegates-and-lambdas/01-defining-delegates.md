### 委托 (Delegates)

委托是一种表示对具有特定参数列表和返回类型的方法的引用的类型。
可以将其视为一个“方法指针”，允许你将方法作为参数进行传递。

### 声明委托类型

```csharp
// 语法：[访问修饰符] delegate [返回类型] [委托名称]([参数]);
public delegate int MathOperation(int x, int y);
public delegate void Logger(string message);
public delegate bool Predicate(int value);
```

### 使用委托

```csharp
// 1. 声明委托类型
public delegate int Calculator(int a, int b);

// 2. 创建一个与签名匹配的方法
public static int Add(int x, int y) => x + y;

// 3. 创建指向该方法的委托实例
Calculator calc = Add;

// 4. 调用委托（调用被引用的方法）
int result = calc(5, 3);  // result = 8
```

### 委托作为参数

```csharp
// 方法可以接收委托作为参数
public static int Execute(int a, int b, Calculator operation)
{
    return operation(a, b);  // 调用委托
}

// 使用不同的方法调用
int sum = Execute(10, 5, Add);       // 15
int diff = Execute(10, 5, Subtract); // 5
```

### 你的任务

1. 定义一个名为 `MathOperation` 的委托类型，满足：

   - 接收两个 `int` 类型的参数
   - 返回一个 `int` 类型的值
2. 实现 `ApplyOperation` 方法，满足：

   - 接收两个整数以及一个 `MathOperation` 委托
   - 使用这两个整数调用该委托
   - 返回调用结果

### 方法签名

```csharp
public delegate int MathOperation(int x, int y);
public static int ApplyOperation(int a, int b, MathOperation operation)
```

### 预期结果

```
ApplyOperation(10, 5, Add) -> 15
ApplyOperation(10, 5, Subtract) -> 5
ApplyOperation(6, 7, Multiply) -> 42
```

### 解答

```csharp
using System;

// 第 1 步：定义一个名为 'MathOperation' 的委托类型
// 它接收两个 int 参数并返回一个 int
public delegate int MathOperation(int x, int y);

public class Solution
{
    // 第 2 步：实现使用该委托的 ApplyOperation 方法
    public static int ApplyOperation(int a, int b, MathOperation operation)
    {
        // 使用这两个整数调用委托并返回结果
        return operation(a, b);
    }
    
    // 可以配合委托使用的辅助方法
    public static int Add(int x, int y) => x + y;
    public static int Subtract(int x, int y) => x - y;
    public static int Multiply(int x, int y) => x * y;
    public static int Divide(int x, int y) => x / y;
}
```
