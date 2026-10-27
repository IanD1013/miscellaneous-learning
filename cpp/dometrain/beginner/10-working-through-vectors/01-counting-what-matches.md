计数器和累加求和在循环中看起来很相似，但回答的问题却不同。
计数器在循环之前声明并从 0 开始，内部的条件决定要对哪些元素进行计数，每个符合条件的元素都会使其加 1，无论该元素的值有多大：

```cpp
std::vector<int> v = {4, 7, 4, 2};

int matches = 0;
for (std::size_t i = 0; i < v.size(); i += 1) {
    if (v[i] == 4) {
        ++matches;
    }
}
```

`matches` 的最终值为 2，即等于 4 的元素个数，而 4 本身的值从未加到其中。
如果将 `++matches` 替换为 `matches += v[i]`，相同的循环就会得出 8，即匹配元素的值的总和，而不是计数。
`v[i]` 仅在 `i < v.size()` 时被读取，这是对 vector 进行每次下标访问所需的边界保证。

在循环外部声明计数器，与循环体对其进行的操作同样重要。
在循环体内声明的计数器会在每次遍历时重新创建并丢失之前的所有累加，因此它的结果只能是 1 或 0。

从 0 开始还能在无需额外分支的情况下处理特殊输入。
没有任何元素满足条件的 vector 最终结果为 0，而完全没有元素的 vector 则根本不会进入循环体，结果同样为 0。
两者都不是拒绝回答；而是有零个元素通过条件，因此计数为零。

- `countAbove` 接收 `const std::vector<int> &numbers` 和一个 `int limit`，并返回一个 `int`。
- 对严格大于 `limit` 的每个元素计数加一。
  等于 `limit` 的元素不算作大于它，因此不计入。
- 空 vector 以及没有任何元素大于 `limit` 的 vector 均返回 0。
- 评测只会检查返回值，因此打印输出没有任何作用。
- 使用 `numbers.size()` 限制循环边界，并且不要使用 `std::count`、`std::count_if` 以及 `count_if`：本练习考查的是手动计数。

## 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    static int countAbove(const std::vector<int> &numbers, int limit) {
        // 每遇到一个大于 limit 的元素就计数加一，而不是累加元素的值
        int matches = 0;
        for (std::size_t i = 0; i < numbers.size(); i += 1) {
            if (numbers[i] > limit) {
                ++matches;
            }
        }
        return matches;
    }
};
```
