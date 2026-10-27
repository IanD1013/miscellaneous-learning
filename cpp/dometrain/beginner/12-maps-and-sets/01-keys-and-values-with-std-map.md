在 `std::map` 中，每个键（key）对应一个值（value），尖括号中的两个类型名称分别指明了它们各自的类型：

```cpp
#include <map>
#include <string>

std::map<std::string, int> counts;
counts["ana"] = 10;
counts["bo"] = 20;
counts["ana"] = 30;
```

`std::map<std::string, int>` 声明了一个 map，其键为 string，值为 int：键类型在前，值类型在后。
该类型由 `#include <map>` 引入，这是一个独立的头文件，起始代码中已经包含了它。

通过 `counts[key]` 进行赋值，要么会创建该条目，要么会替换该键下已有的值，因此上述三条语句最终会留下两个条目：`ana` 对应 30，`bo` 对应 20。
`counts.size()` 返回的是条目数，而不是赋值操作的次数，无论如何进行赋值，同一个键都不会出现两次。

读取操作存在一个副作用，在依赖它之前了解这一点非常重要。
当使用下标访问 map 中不存在的键时，map 会插入该键，并赋予其类型的默认构造值（对于 `int` 为 0，对于 `std::string` 为空字符串），然后返回该值的引用。
因此，`counts["zed"]` 会返回 0，并留下三个条目。
读取操作会使 map 变大，之后获取的任何大小都会包含这个从未被显式存储过的键。

`entriesAndProbedValue` 接收 `const std::vector<std::string> &keys`、`const std::vector<int> &values` 和 `const std::string &probe`。
它返回一个包含两个 int 的 `std::vector<int>`：读取 `probe` 后 map 中包含的条目数，以及该读取操作产生的值。
使用同一个索引遍历这两个 vector，将 `values[i]` 赋值给 `keys[i]`，读取一次 `probe` 并存入变量中，然后获取 map 的大小。
如果在读取之前获取大小，就会遗漏读取操作所创建的条目。
在构建 map 之前，如果传入的两个 vector 包含的元素数量不同，应直接拒绝并返回一个完全没有任何元素的 vector（因为有效答案绝不会是这种形式）。
一对空 vector 也是合法输入：对其进行探测会返回 1 个条目且值为 0。
你的代码中必须包含 `std::map<`，且 `.count(` 和 `.find(` 均已被禁用。

## 解答

```cpp
#include <cstddef>
#include <map>
#include <string>
#include <vector>

struct Solution {
    static std::vector<int> entriesAndProbedValue(const std::vector<std::string> &keys, const std::vector<int> &values, const std::string &probe) {
        std::vector<int> report;
        // 两个 vector 长度不同时直接返回空结果
        if (keys.size() != values.size()) {
            return report;
        }
        // 用两个 vector 构建 map，读取 probe 后再报告条目数和读到的值
        std::map<std::string, int> scores;
        for (std::size_t i = 0; i < keys.size(); ++i) {
            scores[keys[i]] = values[i];
        }
        int probed = scores[probe];
        report.push_back(static_cast<int>(scores.size()));
        report.push_back(probed);
        return report;
    }
};
```
