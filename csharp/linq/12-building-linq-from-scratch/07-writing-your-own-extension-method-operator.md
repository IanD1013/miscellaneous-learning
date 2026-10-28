### 自定义 LINQ 风格的扩展方法

你每天使用的每个 LINQ 运算符（如 `Where`、`Select`、`OrderBy`）都只是在静态类中针对 `IEnumerable<T>` 定义的静态扩展方法。
它们并没有什么神奇之处；C# 编译器会将 `source.Where(predicate)` 重写为 `Enumerable.Where(source, predicate)`。
这意味着你可以创建自己的运算符，并与内置运算符无缝链式调用。

### 扩展方法的工作原理

扩展方法是静态类中的静态方法，其第一个参数使用 `this` 关键字进行修饰。
`this` 参数告诉编译器允许像调用该类型上的实例方法一样调用此方法。

```csharp
public static class StringExtensions
{
    public static string Shout(this string text)
    {
        return text.ToUpper() + "!!!";
    }
}

// 用法：
string greeting = "hello".Shout(); // "HELLO!!!"
```

当扩展方法返回 `IEnumerable<T>` 时，它就变成了一个可链式调用的 LINQ 风格运算符。

### 语法

```csharp
public static class MyLinqExtensions
{
    public static IEnumerable<T> MyOperator<T>(this IEnumerable<T> source)
    {
        // 遍历 source，应用逻辑，yield return 选中的元素
    }
}
```

关键规则：

- 类**必须**是 `static`。
- 方法**必须**是 `static`。
- 第一个参数**必须**使用 `this` 关键字。
- 使用 `yield return` 逐个延迟生成元素。

### 带有 `yield return` 的迭代器方法

包含 `yield return` 的方法会被编译成一个按需生成元素的状态机，就像内置的 LINQ 运算符一样。
在有代码对结果进行枚举之前，该方法不会执行。

```csharp
public static IEnumerable<int> EveryThird(this IEnumerable<int> source)
{
    int count = 0;
    foreach (var item in source)
    {
        if (count % 3 == 0)
            yield return item;
        count++;
    }
}

// [10, 20, 30, 40, 50, 60, 70, 80, 90].EveryThird()
// 产出：10, 40, 70
```

注意其模式：跟踪位置、应用条件，并 `yield return` 匹配的元素。

### 示例

```csharp
// 将每个元素翻倍的扩展方法
public static IEnumerable<int> DoubleEach(this IEnumerable<int> source)
{
    foreach (var item in source)
        yield return item * 2;
}
// [3, 5, 7].DoubleEach() → 6, 10, 14

// 在低于阈值时持续取元素的扩展方法
public static IEnumerable<int> TakeWhileBelow(this IEnumerable<int> source, int max)
{
    foreach (var item in source)
    {
        if (item >= max) yield break;
        yield return item;
    }
}
// [1, 3, 5, 8, 2].TakeWhileBelow(6) → 1, 3, 5
```

### 你的任务

在 `IEnumerable<int>` 上创建一个名为 `MyAlternate` 的自定义 LINQ 风格扩展方法，该方法从索引 0 开始每隔一个元素返回一次。
也就是说，它生成索引为 0、2、4、6 等位置的元素。

然后实现 `Solution.GetAlternate(int[] numbers)`，该方法对输入数组调用 `MyAlternate()`，并将结果作为 `int[]` 返回。

扩展类和 `Solution` 类都在同一个文件中。
已提供扩展类骨架，你需要实现这两个方法。

### 方法签名

```csharp
// 在 EnumerableExtensions（静态类）中：
public static IEnumerable<int> MyAlternate(this IEnumerable<int> source)

// 在 Solution 中：
public static int[] GetAlternate(int[] numbers)
```

### 预期结果

```scss
GetAlternate([1, 2, 3, 4, 5, 6])  → [1, 3, 5]
GetAlternate([10, 20, 30])         → [10, 30]
GetAlternate([42])                 → [42]
GetAlternate([])                   → []
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int[] GetAlternate(int[] numbers)
    {
        // 对数组调用 MyAlternate()，并转换为数组
        return numbers.MyAlternate().ToArray();
    }
}

public static class EnumerableExtensions
{
    // IEnumerable<int> 上的 MyAlternate 扩展方法
    // 从索引 0 开始每隔一个元素产出一次
    public static IEnumerable<int> MyAlternate(this IEnumerable<int> source)
    {
        int index = 0;
        foreach (var item in source)
        {
            // 只产出偶数索引位置的元素
            if (index % 2 == 0)
                yield return item;
            index++;
        }
    }
}
```
