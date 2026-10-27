在尖括号之间填入 `std::string`，vector 的元素就会是文本而不是数字。
下面的声明构建了一个 vector 并对其进行了遍历。

```cpp
#include <string>
#include <vector>

std::vector<std::string> words = {"red", "", "blue"};

std::string joined;
for (const std::string &word : words) {
    joined += word;
}
```

vector 的其他特性没有任何改变。
`size()` 返回 3，`words[0]` 读取为 `red`，基于冒号的 range-for 循环遍历这些元素的方式与遍历数字时完全相同。
循环变量是值得仔细斟酌的部分：`const std::string &word` 让 `word` 代表正在访问的元素，因此它的字符不会在每次迭代时被复制到循环体中。
`joined` 最终为 `redblue`，中间的空元素像其他两个元素一样被访问，只是它本身没有贡献任何字符。

### 放置分隔符

如果在每个元素后面都追加分隔符，末尾就会多出一个分隔符；而在每个元素前面都追加分隔符，开头又会多出一个。
分隔符应该出现在除第一个元素之外的每个元素前面，在循环上方声明一个 `bool` 变量就足以区分第一次迭代与后续迭代：它初始为 `false`，循环体仅在它已经为 `true` 时才追加分隔符，并且每次迭代在结束前都将其设置为 `true`。

`joinWith` 接收 `const std::vector<std::string> &parts` 和 `const std::string &separator`，并返回一个 `std::string`。

- 每个元素按顺序出现，每对元素之间恰好有一个 `separator`，且两端都没有分隔符。
- 无论空元素位于何处，它仍然是一个元素：`{"a", "", "b"}` 用 `","` 连接后的结果是 `a,,b`，而 `{"", "x", ""}` 用 `"-"` 连接后的结果是 `-x-`，开头的分隔符依然保留。
- 如果没有可连接的内容，则返回空字符串；单个元素则返回其自身，不附加任何分隔符。
- 使用 `+=` 构建结果，你的文件中必须包含该操作符。
  `push_back` 已被禁用，因为你返回的是字符串而不是重新构建的 vector。
- 通过 const 引用获取每个元素，写作 `const std::string &part`。
  按值拷贝的形式 `std::string part` 已被禁用，因此请将正在构建的字符串命名为 `joined`，并将 `part` 留给循环使用。

### 解答

```cpp
#include <string>
#include <vector>

struct Solution {
    static std::string joinWith(const std::vector<std::string> &parts, const std::string &separator) {
        // 按顺序追加每个元素，分隔符只放在相邻元素之间
        std::string joined;
        bool first = true;
        for (const std::string &part : parts) {
            if (!first) {
                joined += separator;
            }
            joined += part;
            first = false;
        }
        return joined;
    }
};
```
