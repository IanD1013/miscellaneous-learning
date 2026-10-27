对一个单词 vector 提出的三个问题有三个不同的答案，而且其中只有一个问题不需要为其构建容器。

统计每个单词意味着统计已经掌握的内容（包括重复项），因此 `words.size()` 就是全部答案，使用第二个容器只会徒劳地复制 vector。
统计不同的单词意味着丢弃重复项，而丢弃已持有的值正是向 set 插入元素的作用。
统计某个特定单词出现的次数意味着在每个单词旁边记录一个数字，只有 map 才有存放该数字的地方，因为 set 仅存储值本身。

因此由问题来决定。
选择 vector、set 还是 map 决定了答案能够表达的含义，而不是得出答案的速度，并且本课程并没有测量时间来作为论据。
用 map 代替 set 会在每个键下放置一个无人要求的无用值，并让下一个读者去探寻其中的含义。
用 set 代替 map 只能如实报告 0 或 1，除此以外别无他物。

起始代码包含三个计分函数，每个函数均单独测试：

- `countWords(const std::vector<std::string> &words)` 不需要自带容器：每个单词都计入统计（包含重复项），因此对于 `{"red", "blue", "red", "green", "red"}`，以 `int` 返回 5。
- `countDistinctWords(const std::vector<std::string> &words)` 丢弃重复项。
  将每个单词插入到 `std::set<std::string>` 中，并以 `int` 返回其大小；同样的这五个单词应返回 3。
- `countOccurrencesOf(const std::vector<std::string> &words, const std::string &probe)` 以 `int` 返回 `probe` 出现的次数，如果从未出现则返回 0。
  在 `std::map<std::string, int>` 中统计单词计数，并读取 `probe` 的计数。
  上述五个单词对于 `red` 返回 3，对于 `grey` 返回 0。

使用 `std::set<` 构建不重复计数，使用 `std::map<` 构建频次统计。
这两个名称都必须出现在文件中的某个位置（这是 token 检查规则所要求的）；将它们各自保留在需要它们的函数中，才能使代码表达其真正的意图。
对于不包含任何单词的 vector，这三个函数都应返回 0。
`size()` 计数的类型永不为负，因此请通过 `static_cast<int>` 将其返回。

## 解答

```cpp
#include <map>
#include <set>
#include <string>
#include <vector>

struct Solution {
    static int countWords(const std::vector<std::string> &words) {
        // 每个单词都计数，包括重复的
        return static_cast<int>(words.size());
    }

    static int countDistinctWords(const std::vector<std::string> &words) {
        // 不同的单词各计一次，用 set 去重
        std::set<std::string> distinct;
        for (const std::string &word : words) {
            distinct.insert(word);
        }
        return static_cast<int>(distinct.size());
    }

    static int countOccurrencesOf(const std::vector<std::string> &words, const std::string &probe) {
        // 用 map 统计频次，返回 probe 出现的次数，没出现过则为 0
        std::map<std::string, int> counts;
        for (const std::string &word : words) {
            ++counts[word];
        }
        return counts[probe];
    }
};
```
