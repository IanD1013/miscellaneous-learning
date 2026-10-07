### 逻辑非运算符

逻辑非运算符（`!`）会反转一个布尔值：`true` 变为 `false`，`false` 变为 `true`。
这是在 C# 中表示“该条件的反面”最常用的方式之一，它让你可以将描述*问题*的标志转换为描述*所需状态*的标志。

### 工作原理

`!` 是一个一元运算符，这意味着它直接放在单个布尔值（变量、字面量、返回 `bool` 的方法调用或带括号的表达式）的前面。
它会计算该值并产生反转后的结果。
它**不会**改变原始变量，它只产生一个新值。

```csharp
bool hasErrors = true;
bool succeeded = !hasErrors;   // succeeded 为 false
// hasErrors 仍然为 true - 它没有被修改
```

### 语法

```csharp
!booleanValue          // 对单个值求反
!(expression)          // 对圆括号内的整个表达式求反
```

### 示例

```csharp
// 把“问题”标志转换为“良好”标志
bool isExpired = false;
bool isStillValid = !isExpired;      // true

// 在条件中使用 NOT，而不是与 false 比较
bool isLoggedIn = false;
if (!isLoggedIn)                     // 优于：if (isLoggedIn == false)
{
    Console.WriteLine("Please sign in");
}

// 对方法的结果求反
string name = "";
bool hasName = !string.IsNullOrEmpty(name);   // false
```

### 将 NOT 与 AND / OR 结合

`!` 的优先级高于 `&&` 和 `||`，因此 `!a && b` 表示 `(!a) && b`。
当你想对整个表达式求反时，请使用括号。

```csharp
bool isRaining = true;
bool hasUmbrella = false;

bool stayDry = !isRaining || hasUmbrella;    // (!true) || false  ->  false
bool getsWet = !(!isRaining || hasUmbrella); // !(false)         ->  true

// 两个条件都必须处于“关闭”状态
bool doorLocked = false;
bool alarmOn = false;
bool canWalkIn = !doorLocked && !alarmOn;    // true
```

### 参考速查

| 表达式 | 含义 | 当 `a = true`、`b = false` 时的结果 |
| --- | --- | --- |
| `!a` | 非 a | `false` |
| `!a && !b` | 既非 a 也非 b | `false` |
| `!a \|\| !b` | a 和 b 不都为真 | `true` |
| `!(a && b)` | 非 (a 且 b) | `true` |

### 你的任务

一个日程安排应用程序为每个团队成员跟踪两个标志：`isBusy`（他们目前正在开会）和 `isOnVacation`（他们正在休假）。
编写 `IsAvailable`，仅当该成员既不忙碌也没有休假时返回 `true`，在所有其他情况下返回 `false`。

使用带有 `!` 运算符的布尔表达式来解决它，不需要使用 `if` 语句。

### 方法签名

```csharp
public static bool IsAvailable(bool isBusy, bool isOnVacation)
```

### 预期结果

```
IsAvailable(false, false) -> True
IsAvailable(true, false)  -> False
IsAvailable(false, true)  -> False
IsAvailable(true, true)   -> False
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool IsAvailable(bool isBusy, bool isOnVacation)
    {
        // 既不忙碌也没有休假时才可用
        return !isBusy && !isOnVacation;
    }
}
```
