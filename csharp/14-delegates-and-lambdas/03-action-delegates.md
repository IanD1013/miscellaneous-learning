### Action 委托

`Action` 是一个内置的委托类型，用于返回 `void` 的方法。
你可以直接使用 `Action`，而无需自定义委托。

### Action 与自定义委托

```csharp
// 自定义委托（我们之前的做法）
public delegate void PrintMessage(string msg);

// 内置的 Action（效果相同，无需定义！）
Action<string> print;
```

### Action 变体

```csharp
// 无参数
Action doSomething = () => Console.WriteLine("Done");

// 一个参数
Action<string> greet = name => Console.WriteLine($"Hello, {name}");

// 多个参数（最多 16 个！）
Action<string, int> repeat = (msg, times) => {
    for (int i = 0; i < times; i++)
        Console.WriteLine(msg);
};
```

### 将 Action 作为参数使用

```csharp
public static void ProcessItems(string[] items, Action<string> processor)
{
    foreach (var item in items)
    {
        processor(item);  // 调用 Action
    }
}

// 用法
ProcessItems(names, name => Console.WriteLine(name.ToUpper()));
```

### 你的任务

实现 `ExecuteActions`，它接收一个消息数组和一个 `Action<string, List<string>>` 委托。
对于每条消息，调用该 action 来记录它。
返回由换行符连接的所有已记录消息。

起始代码中包含了与 `Action<string, List<string>>` 签名匹配的辅助方法 `LogMessage` 和 `LogWithTimestamp`。

### 方法签名

```csharp
public static string ExecuteActions(string[] messages, Action<string, List<string>> logger)
```

### 预期结果

```
ExecuteActions(["Hello"], LogMessage) -> "[LOG] Hello"
ExecuteActions(["A", "B"], LogMessage) -> "[LOG] A\n[LOG] B"
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static string ExecuteActions(string[] messages, Action<string, List<string>> logger)
    {
        // 用于存放已记录消息的列表
        List<string> output = new List<string>();
        
        // 对每条消息调用 Action 委托进行记录
        foreach (string message in messages)
        {
            logger(message, output);
        }
        
        // 返回由换行符连接的所有已记录消息
        return string.Join("\n", output);
    }
    
    // 可用作 Action<string, List<string>> 的辅助方法
    public static void LogMessage(string message, List<string> output)
    {
        output.Add($"[LOG] {message}");
    }
    
    // 另一个使用不同格式的辅助方法
    public static void LogWithTimestamp(string message, List<string> output)
    {
        output.Add($"[2024-01-01] {message}");
    }
}
```
