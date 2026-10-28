### 带有结果选择器的 SelectMany

当扁平化嵌套集合时，你通常需要知道每个子项来自**哪个父项**。
`SelectMany` 的双参数重载完美地解决了这个问题：它允许你在单一步骤中将每个子项与其父项一起投影，而不会丢失这种父子关系。

这在实际应用中非常宝贵：例如将部门与其每位员工进行配对、将商店与其每件商品进行配对，或将播放列表与其每首歌曲进行配对。

### 工作原理

基础的 `SelectMany(collectionSelector)` 会扁平化嵌套集合，但会丢弃对父项的所有引用。
双参数重载则添加了一个**结果选择器（result selector）**，这是第二个函数，同时接收父元素和当前子元素，让你能随意将它们组合在一起。

可以把它想象成拆箱子：集合选择器打开每个箱子以展现其中的内容，而结果选择器则给每件物品贴上标签，标明它来自哪个箱子。

### 语法

```csharp
source.SelectMany(
    collectionSelector,   // (parent) => 子集合
    resultSelector         // (parent, child) => 投影结果
);
```

集合选择器还有一个带索引的变体：

```csharp
source.SelectMany(
    (parent, index) => childCollections[index],  // 用索引找到子项
    (parent, child) => /* 组合父项和子项 */
);
```

### 示例

```csharp
// 示例 1：将每个团队与其成员配对
string[] teams = { "Alpha", "Beta" };
string[][] members = { new[] { "Alice", "Bob" }, new[] { "Carol" } };

var roster = teams.SelectMany(
    (team, i) => members[i],
    (team, member) => $"{team} - {member}"
).ToArray();
// 结果：["Alpha - Alice", "Alpha - Bob", "Beta - Carol"]

// 示例 2：将每位作者与其书名配对
var authors = new[] { "Tolkien", "Rowling" };
var books = new[] {
    new[] { "The Hobbit", "The Silmarillion" },
    new[] { "Harry Potter", "The Casual Vacancy" }
};

var catalog = authors.SelectMany(
    (author, i) => books[i],
    (author, book) => $"{book} by {author}"
).ToArray();
// 结果：["The Hobbit by Tolkien", "The Silmarillion by Tolkien",
//        "Harry Potter by Rowling", "The Casual Vacancy by Rowling"]

// 示例 3：不使用结果选择器（用于对比）
var flatBooks = authors.SelectMany((a, i) => books[i]).ToArray();
// 结果：["The Hobbit", "The Silmarillion", "Harry Potter", "The Casual Vacancy"]
// 注意：作者信息丢失了！
```

### 常见模式

| 模式 | 集合选择器（Collection Selector） | 结果选择器（Result Selector） |
| --- | --- | --- |
| 平行数组 | `(parent, i) => otherArray[i]` | `(parent, child) => ...` |
| 嵌套属性 | `parent => parent.Children` | `(parent, child) => ...` |
| 格式化输出 | 任意 | `(parent, child) => $"{parent}: {child}"` |

### 你的任务

你将获得两个平行数组：`categories`（类别名称数组）和 `items`（交错数组，其中 `items[i]` 包含属于 `categories[i]` 的项目）。

编写一个方法，使用带有结果选择器的 `SelectMany` 将每个项目与其所属的父类别配对。
每个配对项的格式应为 `"category: item"`（类别名称、冒号、空格、项目名称）。
结果应保持其自然顺序：第一个类别的所有项目首先出现，然后是第二个类别的所有项目，依此类推。

### 方法签名

```csharp
public static string[] PairWithParent(string[] categories, string[][] items)
```

### 预期结果

```css
PairWithParent(["fruits", "veggies"], [["apple", "banana"], ["carrot", "pea"]])
  -> ["fruits: apple", "fruits: banana", "veggies: carrot", "veggies: pea"]

PairWithParent(["colors"], [["red", "blue", "green"]])
  -> ["colors: red", "colors: blue", "colors: green"]
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] PairWithParent(string[] categories, string[][] items)
    {
        return categories.SelectMany(
            // 集合选择器：用索引取出该类别对应的项目数组
            (category, i) => items[i],
            // 结果选择器：把类别和项目组合成 "category: item"
            (category, item) => $"{category}: {item}"
        ).ToArray();
    }
}
```
