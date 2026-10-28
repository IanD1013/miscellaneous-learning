### C# 中的三序列 Zip

从 .NET 6 开始，LINQ 的 `Zip` 方法增加了一个强大的重载，可以接受**另外两个序列**，这意味着你可以在单次调用中将三个序列压缩（zip）在一起。
在此之前，合并三个集合需要使用嵌套的 `Zip` 调用或手动跟踪索引，这两种方式都很繁琐且难以阅读。
三序列 `Zip` 使得在多个集合上进行并行迭代变得简洁且富有表现力。

### 工作原理

你可能很熟悉经典的双序列 `Zip`：它同步遍历两个集合，将相同索引处的元素配对。
三序列重载执行相同的操作，但针对的是**三个**集合。
它会生成一个 `(First, Second, Third)` 元组序列，每个索引位置对应一个元组。
与所有 `Zip` 重载一样，当**最短**的序列耗尽时它就会停止，因此你永远不会遇到 `IndexOutOfRangeException`。

### 语法

```csharp
// 双序列 Zip（经典）
var pairs = first.Zip(second);
// 每个元素都是一个包含 .First 和 .Second 的 ValueTuple<T1, T2>

// 三序列 Zip (.NET 6+)
var triples = first.Zip(second, third);
// 每个元素都是一个包含 .First、.Second 和 .Third 的 ValueTuple<T1, T2, T3>
```

因为 `Zip` 返回元组，所以你可以链式调用 `.Select(...)` 将每个元组转换为所需的任何结果。

### 示例

```csharp
// 示例 1：将姓名、城市和年龄合并为格式化字符串
string[] names  = { "Alice", "Bob" };
string[] cities = { "London", "Paris" };
int[] ages      = { 30, 25 };

var profiles = names.Zip(cities, ages)
    .Select(t => $"{t.First}, age {t.Third}, from {t.Second}");
// ["Alice, age 30, from London", "Bob, age 25, from Paris"]

// 示例 2：从原始分、权重和加分数组计算加权得分
double[] raw    = { 80.0, 90.0, 70.0 };
double[] weight = { 0.5, 0.3, 0.2 };
double[] bonus  = { 5.0, 0.0, 10.0 };

var scores = raw.Zip(weight, bonus)
    .Select(t => t.First * t.Second + t.Third);
// [45.0, 27.0, 24.0]

// 示例 3：最短的序列决定长度
int[] x = { 1, 2, 3, 4, 5 };
int[] y = { 10, 20 };
int[] z = { 100, 200, 300 };

var result = x.Zip(y, z).Select(t => t.First + t.Second + t.Third);
// [111, 222] - 只有 2 个元素，因为 y 的长度为 2
```

### 元组属性

三序列 `Zip` 返回的元组具有以下属性：

| 属性 | 描述 |
| --- | --- |
| `t.First` | 来自第一个（调用方）序列的元素 |
| `t.Second` | 来自第二个序列的元素 |
| `t.Third` | 来自第三个序列的元素 |

你也可以在 lambda 表达式中使用**元组解构**：`.Select(t => { var (x, y, z) = t; return x + y + z; })`

### 你的任务

编写一个方法，接收三个整数数组，并返回一个新的整数数组，其中每个元素都是所有三个输入数组在对应索引处元素的**和**。
使用三序列 `Zip` 重载后接 `Select` 来计算每个和。

请记住：如果数组长度不同，生成的结果数量应与最短数组的元素数量一致。

### 方法签名

```csharp
public static int[] ZipThree(int[] a, int[] b, int[] c)
```

### 预期结果

```css
ZipThree([1, 2, 3], [4, 5, 6], [7, 8, 9])       -> [12, 15, 18]
ZipThree([10], [20], [30])                        -> [60]
ZipThree([1, 2, 3, 4], [10, 20], [100, 200, 300]) -> [111, 222]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] ZipThree(int[] a, int[] b, int[] c)
    {
        // 三序列 Zip 生成 (First, Second, Third) 元组，再用 Select 求和
        return a.Zip(b, c)
            .Select(t => t.First + t.Second + t.Third)
            .ToArray();
    }
}
```
