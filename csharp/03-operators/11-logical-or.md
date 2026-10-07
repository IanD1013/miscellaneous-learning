### 逻辑或运算符

逻辑或运算符（`||`）在它的操作数中**至少有一个**为 true 时返回 `true`。
当你需要检查多个条件中是否有任意一个满足时，就可以使用它。

### 基本用法

```csharp
bool result1 = true || false;   // true（第一个为 true）
bool result2 = false || true;   // true（第二个为 true）
bool result3 = false || false;  // false（都不为 true）
bool result4 = true || true;    // true（两个都为 true）
```

### OR 与 AND

| 运算符 | 符号 | 何时返回 true |
| --- | --- | --- |
| AND | `&&` | 两个操作数都为 true |
| OR | `\|\|` | 至少一个操作数为 true |

```csharp
// AND - 两个都必须为 true
bool canDrive = hasLicense && hasCar;  // 需要两个都满足

// OR - 任意一个为 true 即可
bool canEnter = isAdult || hasParentConsent;  // 至少需要满足一个
```

### 短路求值

或运算符采用短路求值：如果第一个操作数为 `true`，则**不会计算**第二个操作数，因为结果已知为 `true`。

```csharp
bool result = true || SomeExpensiveCheck();  // SomeExpensiveCheck() 永远不会执行！
```

### 你的任务

实现一个方法，用于检查某人是否可以访问受限内容。
满足以下任一条件即可访问：

- 年龄在 18 岁或以上，**或者**
- 拥有明确的许可（无论年龄大小）

如果满足**任一**条件，则返回 `true`，否则返回 `false`。

### 方法签名

```csharp
public static bool CheckCondition(int age, bool hasPermission)
```

### 预期结果

```
CheckCondition(20, false) -> True   // 成年人，不需要许可
CheckCondition(15, true) -> True    // 未成年但有许可
CheckCondition(15, false) -> False  // 未成年且没有许可
CheckCondition(18, false) -> True   // 正好 18 岁，不需要许可
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool CheckCondition(int age, bool hasPermission)
    {
        // 年满 18 岁或者拥有许可，满足任一条件即返回 true
        return age >= 18 || hasPermission;
    }
}
```
