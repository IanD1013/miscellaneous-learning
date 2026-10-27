`<cctype>` 收集了一组小型函数，每个函数用于回答关于单个字符的某一个问题。

```cpp
#include <cctype>

int digits = 0;
if (std::isdigit(static_cast<unsigned char>(c))) {
    digits += 1;
}
```

`std::isdigit` 对十个数字字符返回“是”，`std::isalpha` 对大小写字母返回“是”，而 `std::isupper` 仅对大写字母返回“是”。
每个函数都返回一个 `int`：否为 0，是为某个非零值。
因此函数调用本身就可以作为条件，绝不要将其与 `true` 进行比较，因为那样的比较会将测试范围缩小到某一个特定的非零值。

参数周围的类型转换值得理解而不仅仅是照抄。
这些函数接收一个其值必须能表示为 `unsigned char`（即 0 到 255）的 `int`。
普通的 `char` 是一个独立的类型，区别于 `signed char` 和 `unsigned char`；在许多平台上，它的行为类似于 signed char，因此从文本中提取的大于 127 的字节会变成负数。
将该负数传递给这些函数之一是未定义行为，而 `static_cast<unsigned char>(c)` 可以防止这种情况，在调用前将字节转换为 0 到 255。
这里测试的每个字符都是 ASCII 字符，因此没有进行类型转换的版本也能通过所有八个用例，但遇到第一个大于 127 的字节时仍然是错误的。

`std::tolower` 位于同一个头文件中。
它返回所传入字符的小写形式，对于任何非大写字母的字符则原样返回，并且绝不修改原始字符，因此返回值是小写字符存在的唯一位置。
它同样返回一个 `int`，在与字符字面量进行任何比较之前，应使用 `static_cast<char>` 将其转换回去。

`countKind(const std::string &text, char kind)` 返回一个 `int`。
先将 `kind` 转为小写，然后进行计数：`'d'` 计算数字个数，`'l'` 计算字母个数，`'u'` 计算大写字母个数，其中 `'D'`、`'L'` 和 `'U'` 表示相同的三种含义。
任何其他种类（例如 `'x'`）都返回 `-1`，这是本课程自第 4 章以来一直使用的拒绝值。
将每个 `<cctype>` 参数都用 `static_cast<unsigned char>` 包装，包括 `kind`，并保留起始代码中的 `#include <cctype>` 行。
调用时请写上 `std::` 限定符（包括 `std::isdigit` 和 `std::tolower` 等），这是被检查的形式。
不包含所请求种类的文本返回 0，空文本也返回 0，因为这两者都是真实的计数值。

## 解答

```cpp
#include <cctype>
#include <string>

struct Solution {
    static int countKind(const std::string &text, char kind) {
        // 先把种类代码转为小写，确定要问的问题，再统计回答“是”的字符
        const char lowered = static_cast<char>(std::tolower(static_cast<unsigned char>(kind)));
        if (lowered != 'd' && lowered != 'l' && lowered != 'u') {
            return -1;
        }
        int total = 0;
        const int length = static_cast<int>(text.size());
        for (int i = 0; i < length; ++i) {
            const unsigned char c = static_cast<unsigned char>(text[i]);
            if (lowered == 'd' && std::isdigit(c)) {
                ++total;
            } else if (lowered == 'l' && std::isalpha(c)) {
                ++total;
            } else if (lowered == 'u' && std::isupper(c)) {
                ++total;
            }
        }
        return total;
    }
};
```
