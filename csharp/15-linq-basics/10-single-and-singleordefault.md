### Single 和 SingleOrDefault

`Single()` 和 `SingleOrDefault()` 用于从集合中检索恰好一个元素。
与 `First()` 不同，这些方法**期望只有唯一个匹配项**，如果多个元素满足条件，则会抛出异常。

### Single() 方法

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 返回唯一满足条件的元素
var three = numbers.Single(n => n == 3);  // 返回 3

// 如果没有匹配项，抛出 InvalidOperationException
var ten = numbers.Single(n => n == 10);  // 异常！

// 如果有多个匹配项，抛出 InvalidOperationException
var evens = numbers.Single(n => n % 2 == 0);  // 异常！（2 和 4 都匹配）
```

### SingleOrDefault() 方法

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

// 如果没有匹配项，返回默认值（引用类型为 null，int 为 0）
var ten = numbers.SingleOrDefault(n => n == 10);  // 返回 0

var names = new List<string> { "Alice", "Bob" };
var missing = names.SingleOrDefault(n => n == "Charlie");  // 返回 null

// 如果有多个匹配项，仍然会抛出异常！
var evens = numbers.SingleOrDefault(n => n % 2 == 0);  // 异常！
```

### Single 与 First - 何时使用哪一个

| 场景 | 使用 | 原因 |
| --- | --- | --- |
| 通过唯一 ID/键查找 | `SingleOrDefault()` | 强化唯一性假设 |
| 获取任意匹配项 | `FirstOrDefault()` | 允许多个匹配项 |
| 数据必须恰好存在一次 | `Single()` | 如果数据无效则快速失败 |

### 关键区别总结

| 方法 | 无匹配项 | 一个匹配项 | 多个匹配项 |
| --- | --- | --- | --- |
| `Single()` | 异常 | 返回元素 | 异常 |
| `SingleOrDefault()` | 返回默认值 | 返回元素 | 异常 |
| `First()` | 异常 | 返回元素 | 返回第一个 |
| `FirstOrDefault()` | 返回默认值 | 返回元素 | 返回第一个 |

### 你的任务

实现一个方法，通过电子邮件地址查找用户。
由于在用户系统中电子邮件应该是唯一的，因此使用 `SingleOrDefault()` 来强制执行此约束。
如果找到该用户则返回用户名，如果没有用户的电子邮件与该地址匹配，则返回 `"Not Found"`。

### 方法签名

```csharp
public static string FindUserByEmail(List<User> users, string email)
```

`User` 类可在 User.cs 中使用，包含 `Username` 和 `Email` 属性。

### 预期结果

```
FindUserByEmail([{"alice", "alice@test.com"}, {"bob", "bob@test.com"}], "alice@test.com") -> "alice"
FindUserByEmail([{"alice", "alice@test.com"}], "unknown@test.com") -> "Not Found"
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static string FindUserByEmail(List<User> users, string email)
    {
        // 返回具有给定电子邮件的用户的用户名
        // 如果没有用户使用该电子邮件，则返回 "Not Found"
        // 电子邮件应该是唯一的，因此使用合适的 LINQ 方法
        User user = users.SingleOrDefault(u => u.Email == email);

        if (user == null)
        {
            return "Not Found";
        }

        return user.Username;
    }
}
```
