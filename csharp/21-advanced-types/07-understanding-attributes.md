### C# 中的特性（Attributes）

特性为你的代码添加元数据，即编译器、运行时或其他工具可以在不改变代码执行方式的情况下使用的额外信息。

### 什么是特性？

特性放置在类、方法、属性或参数等声明上方的方括号 `[]` 中。

```csharp
[AttributeName]
public void MyMethod() { }

[AttributeName("parameter")]
public class MyClass { }
```

### [Obsolete] 特性

将代码标记为已弃用。
当使用已弃用的代码时，编译器会生成一条警告。

```csharp
[Obsolete]
public void OldMethod() { }  // 警告：'OldMethod' 已过时

[Obsolete("Use NewMethod instead.")]
public void OldMethod() { }  // 警告中包含你的消息

[Obsolete("Removed in v2.0", true)]  // 第二个参数 = 报错而不是警告
public void OldMethod() { }
```

### 其他常用内置特性

| 特性 | 用途 | 示例 |
| --- | --- | --- |
| `[Obsolete]` | 标记已弃用的代码 | `[Obsolete("Use X instead")]` |
| `[Serializable]` | 允许对象序列化 | `[Serializable] class Data` |
| `[Conditional]` | 仅在定义了指定符号时编译方法 | `[Conditional("DEBUG")]` |
| `[Flags]` | 启用按位枚举操作 | `[Flags] enum Permissions` |

### 你的任务

1. 为 `OldCalculation` 方法添加 `[Obsolete]` 特性
2. 包含自定义消息：`"Use NewCalculation instead. This method will be removed in version 2.0."`
3. 在 `GetObsoleteMessage` 中，调用 `OldCalculation(5, 3)` 并返回其结果

### 方法签名

```csharp
[Obsolete("message")]
public static string OldCalculation(int x, int y)

public static string GetObsoleteMessage()
```

### 预期结果

```
GetObsoleteMessage() -> "Result: 8"
```

注意：你会看到一条关于使用已弃用代码的编译器警告，这是预期的！
代码仍会正常运行，但该警告会提醒开发者更新其代码。

### 解答

```csharp
using System;

public class Solution
{
    // 为该方法添加带自定义消息的 [Obsolete] 特性
    [Obsolete("Use NewCalculation instead. This method will be removed in version 2.0.")]
    public static string OldCalculation(int x, int y)
    {
        return $"Result: {x + y}";
    }
    
    public static string GetObsoleteMessage()
    {
        // 调用已弃用的方法并返回其结果
        // 编译器会显示警告，但代码仍然可以运行！
        return OldCalculation(5, 3);
    }
}
```
