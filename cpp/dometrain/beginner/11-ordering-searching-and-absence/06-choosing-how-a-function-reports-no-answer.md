读取调用者指定索引处存储的值可能会因三种情况而失败：负索引、超出最后一个元素的索引以及 vector 为空。
成功的返回值决定了适用哪种失败约定，这里有四种形式可供选择。

哨兵值会保留其自身返回值类型中的一个特定值来表示无答案，就像第 10.3 课中保留 -1 一样。
来自第 7.4 课的带有引用输出参数（out-parameter）的 `bool` 返回 `true` 或 `false`，并填充调用者持有的变量。
`std::optional<int>` 携带一个值或表示无值，且不保留任何特殊数字。
调用者传入的后备值（fallback）是第 11.5 课结尾所用的形式，它将决定权留给知晓缺失含义的代码。

### 哨兵值无可用数字的情况

这里的答案是 vector 中存储的任意值，并且每个 `int` 都是合法的：某个评分用例在被读取的索引处存储了 -1，另一个存储了 0。
哨兵值需要一个任何真实答案都不会取到的值，而这些数据没有留下任何这样的值：拿到 -1 的调用者无法区分存储的 -1 与失败。
出于这个原因，`-1` 被禁用：请使用 `index < 0` 拒绝过小的索引。

本文件包含其余三种形式。
没有函数签名说明函数拒绝哪些索引，因此该规则在下文中详细说明。

### 每个函数的返回值

- 一个由你自己命名的辅助函数，`static std::optional<int> yourName(const std::vector<int> &values, int index)`，当索引指向某个元素时返回存储的值，否则返回 `std::nullopt`。
- `static bool tryValueAt(const std::vector<int> &values, int index, int &found)` 仅在返回 `true` 时将元素写入 `found`，否则保持 `found` 原样不变。
- `askBothAt` 接收 vector 和一个 `int index`，并返回包含三个数字的 `std::vector<int>`：表示 optional 是否包含值的 1 或 0、表示 `tryValueAt` 返回值的 1 或 0，以及在两次调用前初始化为 4242 并在两次调用返回后读回的局部 `int`。
  在索引 1 处的 `{4, 9, 25}` 返回 `{1, 1, 9}`，而在索引 2 处的 `{4, 9}` 以及在索引 -1 处的 `{4, 9}` 均返回 `{0, 0, 4242}`。
- `valueAtOrFallback` 接收 vector、一个 `int index` 和一个 `int fallback`，并返回一个 `int`：存储的值，或者当索引未指向任何元素时返回 `fallback`。
  索引为 2 的 `{8, 3, -1}` 返回 -1，因为那里存储的就是 -1；`{4, 9}` 的索引 5 超出了末尾，而索引 -1 小于第一个元素，因此两者都返回 fallback，空 vector 的任何索引也是如此。
- `std::optional<int>`、`tryValueAt` 和 `has_value()` 均必须出现。
- 两个辅助函数以相同的方式拒绝索引：先获取一次 `const int count = static_cast<int>(values.size());`，然后根据 `index < 0 || index >= count` 拒绝。
  两边都保持 `int` 类型，被拒绝的索引绝不会到达方括号下标操作。

### 解答

```cpp
#include <optional>
#include <vector>

struct Solution {
    // 索引指向元素时返回该值，否则返回空
    static std::optional<int> valueAt(const std::vector<int> &values, int index) {
        const int count = static_cast<int>(values.size());
        if (index < 0 || index >= count) {
            return std::nullopt;
        }
        return values[index];
    }

    // 只有找到元素时才写入 found 并返回 true
    static bool tryValueAt(const std::vector<int> &values, int index, int &found) {
        const int count = static_cast<int>(values.size());
        if (index < 0 || index >= count) {
            return false;
        }
        found = values[index];
        return true;
    }

    static std::vector<int> askBothAt(const std::vector<int> &values, int index) {
        // 用 4242 初始化变量，分别询问两个辅助函数，报告三个数字
        int seed = 4242;
        std::optional<int> fromOptional = valueAt(values, index);
        bool fromBool = tryValueAt(values, index, seed);
        std::vector<int> report;
        report.push_back(fromOptional.has_value() ? 1 : 0);
        report.push_back(fromBool ? 1 : 0);
        report.push_back(seed);
        return report;
    }

    static int valueAtOrFallback(const std::vector<int> &values, int index, int fallback) {
        // 有值就返回存储的值，否则返回调用者给的 fallback
        std::optional<int> result = valueAt(values, index);
        if (result.has_value()) {
            return result.value();
        }
        return fallback;
    }
};
```
