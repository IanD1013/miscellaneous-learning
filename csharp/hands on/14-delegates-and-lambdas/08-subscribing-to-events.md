### 订阅事件

订阅事件意味着注册一个处理程序方法，该方法将在触发事件时被调用。
使用 `+=` 运算符来添加事件处理程序。

### += 运算符

```csharp
// 使用具名方法订阅
button.Click += HandleClick;

// 使用 lambda 表达式订阅
button.Click += (sender) => Console.WriteLine("Clicked!");

// 使用匿名方法订阅
button.Click += delegate(object sender) { Console.WriteLine("Clicked!"); };
```

### 多个订阅者

事件可以拥有多个处理程序，当事件触发时它们都会执行：

```csharp
timer.Elapsed += LogToConsole;
timer.Elapsed += LogToFile;
timer.Elapsed += UpdateUI;
// Elapsed 触发时，这三个方法都会运行
```

### 使用 -= 取消订阅

当你不再需要接收通知时，使用 `-=` 移除处理程序：

```csharp
button.Click -= HandleClick;  // 停止监听
```

### 你的任务

一个 `OrderProcessor` 类具有两个事件：`OrderReceived` 和 `OrderCompleted`。
请为这两个事件订阅处理程序，以便在处理订单时打印消息。

### 所需输出格式

- 当 `OrderReceived` 触发时：`Order received: {orderName}`
- 当 `OrderCompleted` 触发时：`Order completed: {orderName}`

### 预期结果

```
RunOrderSystem(["Pizza"]) ->
Order received: Pizza
Order completed: Pizza

RunOrderSystem(["Book", "Phone"]) ->
Order received: Book
Order completed: Book
Order received: Phone
Order completed: Phone
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public delegate void OrderHandler(string orderName);

public class OrderProcessor
{
    public event OrderHandler OrderReceived;
    public event OrderHandler OrderCompleted;
    
    public void ProcessOrder(string orderName)
    {
        OrderReceived?.Invoke(orderName);
        // 模拟处理过程
        OrderCompleted?.Invoke(orderName);
    }
}

public class Solution
{
    public static void RunOrderSystem(string[] orderNames)
    {
        OrderProcessor processor = new OrderProcessor();
        
        // 订阅 OrderReceived 事件
        processor.OrderReceived += orderName => Console.WriteLine($"Order received: {orderName}");
        
        // 订阅 OrderCompleted 事件
        processor.OrderCompleted += orderName => Console.WriteLine($"Order completed: {orderName}");
        
        // 处理每个订单
        foreach (string order in orderNames)
        {
            processor.ProcessOrder(order);
        }
    }
}
```
