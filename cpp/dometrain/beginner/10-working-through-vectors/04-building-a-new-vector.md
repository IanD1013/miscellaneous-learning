过滤 vector 会保留一部分元素并丢弃其余元素，而最经济的做法其实是什么都不“丢弃”。
我们可以从一个空的第二个 vector 开始，循环依次检查输入中的每个元素，并通过 `push_back` 仅复制通过测试的元素：

```cpp
std::vector<std::string> input = {"one", "two", "three"};

std::vector<std::string> kept;
for (const std::string &item : input) {
    if (item.size() > 3) {
        kept.push_back(item);
    }
}
```

`kept` 最终仅包含 `"three"`。
`push_back` 会在末尾追加，因此保留下来的元素会维持它们在原序列中的相对顺序，并且由于循环仅读取 `input`，所以输入保持不变。
根据通过测试的元素数量，结果可能包含零个到与输入相同数量的元素。

相反，从输入中直接删除未通过的元素不仅更繁琐，而且可靠性更低。
参数是一个 `const` 引用，因此根本无法对其进行任何修改；而且在遍历过程中删除元素会使下一个元素向前移动到刚释放的位置，而循环此时已经走过了该位置。

本练习中的测试是“包含”而非“相等”。
当 `text` 出现在 `word` 的任何位置（开头、中间或末尾）时，`word.find(text) != std::string::npos` 均为 true。
输入中的空字符串不包含此处使用的任何搜索文本，因此它会像其他不匹配的单词一样无法通过测试。

- `wordsContaining` 接受 `const std::vector<std::string> &words` 和 `const std::string &text`，并返回一个会逐元素进行比对的 `std::vector<std::string>`。
- 复制所有包含 `text` 的单词，保持它们在 `words` 中的顺序，包括重复项。
- 当没有任何匹配项，或者 `words` 本身为空时，返回的结果为空。
  这是正确的结果，而不是报错。
- 使用 `push_back` 追加元素。
  `copy_if` 和 `remove_if` 均被禁用，省略名称前的 `std::` 也是无效的，因为本题旨在考察循环和追加操作。

## 解答

```cpp
#include <string>
#include <vector>

struct Solution {
    static std::vector<std::string> wordsContaining(const std::vector<std::string> &words,
                                                    const std::string &text) {
        std::vector<std::string> found;
        // 把每个包含 text 的单词复制到 found 中，words 保持不变
        for (const std::string &word : words) {
            if (word.find(text) != std::string::npos) {
                found.push_back(word);
            }
        }
        return found;
    }
};
```
