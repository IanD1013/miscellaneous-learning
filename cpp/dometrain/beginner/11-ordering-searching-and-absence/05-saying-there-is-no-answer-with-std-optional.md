可能没有返回值的函数可以在其返回类型中明确表达这一点：

```cpp
#include <optional>
#include <vector>

std::optional<int> firstNegative(const std::vector<int> &values) {
    for (const int &value : values) {
        if (value < 0) {
            return value;
        }
    }
    return std::nullopt;
}
```

`std::optional<int>` 可以包含一个 `int` 或者什么都不包含。
返回一个 `int` 会填充它，`return std::nullopt;` 会让它保持为空，而且这种空结果绝不会与任何 `int` 混淆。
该类型通过 `#include <optional>` 引入，在使用该名称之前必须将其包含在文件中。
第 4.5 课曾通过保留一个与返回值同类型的值来处理函数无法处理的情况，而第 7.4 课将 `bool` 与调用者拥有的变量配对；optional 则不需要这些保留方案，因为“无值（nothing）”本身就已经与所有数字区分开来了。

调用者随后分两步操作：

```cpp
std::optional<int> result = firstNegative(values);
if (result.has_value()) {
    int answer = result.value();
}
```

`has_value()` 仅用于报告值是否存在：包含 0 的 optional 会报告 `true`，因为零也是一个正常的值。
`value()` 会返回内部的 `int`，并且它只能且必须位于条件测试为 `true` 的分支中。
对一个空的 optional 调用 `value()` 在当前引擎上会导致程序以退出代码 134 终止，产生空结果且没有任何提示信息，以至于事后无法进行任何检查。
因此，每次都必须先进行检查。

### 需求

- 已经为你声明了 `firstAbove`：它接收 `const std::vector<int> &values` 和一个 `int threshold`，并返回 `std::optional<int>`。
  返回严格大于 `threshold` 的第一个元素；当没有元素满足条件时返回 `std::nullopt`。
  等于 `threshold` 的值不符合条件，因此对于 `{6, 10}` 且 threshold 为 6，返回 10。
- `firstAboveOrFallback` 是用于评分的函数。
  它接收相同的 vector 和 threshold，外加一个 `int fallback`；调用 `firstAbove`，并在 `result.has_value()` 为 `true` 时返回 `result.value()`，否则返回 `fallback`。
  评分系统比对的是 `int`，这也是为什么 optional 仅保留在文件内部的原因。
- 取第一个符合条件的元素，而不是最大的元素：例如 `{3, 9, 12, 7}` 且 threshold 为 5 时，返回 9。
- `{-5, -2, 0, 4}` 且 threshold 为 -1 时返回 0。
  存储的 0 也是一个有效结果，如果辅助函数将其视为空值，则无法通过该测试用例。
- `{1, 2, 3}` 且 threshold 为 3 时返回 fallback，空 vector 也是如此，两种情况下都不应解包任何值。
- 保持两个步骤分开：在 `if` 中使用 `has_value()`，在其中调用 `.value()`，两者都必须出现。

### 解答

```cpp
#include <optional>
#include <vector>

struct Solution {
    static std::optional<int> firstAbove(const std::vector<int> &values, int threshold) {
        // 返回第一个大于阈值的元素，没有则返回空
        for (int value : values) {
            if (value > threshold) {
                return value;
            }
        }
        return std::nullopt;
    }


    static int firstAboveOrFallback(const std::vector<int> &values, int threshold, int fallback) {
        std::optional<int> result = firstAbove(values, threshold);
        // 先检查是否有值，有值才取出
        if (result.has_value()) {
            return result.value();
        }
        return fallback;
    }
};
```
