`substr` 从字符串中复制一段字符并返回该副本，而调用它的原始字符串保持完全不变。

```cpp
std::string text = "abcdefgh";
std::string tail = text.substr(5);
std::string part = text.substr(2, 3);
```

`text.substr(5)` 从位置 5 开始复制直到末尾，因此 `tail` 保存为 `fgh`。
`text.substr(2, 3)` 从位置 2 开始复制最多 3 个字符，因此 `part` 保存为 `cde`。
第二个参数是长度，即字符数，而不是停止的位置。
如果请求的字符数超过了剩余字符数，你将毫无怨言地获得剩余的所有字符：`text.substr(7, 4)` 返回 `h`。
`text` 本身未受影响，因为每次调用都会生成一个独立的副本。
一次调用就获取了整段内容，因此不需要 `for` 和 `while`：没有任何东西留给循环去遍历。

### 最后一个有效的位置，以及第一个无效的位置

合法位置从 0 开始，一直到并包括字符串大小，即 `pos <= s.size()`。
对于 8 个字符的字符串，`text.substr(8)` 会返回一个空字符串，因此该上限是真正可用的。
再往后一个位置，`text.substr(9)`，会导致整个测试用例以退出代码 134 终止，且不返回任何值。
该引擎上不会报告任何出错信息，并且调用之后的代码都不会执行。
在每条路径上、进入 `substr` 之前，务必先检查位置。
这就是第 8.2 课的规则，但有一个值得强调的区别：对于 `substr`，大小（size）是一个合法位置，而对于 `s[i]`，它从来都不是一个合法的索引。

你的函数是 `extractField(const std::string &text, int start, int length)`，它返回一个 `std::string`。
负数的 `start`、负数的 `length` 或大于字符串大小的 `start` 都会被拒绝并返回 `"?"`，这是第 8.2 课中用于表示不可读取索引的标记。
所有其他请求都返回 `text.substr(start, length)`。
请使用 `start > static_cast<int>(text.size())` 进行比较，因为 `size()` 返回的不是 `int`，类型转换可以使比较的双方保持一致。

空字符串不能用作拒绝值，因为当 `start` 等于字符串大小时合法返回的就是空字符串。
每个测试用例都会对你的函数返回的字符串进行评分，因此应返回 `"?"` 而不是打印它。

### 解答

```cpp
#include <string>

struct Solution {
    static std::string extractField(const std::string &text, int start, int length) {
        // 先用 size() 检查位置，再返回对应的那一段字符
        if (start < 0 || length < 0 || start > static_cast<int>(text.size())) {
            return "?";
        }
        return text.substr(start, length);
    }
};
```
