### 多次枚举的陷阱

LINQ 代码中最常见也最隐蔽的错误之一，就是对同一个 `IEnumerable<T>` 进行多次迭代。
因为 LINQ 使用了**延迟执行**（deferred execution），所以 `IEnumerable<T>` 本身并不保存结果，它只包含生成结果的*配方（recipe）*。
每次你对其进行枚举时（使用 `foreach`、`.Count()`、`.Sum()`、`.ToList()` 等），整个管道都会从头重新执行一遍。

对于内存中的集合，这仅仅是浪费资源；但对于依赖数据库查询、文件读取或网络调用的数据源，这意味着**会多次执行开销巨大的操作**，更糟糕的是，如果底层数据发生变化，每次还可能得到不同的结果。

### 工作原理

思考以下代码：

```csharp
IEnumerable<string> names = GetNamesFromDatabase(); // 延迟执行！
int total = names.Count();    // 第 1 次枚举 - 执行查询
var first = names.First();    // 第 2 次枚举 - 再次执行查询
```

数据库查询被执行了**两次**。
如果查询需要 200 毫秒，你毫无必要地将延迟增加了一倍。
更严重的是，如果在这两次调用之间插入了新行，`Count()` 和实际获取到的数据可能会出现不一致。

### 解决方法：物化一次

解决方案是在多次使用该序列之前，将其**物化**（materialize）为具体集合：

```csharp
var namesList = GetNamesFromDatabase().ToList(); // 只执行一次查询
int total = namesList.Count;    // 从内存中的列表读取
var first = namesList.First();  // 从内存中的列表读取
```

当你需要可调整大小的列表时，请使用 `.ToList()`；当你需要固定大小的数组时，请使用 `.ToArray()`。
这两者都会强制立即求值，并将所有元素存储在内存中。

### 语法

```csharp
// 物化为 List<T>
List<T> list = someEnumerable.ToList();

// 物化为数组
T[] array = someEnumerable.ToArray();

// 然后可以安全地进行多个操作
int count = list.Count;       // 属性 - 不会重新枚举
T first = list[0];            // 直接索引访问
int sum = list.Sum();         // 遍历内存中的列表
```

### 示例

```csharp
// 错误：对延迟查询进行多次枚举
IEnumerable<decimal> prices = products.Select(p => p.Price * 1.1m);
decimal avg = prices.Average();  // 第 1 次枚举
decimal max = prices.Max();      // 第 2 次枚举 - 重新计算所有内容

// 正确：先物化，然后自由使用
var priceList = products.Select(p => p.Price * 1.1m).ToList();
decimal avg = priceList.Average();  // 快速 - 从内存读取
decimal max = priceList.Max();      // 快速 - 从内存读取
```

```csharp
// 危险：数据源可能是只能使用一次的流
IEnumerable<string> lines = ReadLinesFromStream(stream);
int lineCount = lines.Count();        // 读取流
string header = lines.First();        // 流已被消耗 - 出错！

// 安全：只物化一次流
var allLines = ReadLinesFromStream(stream).ToList();
int lineCount = allLines.Count;       // 正常工作
string header = allLines[0];          // 正常工作
```

### 检测该问题

**ReSharper** 和 **Rider** 等工具会显示警告：*"Possible multiple enumeration of IEnumerable"*（可能多次枚举 IEnumerable）。
这就是提示你进行物化的信号。
经验法则：如果一个方法参数是 `IEnumerable<T>` 且你打算使用它多次，请在方法的最开始将其物化。

| 方法 | 是否重新枚举？ | 多次使用是否安全？ |
| --- | --- | --- |
| 原始 `IEnumerable<T>` | 是 - 每次都枚举 | 否 |
| `.ToList()` | 否 - 已物化 | 是 |
| `.ToArray()` | 否 - 已物化 | 是 |

### 你的任务

编写一个方法，接收一个 `IEnumerable<int>` 数据源，并在不对数据源进行多次枚举的情况下，安全地**同时**计算元素数量和总和。
该方法应：

1. 首先将数据源物化为具体集合
2. 从物化后的集合中计算元素数量和总和
3. 将结果作为 `int[]` 返回，格式为 `[count, sum]`

每当你接收到一个 `IEnumerable<T>` 参数并需要对其执行多个操作时，这种模式都是必不可少的。

### 方法签名

```csharp
public static int[] SafeCountAndSum(IEnumerable<int> source)
```

### 预期结果

```scss
SafeCountAndSum([1, 2, 3, 4, 5]) -> [5, 15]
SafeCountAndSum([10]) -> [1, 10]
SafeCountAndSum([]) -> [0, 0]
```

### 解答

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution
{
    public static int[] SafeCountAndSum(IEnumerable<int> source)
    {
        // 只枚举一次数据源，物化为 List<int>
        List<int> list = source.ToList();

        // Count 是属性，Sum() 遍历的是内存中的列表
        return new int[] { list.Count, list.Sum() };
    }
}
```
