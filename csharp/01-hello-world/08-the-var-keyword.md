### var 关键字

`var` 关键字允许编译器根据你赋给变量的值来推断变量的类型。
该变量仍然是强类型的，但你无需自己编写类型名称。

### 基本用法

```csharp
// 不必这样写：
int number = 42;
int doubled = number * 2;

// 你可以这样写：
var number = 42;      // 编译器知道这是一个 int
var doubled = number * 2;   // 编译器知道这也是一个 int
```

### var 与显式类型对比

| 显式类型 | 使用 var | 编译器识别的类型 |
| --- | --- | --- |
| `int x = 5;` | `var x = 5;` | int |
| `int y = x + 3;` | `var y = x + 3;` | int |
| `int z = x * 2;` | `var z = x * 2;` | int |

### 重要规则

```csharp
// var 必须有一个值 - 编译器需要它来确定类型
var x = 10;    // 有效
// var y;       // 错误：不能在没有值的情况下使用 var

// 类型一旦确定就不能改变
var count = 5;
count = 10;    // 有效 - 仍然是 int
// count = 3.14;  // 错误：count 是 int，不是 double
```

### 你的任务

实现一个使用 `var` 关键字将数值翻倍的方法。

接收一个 `int value`，使用 `var` 存储该值乘以 2 的结果，并返回该结果。

### 方法签名

```csharp
public static int DoubleValue(int value)
```

### 预期结果

```
DoubleValue(6) -> 12
DoubleValue(9) -> 18
DoubleValue(0) -> 0
DoubleValue(-7) -> -14
```

### 解答

```csharp
using System;

public class Solution
{
    public static int DoubleValue(int value)
    {
        // 使用 var 存储该值乘以 2 的结果
        var result = value * 2;
        // 返回结果
        return result;
    }
}
```
