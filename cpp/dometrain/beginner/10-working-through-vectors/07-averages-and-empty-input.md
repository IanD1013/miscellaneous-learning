从 vector 计算平均值会遇到两个独立的问题，每一个都需要在代码中通过明确的决策来解决。
第一个问题是除法。
总和以 `int` 类型累加，而 `size()` 返回的是一个无符号计数（unsigned count），这种类型无法容纳负数。
将两者混用会在执行除法之前把总和转换为该无符号类型，因此 `total / numbers.size()` 是一个整数除法，其后果不仅仅是丢弃小数部分。

```cpp
int total = 9;
std::vector<int> v = {1, 2, 3, 3};

double truncated = total / v.size();                      // 2
double kept = static_cast<double>(total) / v.size();      // 2.25
```

当总和为 9 时，只是小数部分丢失了。
但当总和小于 0 时，结果将变得面目全非：-7 转换为 4 字节无符号计数后会变成一个略大于 40 亿的数字，将其除以 2 得到的结果会略大于 20 亿，而原本期望的结果是 -3.5。

`static_cast<double>` 应该作用于操作数上，且位于除法运算之前。
对其中一边进行类型拓宽会使整个除法变成浮点除法，从而保留小数部分。
如果写在计算完成的商外面，形如 `static_cast<double>(total / v.size())`，它拓宽的就是一个小数部分已经丢失的数字，这只会将 2 变成 2.0，而不是得到 2.25。

### 没有可计算平均值的元素

第二个问题是元素数量。
空 vector 的平均值是不存在的：没有总和可以分摊给零个元素，除法也没有可操作的对象。
因此，在累加和除法之前，首先需要检查 `numbers.empty()`。

此时返回的是调用者传入的值，即第二个参数 `absent`，原因在第 10.2 节中已经明确：任何 `double` 值都可以是某个 vector 的真实平均值（包括 0 在内），因此函数自己虚构的任何值都不能代表“缺失”。
这里的新特性是类型：`absent` 是作为 `double` 传入的，而每个元素都是 `int`，它会被原样返回，既不参与求和，也不参与除法。

- `averageOfOr(const std::vector<int> &numbers, double absent)` 返回一个 `double`。
- 如果存在元素，则返回它们的总和除以元素个数：`{1, 2, 3, 4}` 的平均值为 2.5，`{-5, -2}` 的平均值为 -3.5，单个元素的平均值就是它本身。
- 0 是一个真实的平均值，因此对于 `{-2, 2}` 且 `absent` 为 99 时，返回 0。
- 空 vector 不会执行任何除法运算：直接原样返回 `absent`。
- 防御条件中需要包含 `.empty()`；禁止使用 `accumulate` 和 `std::accumulate`，总和需要你自己累加计算。

### 解答

```cpp
#include <vector>

struct Solution {
    static double averageOfOr(const std::vector<int> &numbers, double absent) {
        // 先根据 numbers.empty() 决定是否返回 absent，再用总和除以元素个数
        if (numbers.empty()) {
            return absent;
        }
        int total = 0;
        for (int value : numbers) {
            total += value;
        }
        return static_cast<double>(total) / numbers.size();
    }
};
```
