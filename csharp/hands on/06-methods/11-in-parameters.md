### in 关键字

`in` 关键字以**只读引用的方式**传递参数，既能高效传递大型值类型，又能保证方法无法修改原始值。

### 为什么使用 in 参数？

```csharp
// 不使用 'in'：结构体会被复制（对大型结构体开销很大）
public static double Calculate(Point p) { ... }

// 使用 'in'：按引用传递，不会产生副本
public static double Calculate(in Point p) { ... }
```

### 只读保证

与 `ref` 不同，`in` 关键字可以防止修改：

```csharp
public static void Process(in Point p)
{
    // p.X = 10;  // 错误：无法修改，它是只读的！
    double x = p.X;  // 可以：允许读取
}
```

### 比较：ref vs in vs out

| 修饰符 | 可读取 | 可修改 | 调用前必须初始化 | 方法内必须赋值 |
| --- | --- | --- | --- | --- |
| `ref` | 是 | 是 | 是 | 否 |
| `in` | 是 | 否 | 是 | 否 |
| `out` | 仅在赋值后 | 是 | 否 | 是 |

### 何时使用 in

- 传递大型结构体（超过 16 字节）以避免复制开销
- 当你想要保证方法不会更改该值时
- 用于涉及值类型且对性能要求极高的代码

### 你的任务

创建一个使用 `in` 参数计算从原点 (0, 0) 到给定点距离的方法。

**距离公式：** `√(x² + y²)`

### 方法签名

```csharp
public static double DistanceFromOrigin(in Point point)
```

### 预期结果

```
DistanceFromOrigin(new Point(3, 4)) -> 5.0
DistanceFromOrigin(new Point(0, 5)) -> 5.0
DistanceFromOrigin(new Point(1, 1)) -> 1.41（近似值）
```

### 解答

```csharp
using System;

public struct Point
{
    public double X;
    public double Y;
    
    public Point(double x, double y)
    {
        X = x;
        Y = y;
    }
}

public class Solution
{
    public static double DistanceFromOrigin(in Point point)
    {
        // 计算从原点 (0, 0) 到该点的距离：sqrt(x² + y²)
        // 'in' 表示只能读取 point.X 和 point.Y，不能修改
        return Math.Sqrt(point.X * point.X + point.Y * point.Y);
    }
}
```
