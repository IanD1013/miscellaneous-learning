### Lambda 表达式

Lambda 表达式是编写匿名方法的一种简洁方式。
你无需声明完整的方法，而是可以使用 `=>`（箭头）语法来定义内联逻辑。

### 基本语法

```csharp
// 单个参数 - 括号可选
x => x * 2           // 将 x 翻倍
(x) => x * 2         // 加上括号，效果相同

// 多个参数 - 必须使用括号
(a, b) => a + b      // 两数相加

// 无参数
() => 42             // 返回 42
```

### Lambda 与传统方法对比

```csharp
// 传统方法
public static int Double(int x)
{
    return x * 2;
}

// Lambda 表达式（简短得多！）
Func<int, int> doubler = x => x * 2;
```

### 表达式 Lambda 与语句 Lambda

```csharp
// 表达式 Lambda（单个表达式，隐式返回）
Func<int, int> square = x => x * x;

// 语句 Lambda（多条语句，显式返回）
Func<int, int> squareVerbose = x => {
    int result = x * x;
    return result;
};
```

### 将 Lambda 与 Func 结合使用

| Lambda | 描述 | 调用示例 |
| --- | --- | --- |
| `x => x * 2` | 将输入翻倍 | `transform(5)` → 10 |
| `x => x * x` | 计算输入的平方 | `transform(4)` → 16 |
| `x => -x` | 对输入取反 | `transform(3)` → -3 |

### 你的任务

实现三个方法，每个方法返回一个 lambda 表达式：

1. `GetDoubler()` - 返回一个将输入翻倍的 lambda
2. `GetSquarer()` - 返回一个计算输入平方的 lambda
3. `GetNegator()` - 返回一个对输入取反的 lambda

### 方法签名

```csharp
public static Func<int, int> GetDoubler()
public static Func<int, int> GetSquarer()
public static Func<int, int> GetNegator()
```

### 预期结果

```
GetDoubler()(5) -> 10
GetSquarer()(4) -> 16
GetNegator()(7) -> -7
```

### 解答

```csharp
using System;

public class Solution
{
    public static int ApplyTransform(int number, Func<int, int> transform)
    {
        return transform(number);
    }
    
    public static Func<int, int> GetDoubler()
    {
        // 返回一个将输入翻倍的 lambda
        return x => x * 2;
    }
    
    public static Func<int, int> GetSquarer()
    {
        // 返回一个计算输入平方的 lambda
        return x => x * x;
    }
    
    public static Func<int, int> GetNegator()
    {
        // 返回一个对输入取反的 lambda（乘以 -1）
        return x => -x;
    }
}
```
