### 在 LINQ 中链式调用多个 Where

当你面对复杂的过滤逻辑时，很容易倾向于使用 `&&` 将所有条件塞进单个 `Where` 谓词中。
虽然这种方式可行，但 LINQ 允许你在管道中**链式调用多个 `Where`**，使每个调用专注于处理一个过滤关注点。
这能保持每个步骤目标明确、清晰易读且更易于维护，尤其是在过滤逻辑变得越来越复杂时。

### 工作原理

当你链式调用两个 `Where` 时，第一个 `Where` 会生成一个中间序列，其中仅包含通过其谓词测试的元素。
然后，第二个 `Where` 会进一步过滤*该*中间序列。
最终结果与在单个 `Where` 中使用 `&&` 组合两个谓词完全相同，但管道风格将每个逻辑关注点分离到了独立的步骤中。

可以把它想象成一系列筛子：每个筛子筛选不同的东西，只有通过*所有*筛子的项才能到达最后。

### 语法

```csharp
// 使用组合谓词的单个 Where：
source.Where(x => conditionA(x) && conditionB(x))

// 等价的链式 Where 调用：
source
    .Where(x => conditionA(x))
    .Where(x => conditionB(x))
```

两者产生相同的结果。
当每个条件代表一个独立的过滤关注点时，推荐使用链式调用的版本。

### 示例

```csharp
// 示例 1：过滤处于活跃状态并且属于工程部门的员工
string[] departments = { "Engineering", "Sales", "HR" };
bool[] active = { true, false, true };

var result = employees
    .Where(e => e.IsActive)        // 第 1 步：只保留活跃员工
    .Where(e => e.Department == "Engineering");  // 第 2 步：只保留工程师

// 示例 2：过滤非空并且以大写字母开头的字符串
string[] words = { "Hello", "", "world", "LINQ", "" };

var filtered = words
    .Where(w => w.Length > 0)              // 第 1 步：移除空字符串
    .Where(w => char.IsUpper(w[0]));       // 第 2 步：以大写字母开头
// 结果: ["Hello", "LINQ"]

// 示例 3：过滤高于阈值并且能被 5 整除的分数
int[] scores = { 10, 23, 45, 67, 80, 55 };

var topRound = scores
    .Where(s => s >= 50)           // 第 1 步：至少为 50
    .Where(s => s % 5 == 0);       // 第 2 步：能被 5 整除
// 结果: [80, 55]
```

### 常见模式

- **分离领域关注点**：一个 `Where` 用于有效性检查，另一个用于业务规则
- **条件化构建管道**：你可以通过编程方式决定是否添加某个 `Where` 步骤
- **调试**：相比于复合谓词内部，在链式调用之间插入断点或日志更容易

### 实用参考

| 运算符 / 概念 | 描述 | 示例 |
| --- | --- | --- |
| `Where(predicate)` | 过滤符合谓词条件的元素 | `.Where(x => x > 0)` |
| `% 2 == 0` | 检查数字是否为偶数 | `4 % 2 == 0` → `true` |
| `> 0` | 检查数字是否为正数 | `3 > 0` → `true` |
| `.ToArray()` | 将 LINQ 序列转换为数组 | `.Where(...).ToArray()` |

### 你的任务

编写一个方法，接收一个整数数组，并返回一个仅包含**既是正数又是偶数**的数字的新数组。
你必须使用**两个独立的链式 `Where` 调用**（每个条件对应一个），而不是单个复合谓词。
最后将最终结果转换为数组。

### 方法签名

```csharp
public static int[] FilterPositiveEvens(int[] numbers)
```

### 预期结果

```scss
FilterPositiveEvens([-2, 1, 2, 3, 4, -4]) -> [2, 4]
FilterPositiveEvens([0, -1, -2, 6, 8])    -> [6, 8]
FilterPositiveEvens([-3, -5, -7])          -> []
```

### 解答

```csharp
using System;
using System.Linq;

public class Solution
{
    public static int[] FilterPositiveEvens(int[] numbers)
    {
        return numbers
            .Where(n => n > 0)        // 第 1 步：只保留正数
            .Where(n => n % 2 == 0)   // 第 2 步：只保留偶数
            .ToArray();
    }
}
```
