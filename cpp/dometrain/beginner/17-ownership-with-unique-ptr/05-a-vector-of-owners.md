所有者（owner）可以存储在 vector 中，每个对象对应一个所有者，元素类型正体现了这一点：

```cpp
std::vector<std::unique_ptr<Line>> owners;
owners.push_back(std::make_unique<Line>("first"));
owners.push_back(std::make_unique<Line>("second"));

for (const std::unique_ptr<Line> &owner : owners) {
    int measured = owner->length();
}
```

`std::vector<std::unique_ptr<Line>>` 是一个元素为所有者的 vector，因此它可以同时在堆上保留多个 `Line` 对象，并且当 vector 被销毁时，每个元素都会释放其持有的对象。
无需对容器进行第二次遍历去查找需要释放的内容。

`owners.push_back(std::make_unique<Line>(word))` 在单个表达式中构建 `Line` 及其所有者，并将该所有者直接放入 vector 中。
在那里构建的对象在其他任何地方都没有所有者，因此不会从仍然需要它的变量中夺走所有权。

### 循环可以接受的形式

`for (auto owner : owners)` 在每次迭代时都会将一个元素复制到 `owner` 中，而复制这些元素之一将成为该元素对象的第二个所有者，因此代码在运行前就会被编译器拒绝。
`for (const std::unique_ptr<Line> &owner : owners)` 直接引用 vector 中的元素而不是复制它，并且 `owner->length()` 可以通过它访问 `Line`。
这同样适用于单个元素：`auto current = owners[0];` 会被拒绝，而 `const std::unique_ptr<Line> &current = owners[0];` 则完全正常。

`lineLengths` 接收 `const std::vector<std::string> &words` 并返回一个 `std::vector<int>`，按单词传入的顺序包含每个单词的长度。
`Line` 存储构建它时所用的文本，并将其大小作为 `int` 返回。
为每个单词提供其专有的 `Line`，然后通过拥有它的元素来测量每个单词，这正是两个必需写法 `std::vector<std::unique_ptr<Line>>` 和 `->length()` 所检查的内容，同时 `new` 和 `delete` 将被直接拒绝。
空输入将返回空 vector。
空单词仍然是一个单词，因此 `{"", "xy", ""}` 返回 `{0, 2, 0}`，且重复的单词每次出现都会计入一个长度。

### 解答

```cpp
#include <cstddef>
#include <memory>
#include <string>
#include <vector>

class Line {
public:
    Line(const std::string &text)
        : text_(text) {
    }

    int length() const {
        return static_cast<int>(text_.size());
    }

private:
    std::string text_;
};

struct Solution {
    static std::vector<int> lineLengths(const std::vector<std::string> &words) {
        std::vector<int> lengths;
        // 为每个单词在堆上创建各自的 Line，再通过拥有它的元素测量长度
        std::vector<std::unique_ptr<Line>> owners;
        for (const std::string &word : words) {
            owners.push_back(std::make_unique<Line>(word));
        }
        for (const std::unique_ptr<Line> &owner : owners) {
            lengths.push_back(owner->length());
        }
        return lengths;
    }
};
```
