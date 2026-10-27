二分查找（binary search）通过将目标值与范围的中间元素进行比较，并仅保留可能包含该值的那一半来查找值。
每次比较都会将剩余部分减半，因此对于一百万个元素，二分查找仅需约 20 次比较，而 `std::find` 可能需要遍历全部一百万个元素。

只有当范围已经按照查找所用的相同 `<` 排序时，这种折半查找才是正确的。
保持排序是二分查找的前置条件（precondition）：调用者在调用前确保为真的条件，函数依赖该条件且从不进行检查。
破坏标准库算法的前置条件会导致未定义行为（undefined behavior）。
在实践中，对未排序的 vector 执行二分查找仍会返回某些结果，但该结果毫无意义：它可能会报告 vector 中实际存在的值不存在。

`<algorithm>` 提供了一个返回 yes 或 no 的二分查找，以及一个用于检查前置条件的函数：

- 当左闭右开区间包含等于 `value` 的元素时，`std::binary_search(first, last, value)` 返回 `true`。
- 当没有元素小于其前一个元素时，`std::is_sorted(first, last)` 返回 `true`，因此相等的相邻元素是合法的，空范围也被视为已排序。
  为了返回 `true`，它必须读取每一个元素，而这正是二分查找旨在避免的全量遍历。
  当接收到不可信的 vector 时检查一次，在此之后的查找就可以依赖该前置条件。

### `std::lower_bound` 和 `std::upper_bound`

`std::lower_bound(first, last, value)` 返回指向第一个不小于 `value` 的元素的迭代器。
`std::upper_bound` 接受相同的参数，并返回指向第一个大于 `value` 的元素的迭代器：

```cpp
std::vector<int> values{2, 4, 4, 7};
auto low = std::lower_bound(values.begin(), values.end(), 4);
auto high = std::upper_bound(values.begin(), values.end(), 4);
```

`low - values.begin()` 是 1，即第一个 4。
`high - values.begin()` 是 3：`upper_bound` 不会停在最后一个 4，而是停在它后面的一个位置，即 7 上。
因此等于 4 的元素正好是从 `low` 到 `high` 的左闭右开区间，而 `high - low` 就是它们的数量，即 2。

同一 vector 上的另外两个值：

```text
值      lower_bound   upper_bound
5       索引 3        索引 3
9       end()         end()
```

该 vector 中没有 5，但 `lower_bound` 仍会落在某个元素上，即 7。
到达某个位置并不意味着该值存在。
两次调用落在同一个元素上，因此计数为 0。

`lower_bound` 返回的位置是插入点（insertion point）：在此处插入 `value` 可以保持 vector 的有序性，且位于已经与其相等的任何元素之前。
对于 9，每个元素都比它小，因此插入点是 `end()`，其索引为 `size()`。
缺失的值仍然有插入点，因此不存在“未找到”索引。

### 需要编写的内容

`sorted_search.cpp` 包含 `Solution` 的四个静态函数。
前三个函数将升序排列的 `sorted` 作为前置条件且不作检查。
每个函数都使用上述算法进行查找，而不是使用循环或 `std::count`：

- `contains(sorted, value)` 返回 `value` 是否在 `sorted` 中。
- `insertionIndex(sorted, value)` 返回使用 `std::lower_bound` 找到的插入点索引。
- `countEqual(sorted, value)` 返回有多少个元素等于 `value`，不存在时返回 0。

`insertSorted(sorted, value)` 接收一个不可信的 vector。
当该 vector 不是升序排列时，返回一个空的 vector；真正的插入不会产生空 vector，因为结果总是包含 `value`。
否则，它会在插入点插入 `value` 并返回该 vector。
空的输入是已排序的，因此 `insertSorted({}, 2)` 返回 `{2}`。
这个函数完全可以承受检查的开销：其插入操作本身就需要移动插入点之后的所有元素，这也是一次全量遍历。

### 解答

```cpp
#include <algorithm>
#include <vector>

struct Solution {
    static bool contains(const std::vector<int>& sorted, int value) {
        return std::binary_search(sorted.begin(), sorted.end(), value);
    }

    static int insertionIndex(const std::vector<int>& sorted, int value) {
        auto it = std::lower_bound(sorted.begin(), sorted.end(), value);
        return static_cast<int>(it - sorted.begin());
    }

    static int countEqual(const std::vector<int>& sorted, int value) {
        // 等于 value 的元素位于 [low, high) 区间
        auto low = std::lower_bound(sorted.begin(), sorted.end(), value);
        auto high = std::upper_bound(sorted.begin(), sorted.end(), value);
        return static_cast<int>(high - low);
    }

    static std::vector<int> insertSorted(std::vector<int> sorted, int value) {
        // 不可信输入，先检查前置条件
        if (!std::is_sorted(sorted.begin(), sorted.end())) {
            return {};
        }
        sorted.insert(std::lower_bound(sorted.begin(), sorted.end(), value), value);
        return sorted;
    }
};
```
