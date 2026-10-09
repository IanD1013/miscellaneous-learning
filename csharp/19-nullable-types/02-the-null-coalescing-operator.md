### 空值合并运算符

空值合并运算符（`??`）提供了一种在可空表达式为 `null` 时返回默认值的简洁方式。
它比编写针对 null 的 if-else 检查更加清晰整洁。

### 基本用法

```csharp
int? maybeNumber = null;
int result = maybeNumber ?? 10;  // result 为 10

int? hasValue = 42;
int result2 = hasValue ?? 10;    // result2 为 42
```

### 不使用 vs 使用 ??

```csharp
// 不使用 ??（冗长）
int result;
if (number.HasValue)
    result = number.Value;
else
    result = defaultValue;

// 使用 ??（简洁）
int result = number ?? defaultValue;
```

### 链式连接多个默认值

```csharp
int? first = null;
int? second = null;
int? third = 100;

int result = first ?? second ?? third ?? 0;  // result 为 100
```

### 你的任务

实现一个接收可空整数和默认值的方法。
使用空值合并运算符（`??`）在该数字有值时返回该数值，在为 `null` 时返回默认值。

### 方法签名

```csharp
public static int GetValueOrDefault(int? number, int defaultValue)
```

### 预期结果

```
GetValueOrDefault(42, 0) -> 42
GetValueOrDefault(null, 100) -> 100
GetValueOrDefault(-5, 0) -> -5
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetValueOrDefault(int? number, int defaultValue)
    {
        // 有值时返回该数值，为 null 时返回默认值
        return number ?? defaultValue;
    }
}
```
