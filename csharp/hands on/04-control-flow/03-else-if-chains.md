### Else-If 链

当你需要按顺序检查多个条件时，请使用 else-if 链。
只有一个代码块会执行，即第一个计算结果为 `true` 的条件。

### 基本结构

```csharp
if (condition1)
{
    // condition1 为 true 时运行
}
else if (condition2)
{
    // condition1 为 false 并且 condition2 为 true 时运行
}
else if (condition3)
{
    // 上面两个都为 false 并且 condition3 为 true 时运行
}
else
{
    // 上面所有条件都为 false 时运行
}
```

### 顺序至关重要！

条件是从上到下依次检查的。
第一个为 `true` 的条件胜出。

```csharp
int temperature = 85;

// 错误的顺序 - 炎热的日子总是返回 "warm"
if (temperature > 60)
{
    return "warm";  // 85 > 60 为 true，在这里就停止了！
}
else if (temperature > 80)
{
    return "hot";   // 对于 85 永远不会执行到这里
}

// 正确的顺序 - 先检查最严格的条件
if (temperature > 80)
{
    return "hot";   // 85 > 80 为 true
}
else if (temperature > 60)
{
    return "warm";
}
```

### 你的任务

将数字分数（0-100）转换为字母等级：

| 分数范围 | 字母等级 |
| --- | --- |
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| 0-59 | F |

### 方法签名

```csharp
public static string GetLetterGrade(int score)
```

### 预期结果

```
GetLetterGrade(95) -> "A"
GetLetterGrade(82) -> "B"
GetLetterGrade(73) -> "C"
GetLetterGrade(65) -> "D"
GetLetterGrade(45) -> "F"
```

### 解答

```csharp
using System;

public class Solution
{
    public static string GetLetterGrade(int score)
    {
        // 从最高的分数段开始检查，第一个满足的条件胜出
        if (score >= 90)
        {
            return "A";
        }
        else if (score >= 80)
        {
            return "B";
        }
        else if (score >= 70)
        {
            return "C";
        }
        else if (score >= 60)
        {
            return "D";
        }
        else
        {
            return "F";
        }
    }
}
```
