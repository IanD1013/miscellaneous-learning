### LINQ Select - 投影元素

在实际应用程序中，你经常需要转换集合：将数据库记录转换为显示模型、从对象中提取特定字段，或者从原始数据计算派生值。
C# 开发者正是使用 LINQ `Select` 运算符将序列中的每个元素投影为一种新形式，从而生成一个长度相同的全新序列。

### 工作原理

`Select` 会遍历序列中的每个元素，应用你提供的转换函数，并为每个元素生成该函数的结果。
原始序列保持不变，`Select` 会创建一个新序列。
输出序列始终具有与输入序列**相同数量的元素**；改变的只是每个元素的形式或值。

可以把它想象成工厂的流水线：物品从一端进入，机器对每一个进行转换，转换后的物品以相同的顺序从另一端出来。

### 语法

```csharp
// 通用模式
IEnumerable<TResult> result = source.Select(element => transformExpression);
```

Lambda 表达式 `element => transformExpression` 会针对每个元素调用一次。
`TResult` 是根据 lambda 返回的内容推断出来的。

因为 `Select` 返回的是 `IEnumerable<T>`，所以你通常会调用 `.ToArray()` 或 `.ToList()` 将结果实例化为具体的集合。

### 示例

```csharp
// 将字符串转换为它们的长度
string[] words = { "cat", "elephant", "ox" };
int[] lengths = words.Select(w => w.Length).ToArray();
// lengths 为 [3, 8, 2]

// 将温度从摄氏度转换为华氏度
double[] celsius = { 0, 25, 100 };
double[] fahrenheit = celsius.Select(c => c * 9.0 / 5.0 + 32).ToArray();
// fahrenheit 为 [32, 77, 212]

// 提取每个名字的首字母
string[] names = { "Alice", "Bob", "Carol" };
char[] initials = names.Select(n => n[0]).ToArray();
// initials 为 ['A', 'B', 'C']
```

请注意，在每种情况下，输出数组的元素数量都与输入完全相同，只是值有所不同。

### 常用参考

| 方法 | 描述 |
| --- | --- |
| `.Select(x => ...)` | 使用 lambda 转换每个元素 |
| `.ToArray()` | 将 `IEnumerable<T>` 转换为数组 |
| `.ToList()` | 将 `IEnumerable<T>` 转换为 `List<T>` |

### 你的任务

编写一个方法，接收一个整数数组并返回一个**新数组**，其中每个元素都是对应输入元素的平方。
输出数组的长度必须与输入数组相同。

### 方法签名

```csharp
public static int[] Square(int[] numbers)
```

### 预期结果

```scss
Square([1, 2, 3, 4, 5]) -> [1, 4, 9, 16, 25]
Square([0, -3, 7])       -> [0, 9, 49]
Square([10])             -> [100]
Square([])               -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] Square(int[] numbers)
    {
        // 用 Select 把每个元素投影为它的平方，再实例化为数组
        return numbers.Select(n => n * n).ToArray();
    }
}
```
