### 集合操作总结：完整集合分析

在实际应用中，你经常需要比较两个数据集合，找出共有的内容、各自独有的内容，以及合并后的完整全貌。
比如比较来自不同营销活动的两个客户列表、来自不同仓库的两个库存清单，或者来自不同角色的两组权限。
LINQ 提供了三个强大的集合操作，让这种分析变得非常简单：`Union`、`Intersect` 和 `Except`。

### 它们的工作原理

这三个方法都在两个序列上操作，并根据集合论生成一个新序列：

- **Union** 合并两个序列并去除重复项。
  它回答的问题是：“跨两个集合的所有不同元素有哪些？”
- **Intersect** 仅返回在**两个**序列中都出现的元素。
  它回答的问题是：“这些集合有什么共同点？”
- **Except** 返回存在于第一个序列中但**不**存在于第二个序列中的元素。
  它回答的问题是：“这个集合独有的内容是什么？”

这三个方法都将单个集合内的重复项视为单个元素（它们都基于去重后的唯一值进行操作）。

### 语法

```csharp
// 这三个方法都遵循相同的模式：
IEnumerable<T> result = firstSequence.Operation(secondSequence);

// Union：两者中所有不重复的元素
var combined = sequenceA.Union(sequenceB);

// Intersect：仅共有的元素
var shared = sequenceA.Intersect(sequenceB);

// Except：在 A 中但不在 B 中的元素
var uniqueToA = sequenceA.Except(sequenceB);
```

### 示例

```csharp
// 比较两个团队的技能集合
string[] teamAlpha = { "C#", "Python", "SQL", "Azure" };
string[] teamBeta = { "Python", "JavaScript", "SQL", "AWS" };

var allSkills = teamAlpha.Union(teamBeta);
// { "C#", "Python", "SQL", "Azure", "JavaScript", "AWS" }，共 6 项技能

var commonSkills = teamAlpha.Intersect(teamBeta);
// { "Python", "SQL" }，2 项共有技能

var alphaOnly = teamAlpha.Except(teamBeta);
// { "C#", "Azure" }，2 项 Alpha 独有的技能

var betaOnly = teamBeta.Except(teamAlpha);
// { "JavaScript", "AWS" }，2 项 Beta 独有的技能
```

```csharp
// 处理单个集合内的重复项
int[] warehouse1 = { 10, 20, 20, 30 };
int[] warehouse2 = { 20, 30, 30, 40 };

var allProducts = warehouse1.Union(warehouse2);
// { 10, 20, 30, 40 }，两者之间的重复项都已移除

var sharedProducts = warehouse1.Intersect(warehouse2);
// { 20, 30 }

var onlyInWarehouse1 = warehouse1.Except(warehouse2);
// { 10 }
```

### 关键要点

| 关系 | 公式 |
| --- | --- |
| Union 计数 | OnlyInA + Intersection + OnlyInB |
| Except 具有方向性 | A.Except(B) ≠ B.Except(A) |
| 单个数组内的重复项 | 视为单个元素 |
| 空数组行为 | Union = 另一个数组的去重元素；Intersect = 空；Except = 非空数组的去重元素 |

### 你的任务

编写一个方法，对两个整数数组执行**完整集合分析**。
计算四个指标：

1. **Union**：两个数组中所有不重复元素的数量
2. **Intersection**：同时出现在两个数组中的元素数量
3. **OnlyInA**：存在于 `a` 中但不存在于 `b` 中的元素数量
4. **OnlyInB**：存在于 `b` 中但不存在于 `a` 中的元素数量

返回包含结果的格式化字符串。

思考如何处理单个数组内的重复项、数组之间没有共享元素时的情况、一个或两个数组为空时的情况，或者它们完全相同的情况。

### 方法签名

```csharp
public static string SetAnalysis(int[] a, int[] b)
```

### 预期结果

```rust
SetAnalysis([1, 2, 3, 4], [3, 4, 5, 6]) -> "Union: 6, Intersection: 2, OnlyInA: 2, OnlyInB: 2"
SetAnalysis([1, 2, 3], [4, 5, 6])       -> "Union: 6, Intersection: 0, OnlyInA: 3, OnlyInB: 3"
SetAnalysis([1, 1, 2, 2], [2, 2, 3, 3]) -> "Union: 3, Intersection: 1, OnlyInA: 1, OnlyInB: 1"
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static string SetAnalysis(int[] a, int[] b)
    {
        // 集合操作会自动去重，因此直接统计各结果的数量即可
        int union = a.Union(b).Count();
        int intersection = a.Intersect(b).Count();
        int onlyInA = a.Except(b).Count();
        int onlyInB = b.Except(a).Count();

        // 按要求的格式返回结果
        return $"Union: {union}, Intersection: {intersection}, OnlyInA: {onlyInA}, OnlyInB: {onlyInB}";
    }
}
```
