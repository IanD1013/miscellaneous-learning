在对一段文本执行任何其他操作之前，通常会提出两个问题：它是否包含任何字符，以及包含多少个字符。
`std::string` 通过点号后面的调用分别回答了这两个问题。

```cpp
std::string label = "Ada";

std::cout << label.size();
if (label.empty()) {
    std::cout << " and nothing in it";
}
```

这会输出 `3`，并且 `if` 主体永远不会执行。
`label.size()` 会报告 `label` 中包含多少个字符（从 1 开始计数），因此三个字符会报告 3。
请将结果视为计数而非索引：它表示有多少文本，而在 `label` 中位置 3 上没有任何内容。
`label.empty()` 询问另一个问题：这个字符串是否完全为空，并返回一个 `bool` 值，这就是为什么它可以直接放入 `if` 中而无需与任何内容进行比较。
它报告的是是否为空，而不是使其变空，因此文本在调用前后保持完全一致。
`size() == 0` 是同一种测试的繁琐写法，而 `empty()` 直接指明了所提的问题。

计数伴随着一种类型转换。
`size()` 返回的是无符号计数类型而不是 `int`，因此返回 `int` 的函数需要显式写出类型转换，如 `static_cast<int>(label.size())`，这也是第 3 章中用来将除法强制转换为 `double` 的同一种类型转换。

计数是以字节为单位的。
`"café"` 报告的是 5 而不是 4，因为带重音符号的字符占用两个字节，所以计数可能会大于读者看到的字母数量。

需要构建的函数是 `lengthOfFirstNonEmpty(const std::string &first, const std::string &second)`，测试会直接读取它返回的 `int`。
当 `first` 包含任何内容时返回 `first` 的长度；仅当 `second` 包含内容时返回 `second` 的长度；当两者都不包含任何字符时返回 `-1`。
包含一个空格的字符串不是空的，因为空格也是一个字符，所以 `" "` 的测量值为 1，而不是顺延到另一个字符串。
`-1` 是第 4 章中记录的当调用无法给出答案时的拒绝返回值，且任何长度都不会是负数，因此调用方可以将两者区分开来。
在测量任何内容之前，先使用 `empty()` 检查这两个字符串，并使用 `size()` 报告所选字符串的计数。

## 解答

```cpp
#include <string>

struct Solution {
    static int lengthOfFirstNonEmpty(const std::string &first, const std::string &second) {
        // 先用 empty() 判断哪个字符串有内容，再用 size() 返回它的字符数
        if (!first.empty()) {
            return static_cast<int>(first.size());
        }
        if (!second.empty()) {
            return static_cast<int>(second.size());
        }
        return -1;
    }
};
```
