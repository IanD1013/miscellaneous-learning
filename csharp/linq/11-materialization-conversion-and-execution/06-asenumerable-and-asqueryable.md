### LINQ 中的 AsEnumerable 和 AsQueryable

在实际的 C# 应用程序中，你经常会处理两种形式的 LINQ：**LINQ to Objects**（通过 `IEnumerable<T>` 操作内存中的集合）和**基于提供程序的 LINQ**（通过 `IQueryable<T>` 操作，其中像 Entity Framework 这样的提供程序会将表达式翻译为 SQL）。
方法 `AsEnumerable()` 和 `AsQueryable()` 允许你在单个查询管道中**在这两种模式之间切换**。

理解何时进行切换对于性能和正确性至关重要。
在数据库服务器上运行复杂的 C# 逻辑可能会失败，因为提供程序无法将其翻译为 SQL。
反之，将数百万行数据拉取到内存中仅仅为了进行筛选，则会浪费资源。

### 工作原理

**`AsEnumerable()`** 接收任何 `IEnumerable<T>`（或 `IQueryable<T>`）并将其作为 `IEnumerable<T>` 类型返回。
这会强制所有后续的 LINQ 运算符使用**内存中的 LINQ to Objects** 实现。
它**不会**具体化（materialize）集合，它只是改变了编译器解析的重载版本。

假设你有一个按日期筛选订单的 Entity Framework 查询。
数据库能够高效地处理该操作。
但是接下来你需要应用一个 SQL 无法理解的自定义 C# 函数（例如正则表达式检查）。
通过在此时调用 `.AsEnumerable()`，你告诉 LINQ：“从这里开始，在内存中执行所有操作。”

**`AsQueryable()`** 则相反。
它将 `IEnumerable<T>` 包装在 `IQueryable<T>` 适配器中，允许你对其构建表达式树。
在构建既可以针对内存数据又可以针对数据库提供程序运行的可复用查询逻辑时，这非常有用。

### 语法

```csharp
// 从 IQueryable 切换到 IEnumerable（提供程序 -> 客户端）
IEnumerable<T> clientSide = someQueryable.AsEnumerable();

// 从 IEnumerable 切换到 IQueryable（客户端 -> 表达式树）
IQueryable<T> queryable = someEnumerable.AsQueryable();
```

### 示例

```csharp
// 示例 1：使用数据库查询筛选员工，
// 然后在客户端应用自定义 C# 方法
var results = dbContext.Employees
    .Where(e => e.Department == "Engineering")  // 翻译为 SQL
    .AsEnumerable()                              // 切换到客户端
    .Where(e => CustomScoreCalculation(e))       // 在 C# 内存中运行
    .ToList();

// 示例 2：在内存数据上构建可复用的筛选器
List<string> names = new() { "Alice", "Bob", "Charlie" };
var queryable = names.AsQueryable();
// 现在你可以针对 'queryable' 构建表达式树
var filtered = queryable.Where(n => n.Length > 3).ToList();
// 结果: ["Alice", "Charlie"]

// 示例 3：混合使用提供程序操作和客户端操作
var orders = dbContext.Orders
    .Where(o => o.Total > 100)          // SQL 处理此项
    .OrderBy(o => o.Date)               // SQL 也处理此项
    .AsEnumerable()                     // 切换到内存
    .Select(o => FormatReceipt(o))      // 仅限 C# 的格式化操作
    .ToList();
```

### 何时使用

| 方法 | 使用时机 | 效果 |
| --- | --- | --- |
| `AsEnumerable()` | 当你需要应用查询提供程序无法翻译的 C# 逻辑时 | 强制使用 LINQ to Objects 求值 |
| `AsQueryable()` | 当你想对内存数据构建可组合的表达式树时 | 包装为 `IQueryable<T>` 以进行表达式树组合 |

### 核心要点

转换发生的时机至关重要。
`AsEnumerable()` **之前**的所有内容都可以由提供程序处理（例如翻译为 SQL）。
`AsEnumerable()` **之后**的所有内容都会在应用程序的内存中运行。
尽量将 `AsEnumerable()` 放在管道尽可能靠后的位置，以便让提供程序承担繁重的工作，但要置于任何需要客户端 C# 逻辑的操作之前。

### 你的任务

编写一个方法 `GetPrimesFromPositives`，该方法接收一个整数数组，并从输入中返回所有正素数的**排序数组**。

你的管道应演示 `AsEnumerable()` 的转换过程：

1. 首先使用 `AsQueryable()` 将输入视为 `IQueryable<int>` - 模拟由提供程序支持的数据源
2. 在仍处于 queryable 阶段时筛选出**正数**
3. 调用 `AsEnumerable()` 切换到客户端求值
4. 使用提供的 `IsPrime` 辅助方法筛选出**素数**（这代表了查询提供程序无法翻译的逻辑）
5. 将结果按升序排序并作为 `int[]` 返回

初始代码中已提供私有辅助方法 `IsPrime`。

### 方法签名

```csharp
public static int[] GetPrimesFromPositives(int[] numbers)
```

### 预期结果

```scss
GetPrimesFromPositives([1, -2, 3, -4, 5, 6, 7, 8, 9, 10]) -> [3, 5, 7]
GetPrimesFromPositives([2, 4, 6, 8]) -> [2]
GetPrimesFromPositives([-5, -3, -1, 0]) -> []
```

### 解答

```csharp
using System;
using System.Linq;
using System.Collections.Generic;

public class Solution
{
    public static int[] GetPrimesFromPositives(int[] numbers)
    {
        return numbers
            .AsQueryable()              // 视为 IQueryable<int>，模拟由提供程序支持的数据源
            .Where(n => n > 0)          // 仍处于 queryable 阶段时筛选正数
            .AsEnumerable()             // 切换到客户端求值
            .Where(n => IsPrime(n))     // 使用 IsPrime 辅助方法筛选素数
            .OrderBy(n => n)            // 按升序排序
            .ToArray();                 // 作为 int[] 返回
    }

    private static bool IsPrime(int n)
    {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        for (int i = 3; i * i <= n; i += 2)
        {
            if (n % i == 0) return false;
        }
        return true;
    }
}
```
