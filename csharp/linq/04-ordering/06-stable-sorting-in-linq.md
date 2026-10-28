### LINQ 中的稳定排序

当对一个集合进行排序时，拥有相同排序键的元素会发生什么？
在某些排序算法中，具有相同键的元素可能会以任意顺序排列，结果是不可预测的。
**稳定排序**（stable sort）保证具有相同键的元素保留它们在源序列中的原始相对顺序。
LINQ 的 `OrderBy` 和 `ThenBy` 方法被明确记录为稳定排序，这使得它们在排序键无法唯一标识每个元素时非常可靠。

### 为什么稳定性很重要

设想你有一个已经按入职日期排序的员工列表。
然后你按部门对他们进行排序。
使用稳定排序，同一部门内的员工仍将保持入职日期的顺序，无需额外操作。
而使用不稳定排序，你将失去这种次要排序顺序。

稳定性在链式排序时也很重要。
`ThenBy` 依赖于前面的 `OrderBy` 的稳定性，以便在不破坏主要排序的前提下叠加额外的排序条件。

### 语法

```csharp
// OrderBy 按从每个元素中提取的键排序
var sorted = collection.OrderBy(element => keySelector);

// ThenBy 添加次要排序（保留主要排序的顺序）
var multiSorted = collection
    .OrderBy(element => primaryKey)
    .ThenBy(element => secondaryKey);
```

### 示例

考虑一个带有成绩的学生列表：

```csharp
var students = new[] { "Carlos-B", "Alice-A", "Bob-B", "Diana-A" };

// 仅按成绩字母（连字符后面的字符）排序
var byGrade = students.OrderBy(s => s.Split('-')[1]).ToArray();
// 结果：["Alice-A", "Diana-A", "Carlos-B", "Bob-B"]
// 两名 A 等学生保持了原始顺序（Alice 在 Diana 之前）
// 两名 B 等学生保持了原始顺序（Carlos 在 Bob 之前）
```

另一个数字示例：

```csharp
var items = new[] { 12, 25, 13, 21, 14 };

// 仅按十位数字排序
var byTens = items.OrderBy(n => n / 10).ToArray();
// 结果：[12, 13, 14, 25, 21]
// 十位为 1 的所有元素保持原始顺序：12, 13, 14
// 十位为 2 的所有元素保持原始顺序：25, 21
```

### 核心要点：按部分键排序

当你仅提取数据的一部分作为排序键时（例如仅提取第一个字母、仅提取十位数或仅提取成绩），多个元素将共享相同的键。
稳定性保证意味着你可以精确预测这些具有相同键的元素将以何种顺序出现，即它们在输入中的原始相对顺序。

### 访问字符串中的字符

请记住，C# 中的字符串支持索引访问：

```csharp
string word = "hello";
char firstChar = word[0]; // 'h'
char lastChar = word[word.Length - 1]; // 'o'
```

字符（`char`）天然支持比较，当作为键使用时会按字母顺序排序。

### 你的任务

编写一个方法，接收一个单词数组，并**仅按其首字母的字母顺序**对其进行排序。
以相同字母开头的单词必须保留它们在输入数组中的原始相对顺序。

例如，如果输入在 `"blueberry"` 之前包含 `"banana"`，且两者都以 `'b'` 开头，那么无论完整的字母顺序如何，输出中 `"banana"` 都必须出现在 `"blueberry"` 之前。

### 方法签名

```csharp
public static string[] SortByFirstChar(string[] words)
```

### 预期结果

```css
SortByFirstChar(["banana", "apple", "cherry", "avocado", "blueberry"]) -> ["apple", "avocado", "banana", "blueberry", "cherry"]
SortByFirstChar(["dog", "cat", "duck", "cow"]) -> ["cat", "cow", "dog", "duck"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] SortByFirstChar(string[] words)
    {
        // 仅以首字母作为排序键，稳定排序会保留首字母相同单词的原始顺序
        return words.OrderBy(w => w[0]).ToArray();
    }
}
```
