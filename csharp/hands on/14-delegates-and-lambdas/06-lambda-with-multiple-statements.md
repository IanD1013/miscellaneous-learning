### 语句 Lambda（多行 Lambda）

当 Lambda 表达式需要包含多个语句时，可以使用大括号 `{ }` 来创建一个**语句 Lambda**（也称为块 Lambda）。

### 表达式 Lambda 与语句 Lambda

```csharp
// 表达式 Lambda - 单个表达式，隐式返回
Func<int, int> square = x => x * x;

// 语句 Lambda - 多条语句，必须显式返回
Func<int, int> process = x =>
{
    int doubled = x * 2;
    int result = doubled + 5;
    return result;  // 必须使用 'return' 关键字
};
```

### 语句 Lambda 语法

```csharp
// 一个参数
Func<int, int> transform = n =>
{
    // 多行代码
    int step1 = n * 2;
    int step2 = step1 + 10;
    return step2;
};

// 多个参数
Func<int, int, int> combine = (a, b) =>
{
    int sum = a + b;
    int product = a * b;
    return sum + product;
};
```

### 主要区别

| 特性 | 表达式 Lambda | 语句 Lambda |
| --- | --- | --- |
| 语法 | `x => expression` | `x => { statements }` |
| 返回值 | 隐式 | 必须显式使用 `return` |
| 代码行数 | 单个表达式 | 多个语句 |
| 使用场景 | 简单转换 | 复杂逻辑 |

### 你的任务

创建一个语句 Lambda，通过多个步骤处理一个数字：

1. 如果数字为负数，将其转换为正数（绝对值）
2. 将该数字翻倍
3. 在结果上加 10
4. 返回最终值

### 方法签名

```csharp
public static int RunComplexProcessing(int number)
```

### 预期结果

```
RunComplexProcessing(5) -> 20    // 5 * 2 + 10 = 20
RunComplexProcessing(-3) -> 16   // |-3| = 3, 3 * 2 + 10 = 16
RunComplexProcessing(0) -> 10    // 0 * 2 + 10 = 10
```

### 解答

```csharp
using System;

public class Solution
{
    public static int ProcessNumber(int number, Func<int, int> processor)
    {
        return processor(number);
    }
    
    public static int RunComplexProcessing(int number)
    {
        // 使用大括号 { } 创建语句 Lambda（多行 Lambda）
        Func<int, int> complexProcessor = n =>
        {
            // 1. 如果数字为负数，将其转换为正数（绝对值）
            if (n < 0)
            {
                n = -n;
            }
            // 2. 将该数字翻倍
            int doubled = n * 2;
            // 3. 在结果上加 10
            int result = doubled + 10;
            // 4. 返回最终值
            return result;
        };
        
        return ProcessNumber(number, complexProcessor);
    }
}
```
