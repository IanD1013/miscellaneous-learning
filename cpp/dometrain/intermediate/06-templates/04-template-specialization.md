在只读的 `describe_primary.hpp` 中，通用的 `template <typename T> struct Describe` 是主模板（primary template）：即编译器为任何没有自己专用定义的类型所使用的定义。
它的 `text` 调用了 `std::to_string`，这仅适用于 `int`，而不适用于列表中保存的其他任何类型。
`bool` 和 `char` 传入 `std::to_string` 时会被提升（promoted）为 `int`，因此它们会变成数字：`false` 变成 `0`，空格变成 `32`。
对于 `std::string`，`std::to_string` 根本没有对应的重载。
请为这三种类型分别提供全特化（full specialization），即针对该特定类型的 `Describe` 完整替换定义：

```cpp
template <>
struct Describe<bool> {
    static std::string text(const bool& value) { return value ? "true" : "false"; }
};
```

`template` 后面的尖括号为空，因为没有剩余的模板参数需要填充，而 `Describe<bool>` 则指明了该定义所针对的类型。
每当编译器需要 `Describe<X>` 时，如果存在专门针对 `X` 编写的特化版本，它就会使用该特化版本，否则将从主模板生成该类。
`Describe<int>` 仍然来自主模板；而 `Describe<bool>` 现在来自上面的代码。

特化会替换整个类。
它不会从主模板继承任何内容，因此它需要重新声明 `text`（包括 `static`），如果特化版本中遗漏了某个成员，那么该成员在 `Describe<bool>` 中就不存在。
请将每个特化写在 `#include "describe_primary.hpp"` 之下，以及任何使用该类型的 `Describe` 的代码之上。

主模板无法针对 `std::string` 编译，而且它也绝不需要这样做：编译器仅对实际调用了其 `text` 的类型才会生成 `text` 的函数体。
在 `Describe<std::string>` 存在之前，单词列表会促使编译器为 `std::string` 生成该函数体，导致构建在主模板所在的行失败并报错 `no matching function for call to 'to_string'`。
一旦特化就位，编译器就永远不会为 `std::string` 生成主模板的函数体。
匹配是完全精确的，不包含任何隐式转换：如果将包含字符串字面量的 `std::vector<const char*>` 传递给 `listOf`，它会请求 `Describe<const char*>`，而 `std::string` 特化并不涵盖该类型，因此会以同样的方式失败。

### 需要添加到 `describe.hpp` 的内容

- 如上所示的 `Describe<bool>`，返回 `"true"` 或 `"false"`。
- `template <> struct Describe<std::string>`，其 `text` 返回双引号包裹的单词：`b c` 变为 `"b c"`。
- `template <> struct Describe<char>`，其 `text` 返回单引号包裹的字符：`~` 变为 `'~'`，空格变为 `' '`。
- `template <typename T> std::string listOf(const std::vector<T>& values)`，它返回方括号括起来的各项，项之间用 `", "` 分隔，最后一项之后没有任何内容，每一项都由 `Describe<T>::text` 格式化。
  单词 `a` 和 `b c` 会得到 `["a", "b c"]`，空 vector 会得到 `[]`。

`driver.cpp` 从 `listInts`、`listWords` 和 `listLetters` 分别使用 `std::vector<int>`、`std::vector<std::string>` 和 `std::vector<char>` 调用 `listOf`。
`listLetters` 会首先将字符编码转换为 `char`。
`describeFlag` 直接调用 `Describe<bool>::text(flag)`。
每种类型一个独立的 `text` 重载虽然可以格式化列表，但显式指定 `Describe<bool>` 的调用只能看到类模板及其特化。

代码正常工作后，仅修改 `char` 特化的尖括号，使其变为 `Describe<unsigned char>`。
推导对于编码 32 和 126，`listLetters` 会返回什么，运行以验证，然后将代码改回 `Describe<char>`。

### 解答

```cpp
#pragma once
#include <cstddef>
#include <string>
#include <vector>
#include "describe_primary.hpp"

template <>
struct Describe<bool> {
    static std::string text(const bool& value) { return value ? "true" : "false"; }
};

template <>
struct Describe<std::string> {
    // 双引号包裹
    static std::string text(const std::string& value) { return "\"" + value + "\""; }
};

template <>
struct Describe<char> {
    // 单引号包裹
    static std::string text(const char& value) { return std::string("'") + value + "'"; }
};

template <typename T>
std::string listOf(const std::vector<T>& values) {
    std::string result = "[";
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i > 0) {
            result += ", ";
        }
        result += Describe<T>::text(values[i]);
    }
    return result + "]";
}
```
