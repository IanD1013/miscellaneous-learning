计数回答了“有多少”，排名回答了“有哪些”，两者是对不同形态数据的独立遍历。
`std::map` 按键（key）升序遍历，因此计数本身绝不能直接作为排名。

固定的 `entry.hpp` 承载了存储每个不同单词的数据结构：

```cpp
struct Entry {
    std::string word;
    int count;
    int firstIndex;
};
```

该文件不可编辑，因此这三个成员就是排序所需依据的全部内容。
遍历一遍 `values` 即可填充一个 `std::map<std::string, Entry>`。
首次遇到某个单词时，在 map 中放入一个 `Entry`，包含该单词、初始计数值 0 以及它出现的索引位置；在每次遇到该单词时（包括第一次），都使用 `++` 增加 `count`。
如果在后续遇到时再次写入 `firstIndex`，它就会变成最后出现的位置，从而颠倒任何依赖它的配对顺序。

map 无法重新排序，因此将其值复制到一个扁平的 `Entry` vector 中并对其进行排序。
只需一个比较函数即可确定所有配对的关系：

```cpp
std::sort(entries.begin(), entries.end(), [](const Entry &a, const Entry &b) {
    if (a.word != b.word) {
        return a.word < b.word;
    }
    return a.firstIndex < b.firstIndex;
});
```

你的实现需要采用这种形式，但使用不同的成员变量：先比较 `a.count` 与 `b.count`，将较大的计数排在前面，当计数相同时，再由较小的 `a.firstIndex` 决定顺序。
对于比较结果为相等的两个元素，`std::sort` 不保证任何相对顺序，因此比较逻辑中未决定的平局将由算法决定而非契约保证，其顺序将无法预测。

### 要求

- `rankByCount` 根据 `const std::vector<std::string> &values` 和一个 `int topCount` 计算并返回一个包含单词的 `std::vector<std::string>`。
  评分程序会比较数字、字符串和扁平 vector，因此计数保留在 map 中即可。
- 按 `count` 降序排名（最高者排在最前），若出现平局则按较早的 `firstIndex` 决出先后。
- 单词采用精确匹配：`Ant` 和 `ant` 是两个不同的单词，各自具有独立的计数。
- 若 `topCount` 小于或等于 0，则返回空内容；若 `values` 为空，同样返回空内容。
  请在执行其他所有操作之前优先单独处理该情况：小于 0 的 `int` 转换为索引所用的无符号类型后会变成一个极大的数字而不是较小的数字，因此根据 vector 大小进行截断可能会静默返回整个排名。
- 若 `topCount` 大于不同单词的数量，则返回所有不同的单词；因此在通过索引访问已排序的 vector 之前，请将其截断为该 vector 的大小。
- 代码中需要使用 `std::map<` 进行计数，并使用 `std::sort(` 进行排序，这两者都会被检测。
  此外，以下三项被禁止使用：`unordered_map`、`std::count` 以及自定义的 `main` 函数，因为运行器会提供调用 `rankByCount` 的入口。

### 解答

```cpp
#include "entry.hpp"

#include <algorithm>
#include <cstddef>
#include <map>
#include <string>
#include <vector>

struct Solution {
    static std::vector<std::string> rankByCount(const std::vector<std::string> &values, int topCount) {
        // 计数，把条目复制到扁平 vector，用一个比较函数排序，再取前 topCount 个
        std::vector<std::string> ranked;
        if (topCount <= 0 || values.empty()) {
            return ranked;
        }

        std::map<std::string, Entry> tally;
        for (std::size_t i = 0; i < values.size(); i++) {
            if (tally.find(values[i]) == tally.end()) {
                tally[values[i]] = Entry{values[i], 0, static_cast<int>(i)};
            }
            ++tally[values[i]].count;
        }

        std::vector<Entry> entries;
        for (const auto &pair : tally) {
            entries.push_back(pair.second);
        }

        std::sort(entries.begin(), entries.end(), [](const Entry &a, const Entry &b) {
            if (a.count != b.count) {
                return a.count > b.count;
            }
            return a.firstIndex < b.firstIndex;
        });

        std::size_t limit = static_cast<std::size_t>(topCount);
        if (limit > entries.size()) {
            limit = entries.size();
        }
        for (std::size_t i = 0; i < limit; i++) {
            ranked.push_back(entries[i].word);
        }
        return ranked;
    }
};
```
