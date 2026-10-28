### C# 中的 Struct

**struct** 是一种将相关数据组合在一起的值类型。
对于表示单一值的小型、简单数据结构（如坐标或颜色），请使用 struct。

### 定义一个 Struct

```csharp
public struct Point
{
    public int X;
    public int Y;
}
```

### Struct 与 Class 的对比

| 特性 | Struct | Class |
| --- | --- | --- |
| 类型 | 值类型 | 引用类型 |
| 存储 | 栈（通常） | 堆 |
| 默认值 | 不能为 null | 可以为 null |
| 适用场景 | 小型、简单的数据 | 复杂的对象 |

### 创建和使用 Struct

```csharp
// 方法 1：直接为字段赋值
Point p1;
p1.X = 10;
p1.Y = 20;

// 方法 2：使用对象初始化器
Point p2 = new Point { X = 5, Y = 15 };

// 访问字段
int xValue = p1.X;  // 10
```

### 何时使用 Struct

- 数据量较小（建议 16 字节或更少）
- 逻辑上表示单一值
- 不可变或极少修改
- 示例：坐标、RGB 颜色、时间间隔

### 你的任务

1. 定义一个带有两个 public `int` 字段（`X` 和 `Y`）的 `Point` struct
2. 实现 `DescribePoint`，创建一个 Point，设置其 X 和 Y 的值，并返回格式化后的字符串

### 方法签名

```csharp
public static string DescribePoint(int x, int y)
```

### 预期结果

```
DescribePoint(3, 4) -> "Point(3, 4)"
DescribePoint(0, 0) -> "Point(0, 0)"
DescribePoint(-5, 10) -> "Point(-5, 10)"
```

### 解答

```csharp
using System;

// 定义 Point struct
public struct Point
{
    // X 和 Y 字段
    public int X;
    public int Y;
}

public class Solution
{
    public static string DescribePoint(int x, int y)
    {
        // 使用给定的 x 和 y 创建一个 Point
        Point p = new Point { X = x, Y = y };
        // 按 "Point(X, Y)" 格式返回字符串
        return $"Point({p.X}, {p.Y})";
    }
}
```
