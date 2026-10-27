`std::string` 会在末尾增长，而 `+=` 是将下一部分内容放到该处的运算符。
右侧的内容会就地附加，因此不需要再通过返回值进行赋值。

```cpp
std::string result;
result += "ab";
result += '!';
result += std::to_string(7);
```

`std::string result;` 声明了一个没有初始值设定项的字符串，它起始为空，而不是包含任何不可预测的内容。
在执行这三条语句后，`result` 的内容为 `ab!7`。
`+=` 的右侧可以是另一个 `std::string`、文本字面量或单个 `char`，其中 `char` 形式会将该单个字符追加到末尾。
但它不会自动为你将数字转换成文本：`result += 7;` 追加的是编码为 7 的字符，而不是数字字符。
`std::to_string(7)` 会先构建十进制文本 `"7"`，然后追加该文本。
`std::string` 和 `std::to_string` 都由 `#include <string>` 提供。

作为单独的语句编写时，`result + text[i]` 看起来完成了相同的工作，但实际上什么都没做，因为 `+` 会构建一个新的字符串并将其丢弃。
用 `+` 连接的两个字符会被当作字符编码相加，而不是拼接成文本，因此结果是通过 `+=` 一次一段逐步增长的。
有三个规则限定了这种形式：你的解答中必须出现 `+=`；禁止使用 `result = result`（从而排除了 `result = result + piece`）；并且禁用了字符串流。

编写函数 `separateCharacters(const std::string &text, const std::string &separator, bool appendNumber, int trailingNumber)`，返回一个 `std::string`。
通过索引遍历 `text` 并返回其字符，在每对字符之间添加 `separator`，且仅在字符之间添加：第一个字符前面没有分隔符，最后一个字符后面也没有分隔符。
仅当索引大于 0 时追加分隔符，这样可以确保两端都不会出现分隔符。

数字是否加入结果仅由 `appendNumber` 决定，因此 `trailingNumber` 可以是任何值，包括负数。
当其为 true 时，它会作为十进制文本追加到末尾；若 `text` 包含任何内容，则在数字前加上分隔符：`"ab"` 搭配 `"-"` 和 65 返回 `a-b-65`，`"ab"` 搭配 `"::"` 和 -5 返回 `a::b::-5`。
空文本在标志为 true 时仅返回该数字。

空 `text` 在标志为 false 时返回空字符串，而空的 `separator` 返回原样不变的 `text`。
这两种情况都是合法的返回值：此函数不会拒绝任何输入。
单字符文本仅返回该字符本身，任何位置都不带分隔符。
返回的字符串将进行精确比较，两端不会裁剪任何字符，因此末尾粘连分隔符会导致测试用例失败。

## 解答

```cpp
#include <string>

struct Solution {
    static std::string separateCharacters(const std::string &text, const std::string &separator, bool appendNumber, int trailingNumber) {
        // 一段一段地构建结果，最后返回
        std::string result;
        const int length = static_cast<int>(text.size());
        for (int i = 0; i < length; ++i) {
            if (i > 0) {
                result += separator;
            }
            result += text[i];
        }
        if (appendNumber) {
            if (!text.empty()) {
                result += separator;
            }
            result += std::to_string(trailingNumber);
        }
        return result;
    }
};
```
