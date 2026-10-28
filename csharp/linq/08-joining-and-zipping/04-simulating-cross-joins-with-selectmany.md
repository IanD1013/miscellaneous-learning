### 使用 SelectMany 生成笛卡尔积

在实际应用中，你经常需要生成来自两个集合的元素的所有可能组合，例如从主食和配菜列表中生成所有套餐组合、从日期和时间段集合中生成所有日程时间槽，或者从浏览器和屏幕分辨率中生成所有测试配置。
在 SQL 中，这就是 **CROSS JOIN**。
在 LINQ 中，用于完成此任务的工具是 `SelectMany`。

### 工作原理

`SelectMany` 遍历**外部**（outer）序列中的每个元素。
对于每个外部元素，它生成一个**内部**（inner）序列，然后将所有这些内部序列**展平**（flatten）为单个扁平的结果。
当你使用 `SelectMany` 将每个外部元素与每个内部元素配对时，就会得到**笛卡尔积**（Cartesian product），即所有可能的配对组合。

可以将其想象为嵌套循环：对于列表 A 中的每一项，遍历列表 B 中的每一项并生成一个配对。
但与其编写显式循环，不如使用 `SelectMany` 以声明式的方式表达这一过程。

### 语法

`SelectMany` 有多个重载。
用于笛卡尔积的最有用的重载接受两个参数：

```csharp
// 重载：集合选择器 + 结果选择器
outer.SelectMany(
    outerElement => innerSequence,                    // 为每个外部元素生成内部序列
    (outerElement, innerElement) => /* 将它们组合 */ // 把每个配对投影为结果
);
```

第一个 lambda 返回内部集合（它可以依赖于外部元素，也可以是一个固定的集合）。
第二个 lambda 接收外部和内部元素，并允许你定义输出的形态。

### 示例

```csharp
// 示例 1：所有主食与配菜的组合
string[] entrees = { "Burger", "Salad" };
string[] sides = { "Fries", "Soup" };

var combos = entrees.SelectMany(
    entree => sides,
    (entree, side) => $"{entree} with {side}"
);
// 结果："Burger with Fries", "Burger with Soup",
//       "Salad with Fries", "Salad with Soup"

// 示例 2：坐标网格
int[] rows = { 1, 2, 3 };
int[] cols = { 1, 2 };

var grid = rows.SelectMany(
    r => cols,
    (r, c) => $"({r},{c})"
);
// 结果："(1,1)", "(1,2)", "(2,1)", "(2,2)", "(3,1)", "(3,2)"

// 示例 3：测试矩阵
string[] browsers = { "Chrome", "Firefox" };
string[] resolutions = { "1080p", "4K" };

var tests = browsers.SelectMany(
    b => resolutions,
    (b, r) => $"{b}@{r}"
).OrderBy(t => t).ToArray();
// 结果：["Chrome@1080p", "Chrome@4K", "Firefox@1080p", "Firefox@4K"]
```

### 组合计数

配对的总数始终是 `outerCount × innerCount`。
2 种主食 × 2 种配菜 = 4 种套餐。
3 行 × 2 列 = 6 个坐标。
如果任一集合为空，则结果为空，因为没有可以配对的内容。

### 你的任务

编写一个方法，接收两个数组 `colors` 和 `sizes`，并以 `"Color-Size"` 格式的字符串形式返回**每种可能的颜色-尺寸组合**。
结果应为按**字母顺序**排序的 `string[]`。

例如，给定颜色 `["Red", "Blue"]` 和尺寸 `["S", "M"]`，所有配对为：Red-S, Red-M, Blue-S, Blue-M。
按字母顺序排序后，结果为：Blue-M, Blue-S, Red-M, Red-S。

### 方法签名

```csharp
public static string[] CrossJoin(string[] colors, string[] sizes)
```

### 预期结果

```css
CrossJoin(["Red", "Blue"], ["S", "M"]) -> ["Blue-M", "Blue-S", "Red-M", "Red-S"]
CrossJoin(["Black"], ["S", "M", "L"]) -> ["Black-L", "Black-M", "Black-S"]
CrossJoin([], ["S", "M"]) -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string[] CrossJoin(string[] colors, string[] sizes)
    {
        // 用 SelectMany 生成所有颜色与尺寸的组合，再按字母顺序排序
        return colors
            .SelectMany(c => sizes, (c, s) => $"{c}-{s}")
            .OrderBy(x => x)
            .ToArray();
    }
}
```
