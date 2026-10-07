### 三元运算符

三元运算符（`?:`）是一种以单个表达式编写简单 if-else 语句的紧凑方式。
当你需要根据条件在两个值之间做出选择时，可以使用它。

### 语法

```csharp
condition ? valueIfTrue : valueIfFalse
```

该运算符会计算条件的值。
如果为 true，则返回第一个值；如果为 false，则返回第二个值。

### 基本示例

```csharp
// 不要这样写：
string result;
if (score >= 50)
    result = "Pass";
else
    result = "Fail";

// 而是这样写：
string result = score >= 50 ? "Pass" : "Fail";

// 更多示例：
int max = a > b ? a : b;
bool isEven = number % 2 == 0 ? true : false;
string greeting = hour < 12 ? "Good morning" : "Good afternoon";
```

### 三元运算符 vs If-Else

| 三元运算符 | If-Else |
| --- | --- |
| 返回一个值 | 执行语句 |
| 单个表达式 | 多行代码 |
| 最适合简单的选择 | 最适合复杂逻辑 |

```csharp
// 三元运算符 - 用于简单赋值时很简洁
string status = isActive ? "Online" : "Offline";

// If-Else - 更适合多个操作
if (isActive)
{
    status = "Online";
    LogActivity();
}
else
{
    status = "Offline";
    SendNotification();
}
```

### 你的任务

编写一个根据年龄对人进行分类的方法。
如果年龄大于或等于 18 岁，则返回 `"Adult"`，否则返回 `"Minor"`。
使用三元运算符以保持解决方案简洁。

### 方法签名

```csharp
public static string GetAgeCategory(int age)
```

### 预期结果

```
GetAgeCategory(21) -> "Adult"
GetAgeCategory(10) -> "Minor"
GetAgeCategory(18) -> "Adult"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetAgeCategory(int age)
    {
        // 年满 18 岁返回 "Adult"，否则返回 "Minor"
        return age >= 18 ? "Adult" : "Minor";
    }
}
```
