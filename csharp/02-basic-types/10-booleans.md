### 布尔值（Booleans）

`bool`（Boolean 的缩写）表示一个逻辑值，只能是 `true` 或 `false`。
布尔值对于在代码中做出决策至关重要。

### 声明与赋值

```csharp
bool isActive = true;
bool isComplete = false;
bool hasPermission = true;
```

### 使用逻辑运算符组合布尔值

| 运算符 | 名称 | 说明 | 示例 |
| --- | --- | --- | --- |
| `&&` | AND | 两者都必须为 true | `true && true` → `true` |
| `\|\|` | OR | 至少有一个必须为 true | `true \|\| false` → `true` |
| `!` | NOT | 反转值 | `!true` → `false` |

```csharp
bool canDrive = hasLicense && isAdult;    // 两个条件都必须为 true
bool canEnter = isVIP || hasPaid;          // 任一条件为 true 即可
bool isLocked = !isOpen;                   // 与 isOpen 相反
```

### 真值表

理解逻辑运算符在不同组合下的工作方式：

**AND (`&&`)** - 两者都必须为 true：

| A | B | A && B |
| --- | --- | --- |
| true | true | true |
| true | false | false |
| false | true | false |
| false | false | false |

**OR (`||`)** - 至少有一个必须为 true：

| A | B | A \|\| B |
| --- | --- | --- |
| true | true | true |
| true | false | true |
| false | true | true |
| false | false | false |

### 你的任务

创建一个方法来判断一个人是否有资格投票。
如果一个人是**成年人**并且是**公民**，则可以投票。
这两个条件均作为布尔参数提供。

### 方法签名

```csharp
public static bool IsEligibleToVote(bool isAdult, bool isCitizen)
```

### 预期结果

```
IsEligibleToVote(true, true)   -> True   // 成年公民
IsEligibleToVote(false, true)  -> False  // 不是成年人
IsEligibleToVote(true, false)  -> False  // 不是公民
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool IsEligibleToVote(bool isAdult, bool isCitizen)
    {
        // 必须同时是成年人且是公民
        return isAdult && isCitizen;
    }
}
```
