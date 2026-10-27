`std::find_if` 使用谓词（一个接受一个元素并返回 `bool` 的函数）搜索一个范围。
它按顺序依次检查元素，在谓词接受的第一个元素处停止，并返回指向该元素的迭代器。
要将该迭代器转换为索引，减去 `values.begin()` 即可：

```cpp
std::vector<int> values{7, -3, 2, -8};
auto it = std::find_if(values.begin(), values.end(), [](int v) { return v < 0; });
if (it != values.end()) {
    int index = static_cast<int>(it - values.begin());   // 1，即 -3
}
```

当谓词不接受任何元素时，`std::find_if` 会返回给定范围的末尾。
与 `std::find` 一样，`values.end()` 并不指向任何元素，因此在进行任何其他使用之前，都需要将 `it` 与 `values.end()` 进行比较。
跳过此比较且未找到匹配项时仍然会得出一个数字：`values.end() - values.begin()` 的结果是 `values.size()`，这是一个其后没有元素的索引。

### 搜索尾部

这两个迭代器构成一个半开区间 `[first, last)`：`first` 表示搜索的第一个元素，而 `last` 表示最后一个元素之后的位置。
传入 `values.begin() + from` 作为 `first`（即你在 `erase` 中使用过的相同的 `begin() + i` 形式），搜索就会涵盖从索引 `from` 开始的尾部：

```cpp
auto it = std::find_if(values.begin() + 2, values.end(), [](int v) { return v < 0; });
```

这会跳过 -3 并找到 -8。
`it` 仍然指向 `values` 内部，因此 `it - values.begin()` 为 3，即 -8 在 vector 中的索引。
减去 `values.begin() + 2` 则会得到 1，即从搜索起始位置算起的位置。

因为 `last` 是末尾之后的下一个位置，所以 `first == last` 的范围是一个空范围，它不需要其他标记。
`values.begin() + values.size()` 即为 `values.end()`，因此起始位置等于 `size()` 时不会搜索任何内容并返回 `values.end()`：这是一个没有匹配项的有效搜索。

小于 0 或大于 `size()` 的起始位置则不同。
`values.begin() + from` 会指向该 vector 并不存在的位置，即便没有任何代码去读取它，构造该迭代器也是未定义行为（undefined behavior）。
在编写 `values.begin() + from` 之前，请先根据 0 和 `values.size()` 检查 `from`。

### 范围上的“是”或“否”判断

还有三个算法像 `std::find_if` 一样接受一个范围和一个谓词，并返回 `bool`：

```cpp
std::any_of(first, last, pred)    // 存在通过的元素时为 true
std::all_of(first, last, pred)    // 没有未通过的元素时为 true
std::none_of(first, last, pred)   // 没有通过的元素时为 true
```

空范围中没有任何元素可以通过或未通过测试，因此 `all_of` 和 `none_of` 在此情况下返回 `true`，而 `any_of` 返回 `false`。

### 编写内容

在 `search.cpp` 中，当某个值大于 `limit` 时即为匹配；等于 `limit` 的值不算匹配。
每个谓词都是一个捕获 `limit` 的 lambda。
使用 `std::find_if` 进行搜索，并使用 `std::any_of`、`std::all_of` 和 `std::none_of` 计算各标志位。

- `firstIndexAbove(values, limit)` 返回第一个匹配项的索引，若不存在则返回 -1。
- `firstIndexAboveFrom(values, limit, from)` 搜索从索引 `from` 开始的尾部，并返回匹配项在整个 vector 中的索引。
  当尾部没有匹配项时返回 -1，当 `from` 为负数或大于 `values.size()` 时返回 -2。
- `rangeFacts(values, limit)` 返回针对同一测试的三个标志位（1 表示 true，0 表示 false），顺序依次为 any、all、none。

对于 `{9, 1, 9}`，当 limit 为 4 时，`firstIndexAboveFrom` 返回：

```text
from   搜索的尾部       返回值
0      9, 1, 9          0
1      1, 9             2
3      （空）           -1
4      无效起始位置     -2
-1     无效起始位置     -2
```

### 解答

```cpp
#include <algorithm>
#include <vector>

struct Solution {
    static int firstIndexAbove(const std::vector<int>& values, int limit) {
        auto it = std::find_if(values.begin(), values.end(), [limit](int v) { return v > limit; });
        // 未找到时返回 -1
        if (it == values.end()) {
            return -1;
        }
        return static_cast<int>(it - values.begin());
    }

    static int firstIndexAboveFrom(const std::vector<int>& values, int limit, int from) {
        // 先检查起始位置，避免构造越界迭代器
        if (from < 0 || from > static_cast<int>(values.size())) {
            return -2;
        }
        auto it = std::find_if(values.begin() + from, values.end(), [limit](int v) { return v > limit; });
        if (it == values.end()) {
            return -1;
        }
        // 索引从 vector 开头计算
        return static_cast<int>(it - values.begin());
    }

    static std::vector<int> rangeFacts(const std::vector<int>& values, int limit) {
        auto above = [limit](int v) { return v > limit; };
        int any = std::any_of(values.begin(), values.end(), above) ? 1 : 0;
        int all = std::all_of(values.begin(), values.end(), above) ? 1 : 0;
        int none = std::none_of(values.begin(), values.end(), above) ? 1 : 0;
        return {any, all, none};
    }
};
```
