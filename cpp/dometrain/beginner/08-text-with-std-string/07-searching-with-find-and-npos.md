在一段文本中查找另一段文本可以使用 `find`，它返回的是一个位置，而不是单纯的“是”或“否”：

```cpp
std::string text = "banana";
auto position = text.find("na");
```

`position` 的值为 2，即整个 `na` 按顺序出现的最左侧位置。
位置 4 处的后续匹配会被忽略，因为 `find` 只报告第一个匹配项。
匹配是区分大小写的，因此在 `banana` 中搜索 `NA` 完全不会有匹配项；而搜索空的目标字符串则会在位置 0 处匹配，而不是被拒绝。

`find` 返回的是一个无符号计数类型，没有负值来表示未找到匹配项，因此 `auto` 会从调用中获取该类型。
标准库保留了该类型所能容纳的最大值，并将其命名为 `std::string::npos`。
因此，`position == std::string::npos` 是判断未找到匹配项的检查方式，也是唯一有效的方法。
`position < 0` 虽然能够编译通过，但永远不会为 true，这会导致未找到的目标字符串像真实位置一样继续传递。
在通过该比较之后，再使用 `static_cast<int>(position)` 进行转换，切勿在此之前转换；并且不要依赖 `npos` 本身转换为 `int` 后的值。

`firstIndexOr(const std::string &text, const std::string &target, int missing)` 返回一个 `int`：即 `target` 在 `text` 中首次出现的位置，或者在未出现时返回调用方传入的 `missing` 值。
`missing` 作为一个参数是有原因的。
各个测试用例会为其传入不同的值，因此在函数中硬编码一个固定数字会导致某些用例失败。
选择一个不可能等于任何真实位置的值是调用方的责任：某个用例在目标不存在时传入了 3，函数便直接返回 3，这与在第 3 个字符处匹配完全无法区分。

在位置 0 处的匹配是一个真实有效的结果，而 `if (text.find(target))` 恰恰会将该匹配视为 false，同时将未找到目标视为 true，在最关键的地方颠倒了结果。
在空 `text` 中搜索包含任意内容的目标会返回 `missing`，`target` 长度大于 `text` 时也是如此，而无论文本内容为何，空的 `target` 都返回 0。
评测不会比较任何打印输出；评分依据是返回的 `int` 值。
你的代码中必须出现 `std::string::npos`，并且由于此处应由 `find` 负责扫描，因此 `substr(`、`for` 和 `while` 均已被禁用。

## 解答

```cpp
#include <string>

struct Solution {
    static int firstIndexOr(const std::string &text, const std::string &target, int missing) {
        // 在 text 中查找 target，返回第一个匹配的起始位置，找不到则返回 missing
        const auto position = text.find(target);
        if (position == std::string::npos) {
            return missing;
        }
        return static_cast<int>(position);
    }
};
```
