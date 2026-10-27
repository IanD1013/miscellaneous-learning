`std::unique` 会将每一段连续重复的元素折叠为其第一个元素，但它无法缩小 vector：它接收到的仅仅是你传入的两个迭代器。

```cpp
std::vector<int> values{4, 4, 7, 7, 7, 4};
auto newEnd = std::unique(values.begin(), values.end());
```

它会遍历该区间一次，并将保留的每个元素向前移动以覆盖空隙，因此 `values` 现在以 4, 7, 4 开头。
`newEnd` 指向索引 3，即最后一个保留元素的下一个位置：该位置是新的逻辑终点。
`values.size()` 仍然是 6，并且从 `newEnd` 到 `end()` 的这三个元素是有效但未指定（unspecified）的。
没有任何保证它们会保留被丢弃的 4 和 7，因此切勿依赖它们。

从 `newEnd` 到 `values.end()` 与其他区间一样是一个左闭右开区间，而擦除（erase）它才是缩小 vector 的操作：

```cpp
values.erase(newEnd, values.end());
```

`values` 现在是 {4, 7, 4}。
如果不调用 `erase`，它仍然包含六个元素。

最后一个 4 之所以得以保留，是因为 `std::unique` 只会将每个元素与其紧挨着的前一个元素进行比较。
要移除无论位于何处的每一个重复项，请先对其进行排序，使相等的值相邻；这样处理的结果会按升序排列，而不是按输入顺序排列。
是否需要保留输入顺序决定了你应当编写这两种方法中的哪一种。

`std::remove_if` 后跟 `erase`（即你用来过滤 vector 的惯用法）的工作方式相同：它会按顺序将谓词返回 `false` 的元素移到前面，返回新的逻辑终点，并且不会删除任何内容。

### 需要编写的内容

每个函数都按值接收 `values` 并修改其自身的副本。
请使用 `std::unique` 移除重复项，而不是手写循环。

- `collapseRuns` 移除相邻的重复项并保持输入顺序。
  对于空 vector，它返回 []。
- `distinctSorted` 按升序返回每个值一次。
  先尝试不进行排序：对于 [3, 1, 3, 2, 1]，你预期会得到什么？
  运行结果会表明你的预期是否正确。
- `duplicatesRemoved` 返回 `distinctSorted` 中的去重操作移除了多少个元素：即去重前的大小减去去重后的大小。
  对于 {5, 5, 8, 5, 8}，它返回 3。
  排序后得到 {5, 5, 5, 8, 8}，去重后只剩下 [5, 8]，因此移除了三个元素，尽管只有两个值发生重复。

### 解答

```cpp
#include <algorithm>
#include <vector>

struct Solution {
    static std::vector<int> collapseRuns(std::vector<int> values) {
        // unique 只折叠相邻重复项，再用 erase 缩小 vector
        values.erase(std::unique(values.begin(), values.end()), values.end());
        return values;
    }

    static std::vector<int> distinctSorted(std::vector<int> values) {
        // 先排序让相等的值相邻
        std::sort(values.begin(), values.end());
        values.erase(std::unique(values.begin(), values.end()), values.end());
        return values;
    }

    static int duplicatesRemoved(std::vector<int> values) {
        int before = static_cast<int>(values.size());
        int after = static_cast<int>(distinctSorted(values).size());
        return before - after;
    }
};
```
