`count(key)` 向 map 询问一件事：该键是否存在？它返回 0 或 1，没有其他可能：

```cpp
#include <map>
#include <string>

std::map<std::string, int> counts;
counts["ana"] = 10;

if (counts.count("ana") == 1) {
    // 存在，并且 map 的大小与测试前相同
}
```

map 为每个键最多保留一个条目，因此 `counts.count(` 绝不会找到第二份副本，也不可能返回 2。
它不会插入任何内容，这使得它成为一种不会影响 `size()` 的存在性测试。
若改用 `counts["bo"] != 0`，虽然看起来是在问同样的问题，但行为却截然不同：下标操作会当场创建缺失的条目，且原本存储为 0 的键会被误报为不存在。

当值也很重要时，调用一次 `find` 就能同时兼顾两项工作：

```cpp
auto found = counts.find("ana");
if (found == counts.end()) {
    // ana 下没有存储任何内容
} else {
    int stored = found->second;
}
```

`find` 返回一个迭代器，即 map 中的一个位置。
`end()` 是最后一个条目之后的位置，当不存在该键时返回的就是它，因此 `found == counts.end()` 就是测试条件。
在读取任何内容之前必须先进行这项检查：在这个引擎上，通过 end 迭代器读取数据是不会报错的，它会静默返回一个看似合理的值而不是停止运行，从而导致缺失的键被当作错误的结果继续传递下去。

迭代器指向一个条目，但它本身并不是条目。
使用点号访问成员是访问迭代器本身，而迭代器自身并没有 `second`，因此文件将无法编译。
`->` 则先访问条目再指定成员：`found->second` 是存储的值，而 `found->first` 是键。

### 要求

- `valueWhenBothPresent(const std::vector<std::string> &keys, const std::vector<int> &values, const std::string &wanted, const std::string &required, int fallback)` 返回单个 `int`，不会检查任何打印输出。
- 通过将 `values[i]` 赋值给 `keys[i]` 来构建 map，然后在且仅在 `required` 也存在时，返回 `wanted` 下存储的值。
- 在所有无法报告已存储值的路径上，都应返回 `fallback`：`required` 不存在、`wanted` 不存在、map 没有条目，以及包含不同元素数量的 vector。
- 存储的 0 是一个有效的答案，应返回 0。
  这种冲突正是为什么“无答案”时的值由调用方选择，而不是在函数内部指定一个数字的原因。
- 你的代码中必须同时出现这两种查找方式：`count(` 和 `find(`，而 `std::count(`、`std::find(` 和 `std::unordered_map` 是被禁用的。

### 解答

```cpp
#include <cstddef>
#include <map>
#include <string>
#include <vector>

struct Solution {
    static int valueWhenBothPresent(const std::vector<std::string> &keys, const std::vector<int> &values, const std::string &wanted, const std::string &required, int fallback) {
        // 长度不同时无法构建 map，返回 fallback
        if (keys.size() != values.size()) {
            return fallback;
        }
        // 构建 map，只有 required 也存在时才返回 wanted 下存储的值
        std::map<std::string, int> scores;
        for (std::size_t i = 0; i < keys.size(); ++i) {
            scores[keys[i]] = values[i];
        }
        if (scores.count(required) == 0) {
            return fallback;
        }
        auto found = scores.find(wanted);
        if (found == scores.end()) {
            return fallback;
        }
        return found->second;
    }
};
```
