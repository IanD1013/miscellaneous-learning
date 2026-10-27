name 列的宽度取决于整个输入，因此不能在构建第一行报告时就确定下来。
先测量全部内容，然后进行格式化：第一轮遍历决定保留哪些条目，第二轮将它们转换为行。

当一个条目包含等号且等号前面至少有一个字符时，该条目才会被保留。

```cpp
std::size_t split = entry.find('=');
if (split == std::string::npos || split == 0) {
    continue;
}
```

`find` 会返回第一个 `=` 的位置，如果字符串中没有 `=` 则返回 `std::string::npos`。
这个返回值不是一个很小的数字，而是 `std::size_t` 能容纳的最大值，并且很容易悄无声息地出错。
作为计数参数时，`substr(0, npos)` 会复制到末尾；而 `npos + 1` 会回绕（wrap around）到 0，因此 `substr(split + 1)` 会从头开始。
如果跳过比较，不带等号的条目就会变成一个其 name 和 value 都等于整个条目的字段，从而拉宽列并增加一行，而没有任何地方报错。
位于位置 0 的等号意味着没有 name，因此这些条目也会被跳过，跳过的条目既不打印也不参与测量。

只有第一个等号起到分隔作用。
`substr(0, split)` 是 name，从 `split + 1` 开始的所有内容都是 value，因此 `a=b=c` 的 value 是 `b=c`。
位于最后位置的等号意味着没有内容可复制，value 保持为空。
起始模板中的 `Field` 结构体包含一个 `name` 和一个 `value`，供第一轮遍历填充。

列宽是保留的最长 name 的长度加 2。
每一行的格式为：name，接着是 `:`，然后是空格（直到 value 前面的文本正好达到该宽度），接着是 value；当 value 为空时则显示单个 `-`：

```text
host: local
p:    8080
```

行与行之间通过使用 `+=` 追加 `\n` 进行连接，行与行之间保留一个换行符，最后一行之后不添加换行符。
结果评测会原样严格比对返回的字符串，不会去除两端的任何字符。

`formatReport` 接收 `const std::vector<std::string> &entries` 并以 `std::string` 形式返回报告：

- 保留的条目按传入顺序显示，跳过的条目既不出现在报告中，也不计入列宽。
- 每个 value 前面的文本宽度都相同，因此无论每个 name 有多长，value 都会对齐。
- 空的 value 显示为 `-`，绝不能是以空格结尾的行。
- 你的代码中必须包含 `find(`、`std::string::npos`、`substr(` 和 `+=`，同时禁用 `<sstream>` 和 `std::cout`。
- 空列表以及没有任何条目被保留的列表，都返回空字符串。

## 解答

```cpp
#include <cstddef>
#include <string>
#include <vector>

struct Field {
    std::string name;
    std::string value;
};

struct Solution {
    static std::string formatReport(const std::vector<std::string> &entries) {
        // 第一轮：把每个格式正确的条目转换成 Field，并测量最长的 name
        std::vector<Field> fields;
        std::size_t longest = 0;
        for (const std::string &entry : entries) {
            std::size_t split = entry.find('=');
            if (split == std::string::npos || split == 0) {
                continue;
            }
            Field field;
            field.name = entry.substr(0, split);
            field.value = entry.substr(split + 1);
            if (field.name.size() > longest) {
                longest = field.name.size();
            }
            fields.push_back(field);
        }

        // 第二轮：每个 Field 生成一行，用空格把 value 前的文本补齐到同一宽度
        std::size_t width = longest + 2;
        std::string report;
        for (std::size_t i = 0; i < fields.size(); i++) {
            if (i > 0) {
                report += "\n";
            }
            std::string line = fields[i].name + ":";
            while (line.size() < width) {
                line += " ";
            }
            if (fields[i].value.empty()) {
                line += "-";
            } else {
                line += fields[i].value;
            }
            report += line;
        }
        return report;
    }
};
```
