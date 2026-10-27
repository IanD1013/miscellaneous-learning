比较长度的 comparator 无法区分 `"two"` 和 `"ten"`。
两者都不比对方短，因此排序将它们视为相等的元素，它们之间的任何相对顺序都算作已排序。
`std::sort` 对这种顺序不做任何保证：它会将所有 3 个字母的单词排在所有 4 个字母的单词之前，但可能会交换 3 个字母单词之间的相对顺序。
在此编辑器中使用 `std::sort` 按长度对这十个单词进行排序，你将得到：

```text
输入       ["four", "two", "one", "three", "six", "ten", "five", "nine", "seven", "zero"]
std::sort  ["ten", "two", "one", "six", "four", "five", "nine", "zero", "three", "seven"]
```

`"ten"` 原本是最后一个 3 字母单词，结果排在了最前面，而 4 字母和 5 字母单词则恰好保持了它们的输入顺序。
换成其他输入或另一个标准库实现，这些平局项的顺序可能会有所不同，因此一次 `std::sort` 保持了所有平局顺序的运行结果并不能代表下一次处理其他列表时也会如此。

当相等元素的输入顺序是结果要求的一部分时，请改用 `std::stable_sort`。
它接受相同的范围和 comparator，并保持相等元素原有的输入顺序，这正是排序算法“稳定”（stable）的含义。

```cpp
std::vector<int> v{31, 12, 35, 18, 30};
std::stable_sort(v.begin(), v.end(), [](int a, int b) { return a / 10 < b / 10; });
// v 为 {12, 18, 31, 35, 30}
```

该 comparator 仅比较十位数，因此 `35` 排在 `30` 前面只有一个原因：它在输入中出现得更早。

### 使用 std::partition 进行划分

`std::partition(first, last, pred)` 将谓词（predicate）接受的每个元素移动到它拒绝的每个元素之前，并返回指向两组之间边界的迭代器。

```cpp
std::vector<int> v{-4, 7, 0, 9, -1};
auto boundary = std::partition(v.begin(), v.end(), [](int x) { return x > 0; });
// v 现在为 {9, 7, 0, -4, -1}
```

边界迭代器指向被拒绝组的第一个元素（在此处是 `0`），如果所有元素都被接受，则为 `end()`；它绝不会指向最后一个被接受的元素。
因此，`[v.begin(), boundary)` 包含被接受的组，`[boundary, v.end())` 包含被拒绝的组，而 `boundary - v.begin()` 为 2，即被接受元素的数量。

仅通过交换 `-4` 和 `9` 就完成了这次划分，这使得 `9` 排在 `7` 前面，而 `-4` 排在 `0` 后面。
谓词决定了每个值归入哪一组，这一点是可靠的。
但每组内部的顺序是无法保证的，另一个标准库实现可能会得到不同的顺序。
`std::stable_partition(first, last, pred)` 执行相同的划分，并保持两组元素原有的输入顺序。

当下一步操作会确立自己的顺序时，`std::partition` 留下的顺序不会产生任何负面影响。
假设你需要将低于某个 limit 的值按升序排列。
如果对整个 vector 排序，还会对你即将丢弃的所有值进行排序。
先进行 partition，然后只对被接受的组进行排序。
排序决定了最终的顺序，因此 `std::partition` 在组内留下的任何顺序都不会显现，而使用 `std::stable_partition` 反而会白白耗费工作去保持一个马上就会被排序覆盖的输入顺序。

### 任务

填写 `ordering.cpp` 中的三个函数：

- `sortByLength(words)` 返回按长度从短到长排列的单词，长度相等的单词保持其输入顺序。
- `evensFirst(values)` 返回偶数值后跟奇数值，每组均保持其输入顺序。
  数值可以为负数，且零为偶数。
- `sortedBelow(values, limit)` 使用 `std::partition` 划分，以升序返回小于 `limit` 的值。
  等于 `limit` 的值将被排除，传入空 vector 则返回空 vector。

### 解答

```cpp
#include <algorithm>
#include <string>
#include <vector>

struct Solution {
    static std::vector<std::string> sortByLength(std::vector<std::string> words) {
        // 稳定排序，长度相等的单词保持输入顺序
        std::stable_sort(words.begin(), words.end(),
                         [](const std::string& a, const std::string& b) { return a.size() < b.size(); });
        return words;
    }

    static std::vector<int> evensFirst(std::vector<int> values) {
        // 负奇数 % 2 为 -1，因此判断是否等于 0
        std::stable_partition(values.begin(), values.end(), [](int v) { return v % 2 == 0; });
        return values;
    }

    static std::vector<int> sortedBelow(std::vector<int> values, int limit) {
        // 先划分，再只对被接受的组排序
        auto boundary = std::partition(values.begin(), values.end(), [limit](int v) { return v < limit; });
        values.erase(boundary, values.end());
        std::sort(values.begin(), values.end());
        return values;
    }
};
```
