比较操作接受两个值并生成一个 `bool`，这意味着其结果可以存储在变量中、从函数返回，或直接放入条件语句中：

```cpp
int count = 7;
int limit = 7;
bool same    = count == limit;   // true
bool differs = count != limit;   // false
bool under   = count < limit;    // false
bool atMost  = count <= limit;   // true
```

`==` 用于判断是否相同，而 `!=` 用于判断是否不同。
`<`、`<=`、`>` 和 `>=` 用于比较两个值的大小顺序，其中带有等号的两种形式将边界值本身也算作匹配。
单个 `=` 则完全是另一回事：它是赋值。
如果写在条件语句中，`if (left = right)` 会将 `right` 复制到 `left` 中并测试该副本，编译器对此只会给出警告而不会报错，因此程序会继续运行，而条件语句读取的是被复制的值。

### 对 double 而言，判断“完全相同”是错误的做法

`double` 存储的是二进制浮点数，因此 0.1 是以该形式所能表示的最接近的值来存储的，而不是精确的十分之一。
将两个这样的近似值相加，其总和会与十进制结果存在微小偏差：

```cpp
#include <cmath>

double sum = 0.1 + 0.2;
bool exact  = sum == 0.3;                       // false
bool within = std::abs(sum - 0.3) <= 0.000001;  // true
```

因此，比较 double 时应该通过距离（差值）来进行。
将两者相减，把差值传递给 `std::abs`（这样无论和是偏小还是偏大，都能一视同仁），然后测试该距离是否在你愿意接受的容差范围内。
`std::abs` 来自 `<cmath>`，该头文件中的版本接受一个 `double` 并返回一个 `double`，保留小数部分；而仅适用于整数的 `abs` 会将 0.5 的差值截断为 0，从而误报匹配。

完成 `sumMatchesWithin(double left, double right, double target, double tolerance)`，当 `left + right` 与 `target` 的差距在 `tolerance` 范围内时返回 `true`，否则返回 `false`。
差值恰好等于 `tolerance` 也算作匹配，因此最终的比较使用 `<=`。
调用者传入的 `tolerance` 为大于或等于零的值；在容差为零时，只有在二进制下精确命中 `target` 的和才会返回 `true`。
初始代码中已包含 `<cmath>` 并为你计算了原始差值，该 include 必须保留在文件中：它在编译前就会被检查，因此即使其余代码正确，删除了该 include 的提交也会被拒绝。

### 解答

```cpp
#include <cmath>

struct Solution {
    static bool sumMatchesWithin(double left, double right, double target, double tolerance) {
        // 比较 left + right 与 target 之间的距离和 tolerance，而不是直接比较两个值
        double difference = left + right - target;
        return std::abs(difference) <= tolerance;
    }
};
```
