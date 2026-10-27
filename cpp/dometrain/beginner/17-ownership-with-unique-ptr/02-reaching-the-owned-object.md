访问所有者持有的字符串有三种形式，每种形式的作用各不相同：

```cpp
std::unique_ptr<std::string> owner = std::make_unique<std::string>("ab");

std::size_t n = owner->size();
*owner += "cd";
const std::string *borrowed = owner.get();
```

`owner->size()` 访问所拥有字符串的成员。
该箭头是任何指针都会使用的操作符。
如果写成 `owner.size()`，则是向所有者本身请求一个它并不具备的 `size` 成员，编译器会指出在 `std::unique_ptr` 中找不到该成员。

`*owner` 指代整个被拥有的字符串，而不是其某个成员，因此在任何需要 `std::string` 的地方都可以这样写。
`*owner += "cd";` 会追加到位于堆上的对象本身，而在更长的表达式中使用 `*owner` 会得到该字符串本身，因此将其与其他文本连接时会将这些字符复制到结果中，而堆对象仍然保留在原处。

`owner.get()` 会生成一个指向所拥有对象的普通 `std::string *`：一个借用的原始指针，同时仍然由所有者负责管理该对象。
这里使用点号调用是因为 `get` 是所有者的成员。
借用该指针的代码可以通过它进行读取并返回，绝不能释放它，也绝不能在其超出所有者生命周期后继续持有它。

### 要求

- `appendAndDescribe` 接收 `const std::string &text` 和 `const std::string &suffix`，并返回一个进行精确比对（包含分隔符等所有内容）的 `std::string`。
- 初始代码会从 `text` 构建 `owner`，并提供接收 `const std::string *` 的 `isEmptyText` 函数。
  在追加后缀之前，使用 `owner.get()` 查询所拥有的字符串，当其返回 true 时使用 `empty`，返回 false 时使用 `filled`。
- 使用 `*owner += suffix;` 追加后缀，以便直接修改所拥有的字符串。
- 用 `|` 连接三个字段：前面确定的单词、追加后通过 `owner->size()` 从对象中读出并通过 `std::to_string` 转换为文本的长度，以及所拥有的字符串本身。
- 两个参数中的任意一个都可以为空，且两者可以相等。
  `""` 与 `"end"` 会得到 `empty|3|end`，两个空字符串会得到 `empty|0|`（在最后一个分隔符之后没有任何内容）。
- 你的文件中必须同时出现 `*owner`、`.get()` 和 `->size()`，分别对应上述三种形式之一。

### 解答

```cpp
#include <memory>
#include <string>

struct Solution {
    static bool isEmptyText(const std::string *borrowed) {
        if (borrowed == nullptr) {
            return true;
        }
        return borrowed->empty();
    }

    static std::string appendAndDescribe(const std::string &text, const std::string &suffix) {
        std::unique_ptr<std::string> owner = std::make_unique<std::string>(text);
        // 追加后缀之前，先通过借用的指针询问所拥有的字符串是否为空
        std::string word = isEmptyText(owner.get()) ? "empty" : "filled";
        // 直接在所拥有的字符串上追加后缀
        *owner += suffix;
        // 用 | 连接单词、追加后的长度和所拥有的字符串本身
        return word + "|" + std::to_string(owner->size()) + "|" + *owner;
    }
};
```
