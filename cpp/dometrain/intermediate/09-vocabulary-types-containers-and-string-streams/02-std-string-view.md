`std::string_view` 是对其存放在别处的字符的非拥有型（non-owning）视图：它只保存一个指向首字符的指针和一个长度，仅此而已。
从 `std::string` 创建一个视图不会拷贝任何字符，在视图上调用 `substr` 也是如此，它只会返回指向相同字符的另一个视图。
为一个包含 3 个字符的字段创建视图与为一个包含 3,000 个字符的字段创建视图的开销是完全一样的。

```cpp
#include <string_view>

std::string path = "src/main.cpp";
std::string_view rest = path;
std::size_t at = rest.find('/');            // 3
std::string_view dir = rest.substr(0, at);  // "src"
rest.remove_prefix(at + 1);                 // "main.cpp"
rest.remove_suffix(4);                      // "main"
std::string name = std::string(rest);       // "main" 的拥有型拷贝
```

视图上的 `find` 用法与在 `std::string` 上相同，当找不到字符时返回 `std::string_view::npos`。
`remove_prefix(n)` 将视图的起始位置向前移动 `n` 个字符，而 `remove_suffix(n)` 则从其末尾丢弃 `n` 个字符。
这两者都只会修改视图本身：在最后一行执行完毕后，`path` 仍然保存着 `"src/main.cpp"`。
它们都不会替你检查 `n`，且 `n` 不能大于 `size()`，因此每次调用前都需要通过 `empty()` 进行测试，或者使用 `find` 在视图内返回的位置。

转换只能单向进行。
在任何需要 `std::string_view` 的地方，`std::string` 都可以自动转换过去，包括作为 `std::string_view` 参数时。
但反向转换需要显式调用 `std::string(view)`，这一拥有所有权的拷贝是唯一会分配内存并复制字符的步骤；在返回 `std::string` 的函数中写 `return rest;` 无法通过编译。
而比较操作完全不需要拷贝：在视图和 `std::string` 之间使用 `==` 会直接比较它们的字符，因此对于内容为 `"src"` 的 `std::string wanted`，`dir == wanted` 为真（true）。

视图不拥有任何内容，因此它所指向的文本的生命周期必须长于视图本身。
只要 `path` 存在，`rest` 和 `dir` 就都是安全的。
但如果一个辅助函数按值接收 `std::string` 类型的文本并返回其视图，就会出问题：该参数只是一个副本，在调用者读取这些视图时它就已经被销毁了，此时每个视图指向的都是不复存在的字符。
编译器会接受这样的辅助函数，而在读取这些视图时也不会有任何报错。

### 需要实现的内容

在 `struct Solution` 中实现三个静态函数：

- `trimmed(text)` 返回去除了两端空格（`' '`）的 `text`。
  单词之间的空格会保留，制表符等其他字符也会保留。
  使用 `remove_prefix` 和 `remove_suffix` 缩小 `text` 视图的范围，然后对剩余内容执行一次拷贝。
  纯空格文本应返回 `""`。
  对于此类输入，所有字符都会被移除，导致视图最终为空，而空视图没有字符可供 `front()` 或 `back()` 返回。
  在空视图上调用这两者中的任何一个都是未定义行为（undefined behavior），因此在每次调用前请先检查 `empty()`。
- `splitFields(line, separator)` 按顺序返回 `line` 中的各个字段，每个字段为一个 `std::string`。
  每个分隔符结束一个字段并开启下一个字段，因此包含 n 个分隔符的行会有 n + 1 个字段，无论是在两端还是在中间的空字段都会被保留：以 `';'` 分割 `";;"` 会得到三个空字段。
  只有 `separator` 会作为字段结束标志，因此以 `';'` 分割 `"a,b"` 得到的单个字段为 `"a,b"`。
  分割不会进行修剪（trim）：以 `';'` 分割 `" a ; b "` 会得到 `" a "` 和 `" b "`。
  在测试输入中，`separator` 会以字符编码形式出现，例如 `','` 为 44，`';'` 为 59。
- `countFieldsEqual(line, separator, wanted)` 返回与 `wanted` 相等的字段数量，比较整个字段。
  `"x,xx,,x"` 的字段分别为 `"x"`、`"xx"`、`""` 和 `"x"`，因此 `countFieldsEqual("x,xx,,x", ',', "x")` 返回 2：`"xx"` 包含 `"x"` 但与它不相等。
  `wanted` 可能为空，此时仅匹配空字段，因此对于同一行输入 `""` 会返回 1。
  此函数在返回后无需保留任何内容，因此直接将每个字段的视图与 `wanted` 进行比较即可，不要进行拷贝。

`splitFields` 和 `countFieldsEqual` 需要相同的字段划分，因此可以编写一个私有静态辅助函数，将其作为 `std::vector<std::string_view>` 返回，供两者共同使用。
该辅助函数中的视图指向 `line`，其生命周期长于两个函数对其的所有使用。
随后 `splitFields` 会将每个视图拷贝到其结果中，因为在 `line` 可能失效之后调用者仍会保留该 vector。

最显而易见的循环条件（只要该行的剩余部分非空就继续运行）会漏掉一个字段。
对于 `",a,"`，最后的 `remove_prefix` 会使视图变为空，循环终止，导致最后一个逗号后面的空字段永远不会被添加。
在运行之前，请先推导一下 `countFieldsEqual("", ',', "")` 应该返回什么；运行结果会验证你的循环逻辑是否正确。

### 解答

```cpp
#include <string>
#include <string_view>
#include <vector>

struct Solution {
    static std::string trimmed(const std::string& text) {
        std::string_view view = text;
        while (!view.empty() && view.front() == ' ') {
            view.remove_prefix(1);
        }
        while (!view.empty() && view.back() == ' ') {
            view.remove_suffix(1);
        }
        return std::string(view);
    }

    static std::vector<std::string> splitFields(const std::string& line, char separator) {
        std::vector<std::string> result;
        for (std::string_view field : fields(line, separator)) {
            result.push_back(std::string(field));  // line 失效后仍需保留，必须拷贝
        }
        return result;
    }

    static int countFieldsEqual(const std::string& line, char separator, const std::string& wanted) {
        int count = 0;
        for (std::string_view field : fields(line, separator)) {
            if (field == wanted) {
                ++count;
            }
        }
        return count;
    }

private:
    // 返回指向 line 的各字段视图
    static std::vector<std::string_view> fields(std::string_view rest, char separator) {
        std::vector<std::string_view> result;
        while (true) {
            std::size_t at = rest.find(separator);
            if (at == std::string_view::npos) {
                result.push_back(rest);  // 最后一个字段，可能为空
                return result;
            }
            result.push_back(rest.substr(0, at));
            rest.remove_prefix(at + 1);
        }
    }
};
```
