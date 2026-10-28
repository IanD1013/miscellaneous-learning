### 值类型的行为

结构体（struct）是**值类型**，这意味着当您将一个结构体赋值给另一个变量时，会创建一个完全独立的副本。
对副本所做的修改绝不会影响原始对象。

### 按值复制与按引用复制

```csharp
// Struct（值类型）- 复制所有数据
struct Point { public int X; public int Y; }
Point p1 = new Point { X = 10, Y = 20 };
Point p2 = p1;  // p2 是一个完整的副本
p2.X = 99;      // 只有 p2 改变
// p1.X 仍然是 10！

// Class（引用类型）- 复制引用
class Enemy { public int Health; }
Enemy e1 = new Enemy { Health = 100 };
Enemy e2 = e1;  // e2 指向同一个对象
e2.Health = 50; // 两者都能看到这个改变
// e1.Health 现在是 50！
```

### 为什么这很重要

| 场景 | 值类型 (struct) | 引用类型 (class) |
| --- | --- | --- |
| 赋值 | 创建独立的副本 | 共享同一个对象 |
| 修改 | 仅影响该副本 | 影响所有引用 |
| 方法参数 | 接收副本 | 接收引用 |
| 内存 | 栈（通常） | 堆 |

### 常见误区

```csharp
struct Counter { public int Value; }
Counter c1 = new Counter { Value = 5 };
Counter c2 = c1;
c2.Value = 100;

Console.WriteLine(c1.Value);  // 仍然是 5！
Console.WriteLine(c2.Value);  // 100
```

### 你的任务

通过以下步骤演示值类型的行为：

1. 使用给定的 `initialHealth` 创建一个原始 `Player` 结构体
2. 将其赋值给一个新变量（创建一个副本）
3. 对副本施加伤害
4. 返回原始玩家的生命值（它应该保持不变）

### 方法签名

```csharp
public static int GetOriginalHealthAfterModifyingCopy(int initialHealth, int damageToApply)
```

### 预期结果

```
GetOriginalHealthAfterModifyingCopy(100, 30) -> 100  // 原始对象未改变！
GetOriginalHealthAfterModifyingCopy(50, 50) -> 50   // 副本承受了全部伤害
```

### 解答

```csharp
using System;

public struct Player
{
    public string Name;
    public int Health;
    public int Score;

    public Player(string name, int health, int score)
    {
        Name = name;
        Health = health;
        Score = score;
    }

    public void TakeDamage(int damage)
    {
        Health -= damage;
        if (Health < 0) Health = 0;
    }
}

public class Solution
{
    public static int GetOriginalHealthAfterModifyingCopy(int initialHealth, int damageToApply)
    {
        // 1. 创建原始 Player：Name="Hero"，生命值为给定的 initialHealth，Score=0
        Player original = new Player("Hero", initialHealth, 0);
        // 2. 通过简单赋值创建原始玩家的副本
        Player copy = original;
        // 3. 使用 TakeDamage() 对副本施加伤害
        copy.TakeDamage(damageToApply);
        // 4. 返回原始玩家的 Health
        // 修改 struct 副本不会影响原始对象
        return original.Health;
    }
}
```
