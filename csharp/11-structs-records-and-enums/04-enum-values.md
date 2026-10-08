### 枚举的基础值

C# 中的每个枚举（enum）都有一个基础整数类型（默认为 int），用于存储每个成员的实际数值。

### 访问数值

```csharp
public enum Priority
{
    Low = 1,
    Medium = 2,
    High = 3
}

// 将枚举强制转换为 int 以获取基础值
int value = (int)Priority.High;  // value = 3
```

### 默认值与自定义值

```csharp
// 默认：从 0 开始并依次递增
public enum Color
{
    Red,    // 0
    Green,  // 1
    Blue    // 2
}

// 自定义：由你指定具体的值
public enum HttpStatus
{
    OK = 200,
    NotFound = 404,
    ServerError = 500
}

int status = (int)HttpStatus.NotFound;  // status = 404
```

### 将 Int 转换为 Enum

```csharp
// 你也可以将 int 强制转换回枚举
Priority p = (Priority)2;  // p = Priority.Medium
```

### 你的任务

给定一个 `DayOfWeek` 枚举成员，返回其底层基础整数值。

`DayOfWeek` 枚举的定义是从 Sunday = 0 到 Saturday = 6。

### 方法签名

```csharp
public static int GetEnumValue(DayOfWeek day)
```

### 预期结果

```
GetEnumValue(DayOfWeek.Sunday) -> 0
GetEnumValue(DayOfWeek.Wednesday) -> 3
GetEnumValue(DayOfWeek.Saturday) -> 6
```

### 解答

```csharp
using System;

public enum DayOfWeek
{
    Sunday = 0,
    Monday = 1,
    Tuesday = 2,
    Wednesday = 3,
    Thursday = 4,
    Friday = 5,
    Saturday = 6
}

public class Solution
{
    public static int GetEnumValue(DayOfWeek day)
    {
        // 将枚举强制转换为 int，得到其基础值
        return (int)day;
    }
}
```
