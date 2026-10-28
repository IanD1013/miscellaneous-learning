### 自增和自减运算符

`++`（自增）和 `--`（自减）运算符用于使变量增加或减少 1。
它们有两种形式：**前缀（prefix）**和**后缀（postfix）**，在表达式中使用时表现不同。

### 后自增和后自减 (value++ / value--)

```csharp
int x = 5;
int result = x++;  // result = 5, x = 6（先返回原值，再修改）

int y = 10;
int result2 = y--; // result2 = 10, y = 9（先返回原值，再修改）
```

**后缀**版本会在做出修改之前返回**原始值**。

### 前自增和前自减 (++value / --value)

```csharp
int x = 5;
int result = ++x;  // result = 6, x = 6（先修改，再返回）

int y = 10;
int result2 = --y; // result2 = 9, y = 9（先修改，再返回）
```

**前缀**版本会**先**做出修改，然后返回新值。

### 关键区别总结

| 运算符 | 名称 | 行为 | 示例 (x=5) |
| --- | --- | --- | --- |
| `x++` | 后自增 (Post-increment) | 返回 x，然后加 1 | 返回 5，x 变为 6 |
| `++x` | 前自增 (Pre-increment) | 加 1，然后返回 x | 返回 6，x 变为 6 |
| `x--` | 后自减 (Post-decrement) | 返回 x，然后减 1 | 返回 5，x 变为 4 |
| `--x` | 前自减 (Pre-decrement) | 减 1，然后返回 x | 返回 4，x 变为 4 |

### 你的任务

实现四个方法来演示每种类型的自增/自减运算符：

- `PostIncrement(value)` - 使用 `value++` 并返回结果
- `PreIncrement(value)` - 使用 `++value` 并返回结果
- `PostDecrement(value)` - 使用 `value--` 并返回结果
- `PreDecrement(value)` - 使用 `--value` 并返回结果

### 方法签名

```csharp
public static int PostIncrement(int value)
public static int PreIncrement(int value)
public static int PostDecrement(int value)
public static int PreDecrement(int value)
```

### 预期结果

```
PostIncrement(5) -> 5   // 返回原始值
PreIncrement(5) -> 6    // 返回自增后的值
PostDecrement(10) -> 10 // 返回原始值
PreDecrement(10) -> 9   // 返回自减后的值
```

### 解答

```csharp
using System;

public class Solution
{
    // 后自增：返回原始值，然后自增
    public static int PostIncrement(int value)
    {
        return value++;
    }
    
    // 前自增：先自增，然后返回新值
    public static int PreIncrement(int value)
    {
        return ++value;
    }
    
    // 后自减：返回原始值，然后自减
    public static int PostDecrement(int value)
    {
        return value--;
    }
    
    // 前自减：先自减，然后返回新值
    public static int PreDecrement(int value)
    {
        return --value;
    }
}
```
