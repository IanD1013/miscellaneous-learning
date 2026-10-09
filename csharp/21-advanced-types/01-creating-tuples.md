### C# 中的元组 (Tuples)

元组（Tuples）允许你将多个值组合成一个轻量级的数据结构，而无需创建单独的类。

### 创建元组

```csharp
// 使用圆括号语法创建基本元组
(int, string) person = (25, "Alice");

// 也可以使用 var 进行类型推断
var coordinates = (10.5, 20.3);

// 元组可以容纳任意类型的组合
(string, int, bool) record = ("Product", 100, true);
```

### 从方法中返回元组

```csharp
// 方法可以返回元组
public static (string, int) GetPerson()
{
    return ("Bob", 30);
}

// 调用方接收到组合在一起的两个值
var result = GetPerson();
// result.Item1 = "Bob", result.Item2 = 30
```

### 元组 vs 类

| 元组 | 类 |
| --- | --- |
| 快速、内联分组 | 具名的、可复用的类型 |
| 无需定义类型 | 需要定义类 |
| 通过 Item1、Item2... 访问 | 通过属性名称访问 |
| 非常适合返回多个值 | 更适合复杂的数据模型 |

### 你的任务

创建一个方法，接收一个人的姓名和年龄，然后将它们作为元组返回。
元组中应首先包含姓名，其次包含年龄。

### 方法签名

```csharp
public static (string, int) CreatePersonTuple(string name, int age)
```

### 预期结果

```
CreatePersonTuple("Alice", 25) -> ("Alice", 25)
CreatePersonTuple("Bob", 42) -> ("Bob", 42)
```

### 解答

```csharp
using System;

public class Solution
{
    public static (string, int) CreatePersonTuple(string name, int age)
    {
        // 先放姓名，再放年龄
        return (name, age);
    }
}
```
