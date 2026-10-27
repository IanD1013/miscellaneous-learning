直接将文本传递给 `std::stoi` 会导致用例在该运行环境中崩溃。
当该库无法执行转换时，程序会立即终止：`abc` 会报告 `stoi: no conversion`，超出类型范围的值会报告 `stoi: out of range`，且调用之后的任何代码都不会执行，包括 `return -1`。
评测系统随后会显示该错误，而不是你预期的答案。

先验证，后转换：先检查每一个字符，只有通过全部三项检查的文本才能进入转换步骤。

文本非空，且其中的每个字符都是十进制数字：

```cpp
std::isdigit(static_cast<unsigned char>(text[i]))
```

`std::isdigit` 将其参数视为一个小的非负数，而 `char` 可能是负数，这正是 `static_cast<unsigned char>` 要解决的问题。
仅测试第一个字符是不够的：对 `12a3` 调用 `std::stoi` 会返回 12，它在遇到字母时停止，并且不会对后续内容做任何处理。

第二项检查是前导零。
`007` 和 `7` 表示同一个值，但只有 `0` 本身可以以零开头。
拒绝其他情况可以保证每个值只有一种表示形式，并允许在后续检查中用文本长度来代表数值的大小：例如 `00000000009` 是表示 9 的 11 个字符。

### 从类型中读取上限

第三项检查是该值能够容纳在 `int` 中。
这里最大的 int 是 2147483647，长度为 10 个字符。
在已经拒绝前导零的情况下，11 个或更多字符总是表示更大的值，而正好 10 个字符时，仅当从左到右读取文本且其不大于 2147483647 时才符合条件：两者第一个不同的位置决定了大小，如果完全匹配也符合条件。

9 位数字也不是上限：拒绝任何超过 9 位数字的规则会排除 2147483647 本身，而 `int` 完全可以容纳这个值。

向 `parseNonNegative` 传入一个 `const std::string &text`，返回一个 `int`：

- 当文本至少包含一个字符、每个字符都是十进制数字、首字符不是 `0`（除非文本恰好为 `0`）且数值不超过 2147483647 时，返回该数值。
- 在所有其他情况下返回 -1，包括空文本。
  有效值绝不会是负数，因此 -1 不会被误认为是有效值。
- 正负号和空格不是数字，因此 `-5` 和 `7 ` 会被拒绝而不是被修剪整理。
- 检查的代码写法包括 `isdigit(`、传给它的 `unsigned` 类型转换，以及 `std::stoi(` 本身。
- 11 个或更多字符仅凭长度就会被拒绝，因此 `10000000000` 在进入转换前就会直接返回 -1。
- 作为函数的最后一步操作，在验证通过的文本上运行一次 `std::stoi(text)`。

### 解答

```cpp
#include <cctype>
#include <cstddef>
#include <string>

struct Solution {
    static int parseNonNegative(const std::string &text) {
        // 在任何转换之前，先证明文本全是数字、没有前导零，并且能放进 int
        if (text.empty()) {
            return -1;
        }
        for (std::size_t i = 0; i < text.size(); i++) {
            if (!std::isdigit(static_cast<unsigned char>(text[i]))) {
                return -1;
            }
        }
        if (text[0] == '0' && text.size() > 1) {
            return -1;
        }
        const std::string largest = "2147483647";
        if (text.size() > largest.size()) {
            return -1;
        }
        if (text.size() == largest.size()) {
            // 长度相同时，第一个不同的位置决定大小
            for (std::size_t i = 0; i < text.size(); i++) {
                if (text[i] < largest[i]) {
                    break;
                }
                if (text[i] > largest[i]) {
                    return -1;
                }
            }
        }
        return std::stoi(text);
    }
};
```
