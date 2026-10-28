售票窗口只有在至少服务了一位顾客后，才能计算其平均等待时间。
顾客数量为零的情况必须返回 false，且不能尝试除以零。

逻辑与 `&&` 将两个操作数合并为一个 bool 表达式，并且仅在两个操作数都为 true 时才为 true。
逻辑或 `||` 在任一操作数为 true 时即为 true。
两者都采用自左向右的短路求值。
对于 `&&`，若左侧操作数为 false，则已决定整个结果，因此会跳过右侧操作数。
对于 `||`，若左侧操作数为 true，则已决定结果并跳过其右侧操作数。

这种求值顺序使得设置保护条件（guard）成为可能。
将 `served` 为正数的测试放在 `&&` 的左侧。
如果它为 false，右侧的除法将永远不会执行。
如果它为 true，则将整数商 `total_seconds / served` 与 `limit_seconds` 进行比较，允许平均值等于上限。

声明的输入范围为 `total_seconds`、`served` 和 `limit_seconds` 分别赋予 0 到 2147483647 之间的值。
服务人数为零是保护条件唯一需要拒绝的除数，而服务了一位顾客是它允许通过的最小数量，因此其边界位于这两个数量之间，而不是某个更大的数字。

将 `average_wait_ok` 实现为一个返回的 bool 表达式，并将保护条件放在前面。
强制使用的 token 规则要求使用 `&&`。
对于 `(240, 4, 90)` 返回 true，对于 `(600, 4, 90)` 返回 false，对于 `(500, 0, 90)` 在不进行除法的情况下返回 false，对于 `(85, 1, 90)` 返回 true，对于 `(180, 2, 90)` 返回 true。

### 解答

```c
#include <stdbool.h>

// 只有服务过至少一位顾客后，平均值才存在
bool average_wait_ok(int total_seconds, int served, int limit_seconds) {
    // 保护条件放在 && 左侧，served 为 0 时跳过除法
    return served > 0 && total_seconds / served <= limit_seconds;
}
```
