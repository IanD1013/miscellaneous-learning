当位置 `i` 在两个 vector 中表示相同的含义时，可以使用单个索引同时遍历它们：

```cpp
std::vector<int> a = {1, 2, 3};
std::vector<int> b = {10, 20, 30};

std::vector<int> result;
for (std::size_t i = 0; i < a.size(); i += 1) {
    result.push_back(a[i] + b[i]);
}
```

单个索引能保证配对的精确性。
两个独立的计数器一旦出现一个递增而另一个没有递增的情况就会错位；而基于范围的 for 循环（range-based for）无法胜任这项工作，因为它只提供元素而没有关联它们的位置。
这是对两个 vector 的单次遍历，而不是嵌套循环：`i` 在每个位置移动一次，两个下标也随之移动。

请注意循环条件所证明的内容。
它只将 `i` 与 `a.size()` 进行检查，对 `b` 则没有任何检查，因此第二个下标处于未检查状态。
在读取含有元素的 vector 时，发生越界读取会返回一个数字而不是报错，这意味着在未对大小不匹配进行防护的情况下运行，会产生一个看似合理但毫无报错标记的结果。
因此在读取任何元素之前，需要先比较大小。
此时 `result` 仍然为空，直接返回它即可返回空结果：

```cpp
if (a.size() != b.size()) {
    return result;
}
```

大小是调用的属性，应在开头一次性确定，而不是在每个下标处单独处理。
比较放置的位置会被评测：如果放在循环下方，它返回的 `result` 已经被循环填充，因此对于 `{3, 3}` 和 `{1, 1, 1, 1}`，它会返回两个求和结果，而本应不返回任何内容。

仅靠空结果无法完整说明情况：两个匹配的空 vector 组合后同样没有元素，但这是一个正确的结果而不是拒绝处理。
因此，该比较本身是一个独立评测的函数，需要区分这两种情况的调用者可以调用它。

- `sizesMatch` 接收 `const std::vector<int> &left` 和 `const std::vector<int> &right` 并返回一个 `bool`：当两者包含相同数量的元素时（包括两个 vector 均为空的情况）返回 `true`，当数量不同时返回 `false`。
- `sumAtEachPosition` 接收相同的两个参数，并返回一个 `std::vector<int>`，其中每个位置包含对应位置元素的和。
- 在 `sumAtEachPosition` 内部，在执行任何下标操作之前比较大小，并在大小不同时返回空 vector；此处应使用 `sizesMatch`。
- 两个函数都会针对各自的用例进行评测，因此都需要编写实际的函数体，且不得出现 `transform` 或 `std::transform`。

## 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    static bool sizesMatch(const std::vector<int> &left, const std::vector<int> &right) {
        // 判断两个 vector 的元素数量是否相同
        return left.size() == right.size();
    }

    static std::vector<int> sumAtEachPosition(const std::vector<int> &left, const std::vector<int> &right) {
        std::vector<int> result;
        // 先调用 sizesMatch，再用同一个索引遍历两个 vector
        if (!sizesMatch(left, right)) {
            return result;
        }
        for (std::size_t i = 0; i < left.size(); i += 1) {
            result.push_back(left[i] + right[i]);
        }
        return result;
    }
};
```
