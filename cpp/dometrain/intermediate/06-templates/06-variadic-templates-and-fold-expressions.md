`template <typename... Args>` 声明了一个模板参数包（template parameter pack），即包含零个或多个类型的列表；而 `const Args&... values` 声明了一个函数参数包（function parameter pack），其中每个类型对应一个参数。
它们结合在一起，可以让一个函数模板接受任意数量的实参：

```cpp
template <typename... Args>
int product(const Args&... values) {
    return (1 * ... * values);
}
```

如果使用单个 `T`，传入两个不同类型的实参将无法进行类型推导。
而使用参数包时，编译器会为每个实参推导一个类型，因此单次调用可以混合不同类型，甚至可以完全不传实参：`product()` 伴随空参数包是一个有效的调用。

参数包中的元素无法通过索引访问，因此 `values[0]` 无法通过编译。
你可以通过包展开（pack expansion）来使用参数包：指定一个包含该包名称的模式（pattern），后面紧跟 `...`，编译器会将其对每个元素重复一次，展开为一个以逗号分隔的列表。
对于名为 `words` 的字符串参数包，`std::vector<std::string> parts{words...}` 会将其中每个元素放入花括号初始化列表中，因此三个单词会生成包含三个元素的 vector，而没有单词则生成一个空的 vector。
`f(values...)` 会将 `values` 的每个元素传递给另一个函数调用。
`sizeof...(args)` 是在编译期已知的参数包 `args` 中元素的数量。
它计算的是实参的个数，而不是字节大小。

### 折叠表达式

`(1 * ... * values)` 是一个折叠表达式（fold expression），即将一个二元运算符应用于整个参数包，并且括号是其语法的一部分。
这是一个以 `1` 作为初始值的二元折叠，它从左侧开始折叠：三个实参会展开为 `((1 * v1) * v2) * v3`，而空参数包则仅保留 `1`。
因为初始值会组合到每个结果中，所以它必须是一个该运算符对其不产生改变的值。

如果省略初始值，就会得到一元折叠，即 `(values * ...)`。
当参数包中有元素时它可以正常工作，但 `product()` 将无法通过编译。
对零个元素进行循环仍然会返回其初始结果；而一元折叠没有初始值可以回退。
只有 `&&`、`||` 和逗号运算符会为空的一元折叠赋予默认值（`&&` 为 `true`，`||` 为 `false`），因此对于任何其他运算符，可能为空的参数包都需要使用二元折叠形式。

折叠表达式还可以对每个元素应用某种模式并组合结果：

```cpp
template <typename... Args>
bool anyNegative(const Args&... values) {
    return (false || ... || (values < 0));
}
```

模式 `(values < 0)` 会针对每个元素重复，因此 `anyNegative(4, -2, 7)` 会展开为 `((false || (4 < 0)) || (-2 < 0)) || (7 < 0)` 并返回 `true`。
该模式本身需要用括号包裹。
如果没有括号，编译器会报错 `expression not permitted as operand of fold expression`。

### 编写内容

在 `variadic.hpp` 中，编写四个函数模板，每个模板均使用 `template <typename... Args>` 声明：

- `int countArgs(const Args&... args)` 返回实参的数量。
- `int sumAll(const Args&... values)` 返回它们的和，如果没有实参则返回 0。
- `bool allPositive(const Args&... values)` 当每个实参都大于 0 时返回 `true`。
  如果没有实参则返回 `true`，因为没有任何实参不满足条件。
- `std::string joinWords(const std::string& separator, const Args&... words)` 返回各单词，且每对单词之间用 `separator` 分隔（其他位置不添加分隔符），如果没有单词则返回空字符串。
  参数包可以跟在普通参数之后：第一个实参绑定到 `separator`，其余实参绑定到 `words`。

使用折叠表达式编写 `sumAll` 和 `allPositive`。
`driver.cpp` 会按顺序将 `countArgs()`、`countArgs(7)` 和 `countArgs(1, std::string("two"), 3.5)` 的结果放入同一个列表，因此正确的 `countArgs` 会得到 `[0, 1, 3]`。
它分别用三个 `int` 和不带实参调用 `sumAll`，用四个 `int` 和不带实参调用 `allPositive`，用三个 `std::string` 单词和不带单词调用 `joinWords`。
不带单词的 `joinWords` 结果会放在方括号内返回，因此空字符串显示为 `[]`。

### 解答

```cpp
#pragma once
#include <cstddef>
#include <string>
#include <vector>

template <typename... Args>
int countArgs(const Args&... args) {
    return static_cast<int>(sizeof...(args));
}

template <typename... Args>
int sumAll(const Args&... values) {
    // 二元折叠，空包时为 0
    return (0 + ... + values);
}

template <typename... Args>
bool allPositive(const Args&... values) {
    // 二元折叠，空包时为 true
    return (true && ... && (values > 0));
}

template <typename... Args>
std::string joinWords(const std::string& separator, const Args&... words) {
    // 包展开到 vector，再逐个拼接
    std::vector<std::string> parts{words...};
    std::string result;
    for (std::size_t i = 0; i < parts.size(); ++i) {
        if (i > 0) {
            result += separator;
        }
        result += parts[i];
    }
    return result;
}
```
