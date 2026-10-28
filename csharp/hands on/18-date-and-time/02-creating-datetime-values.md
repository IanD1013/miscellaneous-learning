### 创建 DateTime 值

`DateTime` 结构提供了多个构造函数来创建特定的日期和时间。
你可以仅指定日期，也可以包含时间部分以表示精确的时刻。

### 仅日期构造函数

```csharp
// DateTime(year, month, day)
DateTime christmas = new DateTime(2024, 12, 25);
// 创建：2024 年 12 月 25 日 12:00:00 AM（午夜）
```

### 日期和时间构造函数

```csharp
// DateTime(year, month, day, hour, minute, second)
DateTime newYear = new DateTime(2025, 1, 1, 0, 0, 0);
// 创建：2025 年 1 月 1 日 12:00:00 AM

DateTime lunch = new DateTime(2024, 6, 15, 12, 30, 0);
// 创建：2024 年 6 月 15 日 12:30:00 PM
```

### 构造函数参数

| 参数 | 范围 | 说明 |
| --- | --- | --- |
| year | 1-9999 | 年份 |
| month | 1-12 | 月份（1 = 一月） |
| day | 1-31 | 月份中的日期 |
| hour | 0-23 | 小时（24小时制） |
| minute | 0-59 | 分钟 |
| second | 0-59 | 秒 |

### 24小时制时间格式

hour 参数采用 24 小时制：

- `0` = 12:00 AM（午夜）
- `12` = 12:00 PM（中午）
- `14` = 2:00 PM
- `23` = 11:00 PM

### 你的任务

创建一个表示 **1990年7月4日 2:30:00 PM** 的 `DateTime` 并将其打印到控制台。

### 方法签名

```csharp
public static void PrintBirthday()
```

### 预期输出

```
7/4/1990 2:30:00 PM
```

### 解答

```csharp
using System;

public class Solution
{
    public static void PrintBirthday()
    {
        // 创建表示 1990 年 7 月 4 日 2:30:00 PM 的 DateTime
        DateTime birthday = new DateTime(1990, 7, 4, 14, 30, 0);

        // 然后使用 Console.WriteLine() 打印它
        Console.WriteLine(birthday);
    }
}
```
