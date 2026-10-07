### 比较运算符

比较运算符用于比较两个值并返回一个布尔值（`true` 或 `false`）。
它们在代码中做条件决策时至关重要。

### 六种比较运算符

```csharp
// 相等：检查两个值是否相同
5 == 5   // true
5 == 3   // false

// 不相等：检查两个值是否不同
5 != 3   // true
5 != 5   // false

// 大于
10 > 5   // true
5 > 10   // false

// 小于
3 < 7    // true
7 < 3    // false

// 大于或等于
5 >= 5   // true（相等也算！）
6 >= 5   // true
4 >= 5   // false

// 小于或等于
5 <= 5   // true（相等也算！）
4 <= 5   // true
6 <= 5   // false
```

### 常见错误

```csharp
// 错误：单个 = 是赋值，而不是比较
int x = 5;
if (x = 3)  // 报错！这会尝试把 3 赋值给 x

// 正确：双等号 == 才是比较
if (x == 3) // 这会把 x 与 3 进行比较
```

### 运算符参考

| 运算符 | 名称 | 示例 | 结果 |
| --- | --- | --- | --- |
| `==` | 等于 | `5 == 5` | true |
| `!=` | 不等于 | `5 != 3` | true |
| `>` | 大于 | `7 > 5` | true |
| `<` | 小于 | `3 < 5` | true |
| `>=` | 大于或等于 | `5 >= 5` | true |
| `<=` | 小于或等于 | `5 <= 5` | true |

### 你的任务

实现六个方法，每个方法使用不同的比较运算符：

- `IsEqual(a, b)` - 使用 `==`，当 a 等于 b 时返回 true
- `IsNotEqual(a, b)` - 使用 `!=`，当 a 不等于 b 时返回 true
- `IsGreaterThan(a, b)` - 使用 `>`，当 a 大于 b 时返回 true
- `IsLessThan(a, b)` - 使用 `<`，当 a 小于 b 时返回 true
- `IsGreaterOrEqual(a, b)` - 使用 `>=`，当 a 大于或等于 b 时返回 true
- `IsLessOrEqual(a, b)` - 使用 `<=`，当 a 小于或等于 b 时返回 true

### 方法签名

```csharp
public static bool IsEqual(int a, int b)
public static bool IsNotEqual(int a, int b)
public static bool IsGreaterThan(int a, int b)
public static bool IsLessThan(int a, int b)
public static bool IsGreaterOrEqual(int a, int b)
public static bool IsLessOrEqual(int a, int b)
```

### 预期结果

```
IsEqual(5, 5) -> True
IsNotEqual(5, 3) -> True
IsGreaterThan(10, 5) -> True
IsLessThan(3, 7) -> True
IsGreaterOrEqual(8, 5) -> True
IsLessOrEqual(4, 9) -> True
```

### 解答

```csharp
using System;

public class Solution
{
    // a 等于 b 时返回 true
    public static bool IsEqual(int a, int b)
    {
        return a == b;
    }

    // a 不等于 b 时返回 true
    public static bool IsNotEqual(int a, int b)
    {
        return a != b;
    }

    // a 大于 b 时返回 true
    public static bool IsGreaterThan(int a, int b)
    {
        return a > b;
    }

    // a 小于 b 时返回 true
    public static bool IsLessThan(int a, int b)
    {
        return a < b;
    }

    // a 大于或等于 b 时返回 true
    public static bool IsGreaterOrEqual(int a, int b)
    {
        return a >= b;
    }

    // a 小于或等于 b 时返回 true
    public static bool IsLessOrEqual(int a, int b)
    {
        return a <= b;
    }
}
```
