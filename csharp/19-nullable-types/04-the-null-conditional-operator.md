### Null 条件运算符

Null 条件运算符（`?.`）允许你安全地访问可能为 `null` 的对象的成员，短路求值并返回 `null`，而不是抛出 `NullReferenceException`。

### 基本用法

```csharp
Person? person = null;

// 不使用 null 条件运算符（抛出 NullReferenceException）
int length = person.Name.Length; // 崩溃！

// 使用 null 条件运算符（安全地返回 null）
int? length = person?.Name?.Length; // 返回 null，不会崩溃
```

### 链式使用 Null 条件运算符

你可以将多个 `?.` 运算符串联起来，安全地访问嵌套属性：

```csharp
// 如果 person 为 null，返回 null
// 如果 person.Name 为 null，返回 null
// 否则，返回长度
int? result = person?.Name?.Length;
```

### 与 Null 合并运算符结合使用

将 `?.` 与 `??` 结合使用，可以在链式调用结果为 `null` 时提供一个默认值：

```csharp
int length = person?.Name?.Length ?? 0;
// 如果 person 为 null 或 Name 为 null，返回 0
// 否则返回实际长度
```

### 你的任务

实现一个安全返回人员姓名长度的方法。
`Person` 对象可能为 `null`，即使它存在，其 `Name` 属性也可能为 `null`。

如果 person 或其 name 为 `null`，则返回 `0`。

### 方法签名

```csharp
public static int GetNameLength(Person? person)
```

### 预期结果

```
GetNameLength(new Person { Name = "Alice" }) -> 5
GetNameLength(new Person { Name = null }) -> 0
GetNameLength(null) -> 0
```

### 解答

```csharp
using System;

public class Person
{
    public string? Name { get; set; }
    public int Age { get; set; }
}

public class Solution
{
    public static int GetNameLength(Person? person)
    {
        // person 或 Name 为 null 时返回 0，否则返回姓名长度
        return person?.Name?.Length ?? 0;
    }
}
```
