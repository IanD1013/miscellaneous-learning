### 使用 `is` 进行类型检查

`is` 关键字用于在运行时检查对象是否与特定类型兼容。
如果对象属于该类型（或派生类型），它将返回 `true`，否则返回 `false`。

### 基本用法

```csharp
object myValue = "Hello";
bool isString = myValue is string;  // true

object myNumber = 42;
bool isInt = myNumber is int;        // true
bool isDouble = myNumber is double;  // false
```

### 处理 null 值

`is` 关键字可以安全地处理 `null` 值，在检查空引用时它会返回 `false`：

```csharp
object nullValue = null;
bool result = nullValue is string;  // false（不是 string，而是 null）
bool isNull = nullValue is null;    // true（C# 7+）
```

### 为什么使用 `is` 而不是 GetType()？

```csharp
// 使用 is - 更简洁，并且能安全处理 null
if (value is string)
{
    Console.WriteLine("It's a string!");
}

// 使用 GetType() - 遇到 null 会抛出异常，而且更冗长
if (value != null && value.GetType() == typeof(string))
{
    Console.WriteLine("It's a string!");
}
```

### 你的任务

实现一个方法，用于检查给定的 `object` 是否为 `string` 类型。

### 方法签名

```csharp
public static bool IsString(object value)
```

### 预期结果

```
IsString("hello") -> True
IsString(42) -> False
IsString(null) -> False
```

### 解答

```csharp
using System;

public class Solution
{
    public static bool IsString(object value)
    {
        // 使用 is 检查类型，null 会返回 false
        return value is string;
    }
}
```
