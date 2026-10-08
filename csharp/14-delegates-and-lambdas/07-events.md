### C# 中的事件（Events）

事件为类提供了一种在发生某些值得关注的情况时通知其他类的方式。
它们遵循发布者-订阅者（publisher-subscriber）模式，其中一个类发布事件，其他类订阅以接收通知。

### `event` 关键字

`event` 关键字用于基于委托类型声明事件。
事件只能在其声明所在的类内部触发。

```csharp
// 使用委托类型声明事件
public event EventHandler MyEvent;

// 使用 EventHandler<T> 声明带自定义数据的事件
public event EventHandler<string> MessageReceived;
```

### EventHandler 委托

`EventHandler` 是 .NET 中用于事件的标准委托类型。
`EventHandler<T>` 允许你在事件中传递自定义数据。

```csharp
// EventHandler 签名：void EventHandler(object sender, EventArgs e)
// EventHandler<T> 签名：void EventHandler<T>(object sender, T e)

public class Button
{
    public event EventHandler Clicked;
    
    public void OnClick()
    {
        // 使用 ?. 安全调用（没有订阅者时处理 null）
        Clicked?.Invoke(this, EventArgs.Empty);
    }
}
```

### 订阅事件

使用 `+=` 订阅事件，使用 `-=` 取消订阅事件。

```csharp
var button = new Button();

// 使用 lambda 订阅
button.Clicked += (sender, e) => Console.WriteLine("Button was clicked!");

// 或者使用方法订阅
button.Clicked += HandleClick;

void HandleClick(object sender, EventArgs e)
{
    Console.WriteLine("Handling click!");
}
```

### 你的任务

创建一个 `TemperatureMonitor` 类，其中包含一个在温度达到临界值（>= 100 度）时触发的事件。

1. 使用 `EventHandler<int>` 声明一个 `TemperatureAlert` 事件
2. 在 `CheckTemperature()` 中，如果温度 >= 100 则触发该事件
3. 在 `RunTemperatureMonitor()` 中，订阅该事件并打印警报消息

### 期望输出格式

```
ALERT: Temperature is {temperature} degrees!
```

### 示例

对于温度 `[85, 100, 95, 110]`：

```
ALERT: Temperature is 100 degrees!
ALERT: Temperature is 110 degrees!
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class TemperatureMonitor
{
    // 使用 EventHandler<int> 声明名为 TemperatureAlert 的事件
    public event EventHandler<int> TemperatureAlert;
    
    public void CheckTemperature(int temperature)
    {
        // 如果温度 >= 100，触发 TemperatureAlert 事件
        // 将温度值作为事件参数传递
        if (temperature >= 100)
        {
            TemperatureAlert?.Invoke(this, temperature);
        }
    }
}

public class Solution
{
    public static void RunTemperatureMonitor(int[] temperatures)
    {
        var monitor = new TemperatureMonitor();
        
        // 订阅 TemperatureAlert 事件，触发时打印警报消息
        monitor.TemperatureAlert += (sender, temperature) =>
            Console.WriteLine($"ALERT: Temperature is {temperature} degrees!");
        
        foreach (int temp in temperatures)
        {
            monitor.CheckTemperature(temp);
        }
    }
}
```
