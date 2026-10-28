### StringBuilder

StringBuilder 是一个可变字符串类，它可以通过多次修改高效地构建字符串，从而避免了每次字符串拼接时创建新字符串对象的性能开销。

### 为什么使用 StringBuilder？

C# 中的字符串是不可变（immutable）的，每次修改都会创建一个新的字符串对象。
在循环中构建字符串时，这会产生许多临时对象：

```csharp
// 低效 - 创建许多字符串对象
string result = "";
for (int i = 0; i < 1000; i++)
{
    result += i.ToString(); // 每次迭代都会产生新字符串！
}

// 高效 - 只有一个 StringBuilder 对象
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    sb.Append(i);
}
string result = sb.ToString();
```

### Append 与 AppendLine

```csharp
StringBuilder sb = new StringBuilder();

sb.Append("Hello");      // 添加文本，不换行
sb.Append(" World");     // 结果："Hello World"

sb.AppendLine("Line 1"); // 添加文本 + 换行符
sb.AppendLine("Line 2"); // 结果："Line 1\nLine 2\n"

sb.Append("Item: ");
sb.AppendLine("Apple");  // 结果："Item: Apple\n"
```

### 常用方法

| 方法 | 说明 | 示例 |
| --- | --- | --- |
| `Append(value)` | 向末尾添加文本 | `sb.Append("text")` |
| `AppendLine(value)` | 添加文本和换行符 | `sb.AppendLine("line")` |
| `AppendLine()` | 仅添加换行符 | `sb.AppendLine()` |
| `ToString()` | 转换为字符串 | `sb.ToString()` |
| `Clear()` | 清空 builder | `sb.Clear()` |

### 你的任务

创建一个使用 StringBuilder 构建格式化报告的方法。
该报告应包含：

1. 第一行的标题
2. 一行破折号（长度与标题相同）
3. 带有编号的项目，每个项目各占一行

使用 `Append()` 构建每个带编号的行，并使用 `AppendLine()` 添加换行。
返回末尾不带多余换行符的最终字符串。

### 方法签名

```csharp
public static string BuildReport(string title, string[] items)
```

### 预期结果

```
BuildReport("Tasks", ["Code", "Test"]) -> "Tasks\n-----\n1. Code\n2. Test"
BuildReport("Shopping List", ["Milk"]) -> "Shopping List\n-------------\n1. Milk"
```

### 解答

```csharp
using System;
using System.Text;

public class Solution
{
    public static string BuildReport(string title, string[] items)
    {
        StringBuilder sb = new StringBuilder();
        
        // 标题和与标题等长的破折号行
        sb.Append(title);
        sb.AppendLine();
        sb.Append(new string('-', title.Length));
        
        // 每个编号项目前先换行，这样末尾不会有多余的换行符
        for (int i = 0; i < items.Length; i++)
        {
            sb.AppendLine();
            sb.Append($"{i + 1}. {items[i]}");
        }
        
        return sb.ToString();
    }
}
```
