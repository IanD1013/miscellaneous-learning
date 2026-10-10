### C# 13 中的 Params 集合

C# 13 扩展了 `params` 关键字，使其可以与任何集合类型一起使用，而不仅仅是数组。
这允许你将 `List<T>`、`Span<T>`、`ReadOnlySpan<T>` 以及其他集合类型用作 params 参数。

### 传统的 Params（仅限数组）

```csharp
// C# 13 之前，只支持数组
public static int Sum(params int[] numbers)
{
    return numbers.Sum();
}

// 调用它
Sum(1, 2, 3, 4, 5);
```

### 搭配 List<T> 的 Params（C# 13+）

```csharp
// C# 13，params 可以用于 List<T>
public static int Sum(params List<int> numbers)
{
    return numbers.Sum();
}

// 调用它，语法相同！
Sum(1, 2, 3, 4, 5);

// 也可以传入一个已有的列表
List<int> myList = new List<int> { 10, 20, 30 };
Sum(myList);  // 这样也可以！
```

### 支持的集合类型

| 类型 | 描述 |
| --- | --- |
| `List<T>` | 可变列表 |
| `Span<T>` | 栈分配的内存跨度 |
| `ReadOnlySpan<T>` | 只读内存跨度 |
| `IEnumerable<T>` | 任何可枚举类型 |

### Params 集合的优势

- 参数类型具有更高的灵活性
- 使用 `Span<T>` 进行栈分配可带来更好的性能
- 调用方可以传递单个元素或集合

### 你的任务

创建一个名为 `SumAll` 的方法，该方法接受一个 `params List<int>` 参数，并返回列表中所有数字的总和。

### 方法签名

```csharp
public static int SumAll(params List<int> numbers)
```

### 预期结果

```
SumAll(1, 2, 3) -> 6
SumAll(10, 20, 30, 40) -> 100
SumAll() -> 0
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public class Solution
{
    public static int SumAll(params List<int> numbers)
    {
        // 遍历列表，累加每个数字；空列表时返回 0
        int total = 0;
        foreach (int number in numbers)
        {
            total += number;
        }
        return total;
    }
}
```
