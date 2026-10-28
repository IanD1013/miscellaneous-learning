### 静态字段 (Static Fields)

静态字段属于类本身，而不是属于任何特定的实例。
所有实例共享同一个静态字段值，这使得它非常适合用于跟踪整个类级别的信息。

### 实例字段 vs 静态字段

```csharp
public class Counter
{
    public int InstanceValue = 0;      // 每个对象都有自己的副本
    public static int SharedValue = 0; // 所有对象共享这一个值
}

var a = new Counter();
var b = new Counter();

a.InstanceValue = 5;      // 只影响 'a'
Counter.SharedValue = 10; // 影响整个类
```

### 访问静态字段

```csharp
// 通过类名访问（推荐）
int count = Counter.SharedValue;

// 或者通过静态方法访问
int count = Counter.GetSharedValue();
```

### 常见用例

| 用例 | 示例 |
| --- | --- |
| 实例计数 | 跟踪创建了多少个对象 |
| 共享配置 | 所有实例的默认设置 |
| 缓存 | 仅存储一次计算出的值 |
| 常量 | `public static readonly double Pi = 3.14159;` |

### 你的任务

Player.cs 中的 `Player` 类已经设置了一个用于跟踪实例计数的 **private** 静态字段。
它提供了 `GetCount()` 和 `ResetCount()` 静态方法来访问和重置该计数器。

完成 Main.cs 以实现：

1. `GetInstanceCount()` - 创建 3 个玩家（Alice、Bob、Charlie）并返回计数
2. `CreatePlayers(int count)` - 创建指定数量的玩家并返回计数

### 方法签名

```csharp
public static int GetInstanceCount()       // 创建 3 个玩家，返回计数
public static int CreatePlayers(int count) // 创建 'count' 个玩家，返回计数
```

### Player 类 API（位于 Player.cs）

```csharp
new Player(string name)      // 构造函数 - 递增内部计数器
Player.GetCount()            // 返回当前实例计数
Player.ResetCount()          // 将计数器重置为 0
```

### 预期结果

```
GetInstanceCount() -> 3
CreatePlayers(0) -> 0
CreatePlayers(5) -> 5
```

### 解答

```csharp
using System;

public class Solution
{
    public static int GetInstanceCount()
    {
        // 测试前先重置计数器
        Player.ResetCount();
        
        // 创建 3 个 Player 实例（Alice、Bob、Charlie）并返回计数
        new Player("Alice");
        new Player("Bob");
        new Player("Charlie");
        
        return Player.GetCount();
    }
    
    public static int CreatePlayers(int count)
    {
        // 测试前先重置计数器
        Player.ResetCount();
        
        // 创建 count 个 Player 实例并返回计数
        for (int i = 0; i < count; i++)
        {
            new Player($"Player{i + 1}");
        }
        
        return Player.GetCount();
    }
}
```
