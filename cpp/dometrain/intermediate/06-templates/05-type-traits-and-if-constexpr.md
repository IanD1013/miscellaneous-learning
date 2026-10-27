函数模板在使用它的每种类型上都会被编译一次，并且对于该类型，其整个函数体都必须能够成功编译。
普通的 `if` 并不会改变这一点：两个分支都会被编译，包括对于当前 `T` 永远不会执行的分支。
而 `if constexpr` 是在编译期决定的。
编译器会保留条件选中的分支，并针对该 `T` 丢弃其他分支，因此被丢弃的分支可以包含对于该类型无法编译的代码：

```cpp
template <typename T>
int total(const T& value) {
    if constexpr (std::is_same<T, std::vector<int>>::value) {
        return std::accumulate(value.begin(), value.end(), 0);
    } else {
        return value;
    }
}
```

该条件检查 `T` 是否完全是 `std::vector<int>`。
`total(7)` 返回 7，而 `total(std::vector<int>{1, 2, 3})` 返回 6。
如果去掉 `constexpr`，这两个调用都无法通过编译：`total<int>` 必须在 `int` 上编译 `value.begin()`，而 `total<std::vector<int>>` 则必须编译 `return value;`，即将 vector 转换为 `int`。

全特化也可以为某种类型提供独立的代码，但需要为每种类型提供单独的定义；而 `if constexpr` 则将所有类型的代码保留在一个函数体中。

### 类型萃取 (Type traits)

`std::is_same` 来自 `#include <type_traits>`，此外还有许多关于类型的查询，被称为类型萃取（type traits）。
它们每个都是一个类模板，其静态成员 `value` 是编译器在编译期获知的 `bool` 值。
这里还需要用到另外两个：

- 对于整型类型，`std::is_integral<T>::value` 为 true：包括 `int`、固定宽度类型（如 `std::uint8_t`），以及 `char` 和 `bool`。
- 对于每个枚举类型（无论是 `enum class` 还是普通 `enum`），`std::is_enum<T>::value` 均为 true。
  枚举不是整型类型，因此即使每个枚举项都有一个数值，`std::is_integral` 对它也为 false。

C++17 还支持更简短的写法，即用 `std::is_same_v<T, U>` 代替 `std::is_same<T, U>::value`。

`if constexpr` 后面可以跟随 `else if constexpr (...)` 测试。
它们自上而下进行评估，并且命中第一个为 true 的测试，因此更狭窄（更具体）的测试应放在前面。
`bool` 能通过 `std::is_integral` 测试，因此写在它下方的 `std::is_same<T, bool>::value` 测试将永远无法到达。

### 拒绝所有其他类型

未能通过所有测试的类型将进入最终的 `else`。
在其中放置一个 `static_assert` 可以将该调用转为带有自定义信息的编译错误，前提是该条件依赖于 `T`；这样它就只针对进入该分支的类型进行检查：

```cpp
static_assert(std::is_same<T, std::string>::value, "kindAndValue accepts bool, integer types, enums and std::string");
```

有了这行代码，`kindAndValue<double>(1.5)` 产生的第一条错误如下所示。
`std::__2::basic_string<char>` 是标准库中 `std::string` 的完整名称。

```text
static_assert failed due to requirement 'std::is_same<double, std::__2::basic_string<char> >::value' "kindAndValue accepts bool, integer types, enums and std::string"
```

`static_assert(false, "unsupported type")` 看起来像是一个捷径，但是用于编译此处代码的 Clang 8 会拒绝它。
一个没有提及 `T` 的条件对所有类型都有相同的结果，因此 Clang 8 在读取模板时会立即检查它，并通过 `static_assert failed "unsupported type"` 中止每次构建，即使是只调用了 `kindAndValue<int>` 的构建也是如此。
GCC 13 和 Clang 17 及更高版本遵循了 2023 年对该规则的修改（即使在 `-std=c++17` 下），并仅对进入该分支的类型进行检查。
包含 `T` 的条件在旧版编译器和新版编译器上的行为是一致的。

### 编写内容

在 `kinds.hpp` 中，将 `template <typename T> std::string kindAndValue(const T& value)` 编写为一个带有 `if constexpr` 链的函数体：

- 对于 `bool`，返回 `"flag true"` 或 `"flag false"`。
- 对于任何其他整型类型（包括 `char`），返回 `"integer "` 加上该数值，因此 `'A'` 返回 `integer 65`。
- 对于枚举，返回 `"enum "` 加上枚举项的数值，因为模板无法查询枚举项的名称。
  `std::to_string` 没有接受 `enum class` 值的重载，因此请先使用 `static_cast<int>` 对其进行转换。
- 对于 `std::string`，返回 `"text "` 加上双引号包裹的字符串：例如对于 `hi`，即为 `text "hi"`。
- 任何其他类型都必须在 `static_assert` 处中止构建，并附带你自定义的提示信息。

`driver.cpp` 在每次调用中都显式指定了类型，如 `kindAndValue<int>(value)`，因此 `kindAndValue` 必须是一个模板。
`describeChar(code)` 传入具有该代码的字符，因此 65 为 `'A'`。
`describeStatus(code)` 传入由 `driver.cpp` 声明的 `enum class Status { ok = 200, notFound = 404 };` 中具有该数值的值，因此 404 为 `Status::notFound`。

### 解答

```cpp
#pragma once
#include <string>
#include <type_traits>

template <typename T>
std::string kindAndValue(const T& value) {
    // bool 也是整型，必须先判断
    if constexpr (std::is_same<T, bool>::value) {
        return value ? "flag true" : "flag false";
    } else if constexpr (std::is_integral<T>::value) {
        return "integer " + std::to_string(value);
    } else if constexpr (std::is_enum<T>::value) {
        return "enum " + std::to_string(static_cast<int>(value));
    } else {
        // 条件依赖 T，只对进入此分支的类型检查
        static_assert(std::is_same<T, std::string>::value, "kindAndValue accepts bool, integer types, enums and std::string");
        return "text \"" + value + "\"";
    }
}
```
