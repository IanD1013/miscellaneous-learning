对 map 的每次循环遍历都会携带一个完整的条目（entry）而不是单个值，因此循环体需要为两样东西命名：

```cpp
#include <map>
#include <string>

std::map<std::string, int> totals;
totals["cow"] = 50;
totals["ant"] = 30;

for (const auto &entry : totals) {
    int value = entry.second;   // entry.first 是键
}
```

`entry` 是 map 中的一个条目，`entry.first` 是它的键，`entry.second` 是它的值。
本练习禁用了这两种写法，以及通过迭代器访问这两部分的箭头形式 `->first` 和 `->second`，因此上面的循环体只是用来展示条目包含的内容，而不是要复制的代码；下面的代码块展示了应该使用的形式。
将条目声明为 `const auto &` 会绑定到 map 中条目的引用，因此字符串键不会在每次循环时被复制。
这两个名称来自于库本身，不能表达数据的含义，而第二种形式改善了这一点：

```cpp
for (const auto &[word, total] : totals) {
    // word 是键，total 是值
}
```

这就是结构化绑定（structured binding）。
方括号替代了原本单个循环变量的位置，并按顺序为本次遍历声明了两个名称：第一个名称代表键，第二个名称代表值。
这两个名称由你自行决定；如果颠倒顺序，并不会调换实际内容，只会让你本想给值的名称赋给了键。

顺序是 `std::map` 自身的保证。
无论条目以何种顺序插入，它们都会按键升序输出（最小的键排在最前面），因此上面的循环会在访问 `cow` 之前先访问 `ant`。
无需任何排序操作即可实现这一点，并且 `sort(` 已被禁用以防尝试排序；`std::unordered_map` 也一并被禁用，因为本练习评分所依赖的正是 `std::map` 保证的顺序。

`firstKeyReachingThreshold(keys, values, threshold, absent)` 返回一个 `std::string`。
使用 `+=` 将 `values[i]` 累加到 `keys[i]` 对应的条目中，这样如果同一个键出现两次，它最终将保存两个值的总和。
然后带着一个累加总和（running total）遍历该 map，并返回累加总和首次达到 `threshold` 处条目的键（使用 `>=` 进行比较，以便在累加总和恰好等于某个条目的阈值时在该处停止）。
当没有任何键符合条件、map 为空或两个 vector 包含的元素数量不相等时，返回调用方传入的值 `absent`。
该值由调用方提供，因为 `""` 在这里是一个合法的键，不仅会被存储，而且在某个测试用例中期望作为有效结果返回。

## 解答

```cpp
#include <cstddef>
#include <map>
#include <string>
#include <vector>

struct Solution {
    static std::string firstKeyReachingThreshold(const std::vector<std::string> &keys, const std::vector<int> &values, int threshold, const std::string &absent) {
        std::map<std::string, int> totals;
        // 长度不同时返回调用者给的 absent
        if (keys.size() != values.size()) {
            return absent;
        }
        // 把每个值累加到对应键的条目里
        for (std::size_t i = 0; i < keys.size(); ++i) {
            totals[keys[i]] += values[i];
        }
        // 按 map 的顺序遍历，累加总和首次达到阈值时返回该键
        int running = 0;
        for (const auto &[key, total] : totals) {
            running += total;
            if (running >= threshold) {
                return key;
            }
        }
        return absent;
    }
};
```
