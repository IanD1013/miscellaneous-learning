A `std::map` 无法直接返回给评分系统（grader）。
评分系统能够比对的是数字、布尔值、字符、字符串，或者由数字、字符或字符串构成的一维 vector，它会拒绝其他所有类型：map、set、vector of vectors，以及列表中令人意外的一员：`std::vector<bool>`。
单个 `bool` 可以完全正常地返回；但它们的 vector 却不行。
程序仍然会成功运行，编译器也不会报错。
然而每个测试用例都会失败并返回空结果，同时提示返回类型无法比较。
因此，对于容器形态的答案，最后一步就是将其转换为评分系统能够识别的形态。

```cpp
std::map<std::string, int> counts;
counts["fig"] = 1;
counts["pear"] = 3;

std::vector<std::string> report;
for (const auto &[word, count] : counts) {
    report.push_back(word + "=" + std::to_string(count));
}
// report 依次保存 "fig=1" 和 "pear=3"
```

一个条目会变成一个 `std::string`，并且通过一次 `push_back` 将其添加到 `std::vector<std::string>` 的末尾，评分系统会对该 vector 逐个元素进行比对，并在打印字符串元素时加上引号。
`std::to_string(count)` 会将数字转换为字符。
`std::string` 无法直接加上 `int`，因此 `word + "=" + count` 永远无法编译，这种转换必须由你显式编写，而不会自动隐式发生。
这两个调用都必须出现在你的答案中：`push_back(` 和 `std::to_string(`。

元素的顺序就是遍历的顺序，而 map 按照键的升序进行遍历，因此答案自然按单词排好序，无需在此进行任何排序，并且禁用了 `std::sort` 以保持这种机制。

### 元素文本

`reportWordCounts(const std::vector<std::string> &words, int minCount)` 返回一个按上文 `report` 的方式构建的 `std::vector<std::string>`。
在 `std::map<`（本题规则明确要求按名称使用）中统计单词频次，然后遍历统计结果，为每个频次至少为 `minCount` 的单词 push 一个元素。
每个元素均为单词紧跟 `=` 再紧跟频次，中间不含任何空格：`apple=2`。
使用 `>=` 进行比较，并通过跳过 push 来排除单词，而不是先构建元素再将其移除。

如果没有传入任何单词，答案不包含任何元素；如果 `minCount` 高于所有频次，也会返回同样的结果。
`minCount` 小于或等于 0 时会保留所有单词，因为进入 map 的单词频次至少为 1。
10 及以上的计数也在取值范围内，`std::to_string` 会写入所有数字位数。

### 解答

```cpp
#include <map>
#include <string>
#include <vector>

struct Solution {
    static std::vector<std::string> reportWordCounts(const std::vector<std::string> &words, int minCount) {
        std::vector<std::string> report;
        // 用 map 统计单词频次，再为每个达到 minCount 的单词添加一个 word=count 元素
        std::map<std::string, int> counts;
        for (const std::string &word : words) {
            ++counts[word];
        }
        for (const auto &[word, count] : counts) {
            if (count >= minCount) {
                report.push_back(word + "=" + std::to_string(count));
            }
        }
        return report;
    }
};
```
