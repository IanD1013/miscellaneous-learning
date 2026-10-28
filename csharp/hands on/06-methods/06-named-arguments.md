### 命名参数

命名参数允许你通过使用参数名称来指定哪个参数接收哪个值，从而使你能够以任意顺序传递参数。

### 基本语法

```csharp
// 方法定义
void Greet(string name, int times, bool loud)
{
    // 具体实现
}

// 普通的按位置调用 - 顺序很重要
Greet("Sam", 3, true);

// 命名参数 - 顺序无关紧要！
Greet(times: 3, loud: true, name: "Sam");
Greet(name: "Sam", loud: true, times: 3);
```

### 混合使用位置参数和命名参数

```csharp
// 位置参数必须放在命名参数之前
Greet("Sam", times: 3, loud: true);  // 有效 - "Sam" 是位置参数
Greet("Sam", 3, loud: true);          // 有效 - 只有最后一个是命名参数

// 这是无效的 - 位置参数放在了命名参数之后
// Greet(name: "Sam", 3, true);  // 无法编译！
```

### 为什么使用命名参数？

| 优势 | 示例 |
| --- | --- |
| 清晰性 | `Draw(x: 10, y: 20)` vs `Draw(10, 20)` |
| 灵活性 | 无需考虑参数顺序 |
| 可读性 | `SetAlarm(hour: 7, minute: 30, enabled: true)` |
| 选择性命名 | 仅命名容易混淆的参数 |

### 你的任务

根据提供的场景编号，使用命名参数和位置参数的不同组合调用 `CreateProfile` 方法。
对于除 1-4 以外的任何场景，返回 `"Invalid scenario"`。

### 方法签名

```csharp
public static string CallWithNamedArguments(int scenario)
```

### 预期结果

```
CallWithNamedArguments(1) -> "Alice, 25, Paris, True"（全部命名，倒序）
CallWithNamedArguments(2) -> "Bob, 30, London, False"（city 在前）
CallWithNamedArguments(3) -> "Carol, 22, Tokyo, True"（混合）
CallWithNamedArguments(4) -> "David, 40, Berlin, False"（大部分按位置）
CallWithNamedArguments(99) -> "Invalid scenario"（任何不在 1-4 内的值）
```

### 解答

```csharp
using System;

public class Solution
{
    // 不要修改此方法 - 它用于测试你的命名参数调用
    public static string CreateProfile(string name, int age, string city, bool isActive)
    {
        return $"{name}, {age}, {city}, {isActive}";
    }
    
    public static string CallWithNamedArguments(int scenario)
    {
        if (scenario == 1)
        {
            // 场景 1：按倒序传入全部命名参数（isActive, city, age, name）
            return CreateProfile(isActive: true, city: "Paris", age: 25, name: "Alice");
        }
        else if (scenario == 2)
        {
            // 场景 2：city 在前，然后是 name、age、isActive
            return CreateProfile(city: "London", name: "Bob", age: 30, isActive: false);
        }
        else if (scenario == 3)
        {
            // 场景 3：前两个按位置（name, age），后两个使用命名参数
            return CreateProfile("Carol", 22, city: "Tokyo", isActive: true);
        }
        else if (scenario == 4)
        {
            // 场景 4：只有 isActive 使用命名参数，其余按位置
            return CreateProfile("David", 40, "Berlin", isActive: false);
        }
        else
        {
            // 其他任何场景
            return "Invalid scenario";
        }
    }
}
```
