### 从固定循环到可复用操作符

在本章中，你构建的每个操作符都把规则硬编码在循环中：`FilterEvens` 只能保留偶数，`DoubleAll` 只能翻倍，而 `MultiplyAll` 只能相乘。
LINQ 的操作符将这些规则作为参数接收。
`Where` 接收要应用的测试条件，`Select` 接收转换操作，而 `Aggregate` 接收种子值和组合步骤。
在这个综合练习中，你将自己编写这三个操作符。
随后 `Callers.cs` 中的两个调用方将分别在数字和单词上使用它们。

### 使用 `Func` 传递行为

`Func<...>` 是一种委托类型：一个持有方法的参数或变量，通常以 lambda 形式编写。
最后一个类型参数是返回类型，前面的类型参数则是输入参数：

- `Func<int, bool>` 接收一个 `int` 并返回一个 `bool`，例如 `n => n > 0`
- `Func<string, int>` 接收一个 `string` 并返回一个 `int`，例如 `w => w.Length`
- `Func<string, int, string>` 接收一个 `string` 和一个 `int` 并返回一个 `string`

在方法内部，调用委托参数的方式与调用方法相同：`predicate(item)`。

### 泛型扩展方法

方法名后面尖括号中的类型参数允许一个方法适用于任何元素类型，编译器会从参数中推断出该类型。
在静态类中，使用 `this` 修饰第一个参数，该方法即可通过点语法调用：

```csharp
public static class CountingExtensions
{
    public static int MyCount<T>(this IEnumerable<T> source, Func<T, bool> predicate)
    {
        int count = 0;
        foreach (T item in source)
        {
            if (predicate(item))
            {
                count++;
            }
        }
        return count;
    }
}

int longWords = new[] { "map", "filter", "fold" }.MyCount(w => w.Length > 3); // 2
int positives = new[] { -1, 4, 9 }.MyCount(n => n > 0);                       // 2
```

一个操作符可以有多个类型参数。
投影返回的元素类型与其接收的元素类型不同，因此输入需要 `T`，输出需要 `TResult`。
折叠需要它自己的 `TAccumulate`，因为累加值通常与集合项具有不同的类型：`Callers.cs` 将数字折叠为 `List<int>`，并将单词折叠为 `string`。

### 你的任务

在不使用内置 LINQ 操作符或 `Array.Sort` 的情况下，完成 `Main.cs` 中的两个静态类：

1. `MiniLinq`，包含三个扩展方法：
   - `MyWhere` 使用 `yield return` 按原始顺序产出谓词返回 `true` 的每个项。
   - `MySelect` 使用 `yield return` 产出选择器对每个项的处理结果。
   - `MyAggregate` 从种子值开始，按顺序对每个项应用组合函数，并返回最终的累加器。
2. `Sorting.InsertionSort`，使用插入排序就地升序对 `int[]` 进行排序。

`Callers.cs` 是只读的，并且已经在 `int[]` 和 `string[]` 上调用了你的操作符，因此它们必须是泛型的，并将行为作为委托接收。

### 方法签名

```csharp
public static IEnumerable<T> MyWhere<T>(this IEnumerable<T> source, Func<T, bool> predicate)
public static IEnumerable<TResult> MySelect<T, TResult>(this IEnumerable<T> source, Func<T, TResult> selector)
public static TAccumulate MyAggregate<T, TAccumulate>(this IEnumerable<T> source, TAccumulate seed, Func<TAccumulate, T, TAccumulate> func)
public static void InsertionSort(int[] values)
```

### 预期结果

```css
Callers.Pipeline([-1, 3, -2, 5, 2, -4, 4])                   -> [4, 6, 8, 10]
Callers.Pipeline([10, -5, 3, -1, 7])                         -> [6, 14, 20]
Callers.Pipeline([-3, -2, -1])                               -> []
Callers.LongWordsInCaps(["map", "filter", "fold", "reduce"]) -> FILTER FOLD REDUCE
Callers.LongWordsInCaps(["yield", "is", "lazy"])             -> YIELD LAZY
```

### 解答

```csharp
using System;
using System.Collections.Generic;

public static class MiniLinq
{
    // 按原始顺序产出谓词返回 true 的每个项
    public static IEnumerable<T> MyWhere<T>(this IEnumerable<T> source, Func<T, bool> predicate)
    {
        foreach (T item in source)
        {
            if (predicate(item))
            {
                yield return item;
            }
        }
    }

    // 产出选择器对每个项的处理结果
    public static IEnumerable<TResult> MySelect<T, TResult>(this IEnumerable<T> source, Func<T, TResult> selector)
    {
        foreach (T item in source)
        {
            yield return selector(item);
        }
    }

    // 从种子值开始，按顺序对每个项应用组合函数，返回最终的累加器
    public static TAccumulate MyAggregate<T, TAccumulate>(this IEnumerable<T> source, TAccumulate seed, Func<TAccumulate, T, TAccumulate> func)
    {
        TAccumulate accumulator = seed;
        foreach (T item in source)
        {
            accumulator = func(accumulator, item);
        }
        return accumulator;
    }
}

public static class Sorting
{
    public static void InsertionSort(int[] values)
    {
        // 就地升序排序：从第二个元素开始
        for (int i = 1; i < values.Length; i++)
        {
            // 保存 key，避免移动时被覆盖
            int key = values[i];
            int j = i - 1;

            // 将比 key 大的元素向右移动一位
            while (j >= 0 && values[j] > key)
            {
                values[j + 1] = values[j];
                j--;
            }

            // 将 key 插入空出的位置
            values[j + 1] = key;
        }
    }
}
```
