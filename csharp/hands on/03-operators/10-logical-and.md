### 逻辑与运算符（&&）

逻辑与运算符（`&&`）组合两个布尔条件，并且仅在**两个**条件都为 true 时才返回 `true`。

### 基本用法

```csharp
bool result1 = true && true;   // True - 两个都为 true
bool result2 = true && false;  // False - 第二个为 false
bool result3 = false && true;  // False - 第一个为 false
bool result4 = false && false; // False - 两个都为 false
```

### 结合比较运算符

`&&` 运算符通常与比较运算符一起使用，以检查多个条件：

```csharp
int age = 25;
bool hasLicense = true;

// 两个条件都必须为 true
bool canDrive = age >= 18 && hasLicense;  // True

int temperature = 72;
bool isComfortable = temperature >= 65 && temperature <= 80;  // True
```

### 短路求值

C# 使用短路求值：如果第一个条件为 `false`，则不会计算第二个条件（因为结果必定为 `false`）：

```csharp
bool a = false && SomeExpensiveMethod();  // SomeExpensiveMethod() 永远不会执行
```

### 真值表

| 条件 A | 条件 B | A && B |
| --- | --- | --- |
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

### 你的任务

编写一个方法来判断一个人是否可以进入游乐园。
一个人可以进入的条件是：

1. 年龄至少为 5 岁（age >= 5），**并且**
2. 持有门票（hasTicket 为 true）

两个条件必须同时满足才允许进入。

### 方法签名

```csharp
public static bool CanEnterPark(int age, bool hasTicket)
```

### 预期结果

```
CanEnterPark(10, true) -> True
CanEnterPark(10, false) -> False
CanEnterPark(3, true) -> False
CanEnterPark(5, true) -> True
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool CanEnterPark(int age, bool hasTicket)
    {
        // 年龄至少 5 岁并且持有门票，两个条件都满足才返回 true
        return age >= 5 && hasTicket;
    }
}
```
