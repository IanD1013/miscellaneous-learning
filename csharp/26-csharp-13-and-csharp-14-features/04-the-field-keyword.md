### C# 14 中的 `field` 关键字

`field` 关键字允许在属性访问器内直接访问该属性自动生成的支持字段（backing field），从而无需声明显式的支持字段。

### 传统方法与 `field` 关键字对比

```csharp
// 传统方式：需要显式的支持字段
private string _name;
public string Name
{
    get => _name;
    set
    {
        if (string.IsNullOrEmpty(value))
            throw new ArgumentException("Name required");
        _name = value;
    }
}

// C# 14：使用 field 关键字
public string Name
{
    get => field;
    set
    {
        if (string.IsNullOrEmpty(value))
            throw new ArgumentException("Name required");
        field = value;
    }
}
```

### `field` 的优势

| 优势 | 描述 |
| --- | --- |
| 减少样板代码 | 无需手动声明支持字段 |
| 命名一致性 | 不再混淆 `_name` 与 `name` |
| 代码更整洁 | 属性逻辑保持自包含 |
| 重构更安全 | 编译器负责管理支持字段 |

### 验证模式

```csharp
public int Age
{
    get => field;
    set
    {
        if (value < 0 || value > 150)
            throw new ArgumentOutOfRangeException();
        field = value;
    }
}
```

### 你的任务

重构 `EmailValidator` 类，使用 `field` 关键字替代显式的支持字段。
`Email` 属性应当：

1. 在 getter 和 setter 中均使用 `field`
2. 在设置前验证 email 是否包含 '@'
3. 针对无效的 email 抛出带有消息 "Invalid email format" 的 `ArgumentException`
4. 同时将 null 或空字符串视为无效并拒绝

### 方法签名

```csharp
public static string ValidateAndGetEmail(string email)
```

### 预期结果

```
ValidateAndGetEmail("user@example.com") -> "user@example.com"
ValidateAndGetEmail("test@domain.org") -> "test@domain.org"
ValidateAndGetEmail("invalid") -> throws ArgumentException
```

### 解答

```csharp
using System;

public class EmailValidator
{
    public string Email
    {
        // 使用 field 关键字访问编译器生成的支持字段
        get => field;
        set
        {
            // null、空字符串或不含 '@' 的 email 都视为无效
            if (string.IsNullOrEmpty(value) || !value.Contains('@'))
                throw new ArgumentException("Invalid email format");
            field = value;
        }
    }
}

public class Solution
{
    public static string ValidateAndGetEmail(string email)
    {
        var validator = new EmailValidator();
        validator.Email = email;
        return validator.Email;
    }
}
```
