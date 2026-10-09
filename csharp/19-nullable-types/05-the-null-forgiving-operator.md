### Null 包容运算符

Null 包容运算符（`!`）用于告诉编译器：“我知道这个值不是 null，相信我。”
当你掌握了编译器不了解的信息时，它可以用来抑制可空警告。

### 何时使用它

```csharp
// 编译器警告：可能的 null 引用
string? name = GetName();
int length = name.Length;  // 警告 CS8602

// 告诉编译器你“知道”它不是 null
int length = name!.Length;  // 无警告
```

### 常见场景

```csharp
// 在你自己做过、但编译器无法识别的 null 检查之后
if (IsValidUser(user))
{
    // 你知道 user.Name 已设置，但编译器不知道
    Console.WriteLine(user.Name!.ToUpper());
}

// 当数据来自可信来源时
string[] args = GetCommandLineArgs();  // 永远不为 null
string firstArg = args[0]!;
```

### 警告：请谨慎使用！

```csharp
// 危险 - 如果你判断错了，就会得到 NullReferenceException
string? maybeNull = null;
int len = maybeNull!.Length;  // 能编译，但在运行时崩溃！
```

### 该运算符不会改变行为

| 代码 | 效果 |
| --- | --- |
| `text!` | 仅抑制警告 |
| `text ?? ""` | 实际提供回退默认值 |
| `text?.Length` | 实际防止崩溃 |

`!` 运算符纯粹是一个编译时提示。
它在运行时不会添加任何 null 检查。

### 你的任务

实现一个返回字符串长度的方法。
该方法接收：

- `text`：一个可空的字符串
- `isGuaranteedNotNull`：一个布尔标志，指示调用方是否保证文本不为 null

当 `isGuaranteedNotNull` 为 `true` 时，使用 null 包容运算符直接访问字符串的长度（信任调用方）。

当 `isGuaranteedNotNull` 为 `false` 时，如果文本为 null 则返回 `-1`，否则返回其长度。

### 方法签名

```csharp
public static int GetStringLength(string? text, bool isGuaranteedNotNull)
```

### 预期结果

```
GetStringLength("hello", true) -> 5
GetStringLength("hello", false) -> 5
GetStringLength(null, false) -> -1
GetStringLength("", true) -> 0
```

### 解答

```csharp
using System;

#nullable enable

public class Solution
{
    public static int GetStringLength(string? text, bool isGuaranteedNotNull)
    {
        // 当 isGuaranteedNotNull 为 true 时，使用 null 包容运算符
        if (isGuaranteedNotNull)
        {
            return text!.Length;
        }

        // 当为 false 时，如果 text 为 null 则返回 -1
        return text?.Length ?? -1;
    }
}
```
