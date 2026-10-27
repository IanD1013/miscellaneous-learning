下面的 lambda 没有指定参数类型：它的两个参数都是 `const auto&`。
类型为 `auto` 的参数是 auto 参数，包含此类参数的 lambda 则是泛型 lambda：

```cpp
const auto smaller = [](const auto& a, const auto& b) { return a < b ? a : b; };
```

`auto` 参数使该 lambda 的调用运算符成为一个函数模板，就如同在 `operator()` 前写上了 `template <typename A, typename B>` 一样，每个 `auto` 对应一个类型参数。
每出现一种新的实参类型组合，编译器就会为其编写另一个版本：

```cpp
smaller(3, 9);                                     // 3，一个 int
smaller(std::string("pear"), std::string("zoo"));  // "pear"，一个 std::string
```

这两个版本都属于同一个 `smaller` 对象，因此用 int 调用它并不会将其绑定到 int。
每个版本都会推导自己的返回类型，第一个版本推导为 `int`，第二个版本推导为 `std::string`，并且在同一个版本内部，每个 `return` 语句都必须推导出相同的类型。

这些版本是在编译时生成的，并且每个版本在生成时都会进行检查，因此函数体只能使用所有实参类型都支持的操作。
`smaller(std::string("pear"), 3)` 无法编译：因为没有 `<` 可以比较 `std::string` 和 `int`。

### lambdas.hpp 中的两个 lambda

`largestOr` 和 `descending` 是 lambdas.hpp 中命名空间作用域下的 `const auto` 对象，具有空的捕获列表，因为在那里没有局部变量可供捕获。
driver.cpp 将 `descending` 传递给 `std::sort`，形式为 `std::sort(values.begin(), values.end(), descending)`，而 `std::sort` 会从该实参推导其比较操作的类型。
无论编译器为其调用运算符生成了多少个版本，泛型 lambda 都是单一类型的单个对象。
名为 `descending` 的函数模板也可以比较这两种元素类型，但它的名字代表的是一组函数族，没有单一类型，因此相同的调用会因 `no matching function for call to 'sort'` 而失败。

初始代码中的两个 lambda 仅针对 `int` 编写，因此 driver.cpp 会在 `largestOr(words, fallback)` 处报错 `no matching function for call to object of type`，并且在标准库的 `algorithm` 头文件内部还会出现更多错误，因为 `std::sort` 在那里使用两个字符串调用了 `descending`。
一旦两个 lambda 都接受 `const auto&` 参数，这些错误就都会消失。

- `descending(a, b)` 是 `std::sort` 用于将较大元素排在前面的比较函数：`{3, 1, 2}` 排序为 `{3, 2, 1}`，而 `{"b", "a", "c"}` 排序为 `{"c", "b", "a"}`。
- `largestOr` 以 `[](const auto& values, const auto& fallback)` 开头，并返回 `values` 中的最大元素，若 `values` 为空则返回 `fallback`。
  driver.cpp 使用一个 `std::vector<int>` 和一个 `int`，以及一个 `std::vector<std::string>` 和一个 `std::string` 来调用它。
  两个 vector 都具有 `empty()` 和 `front()`，且两种元素类型都支持 `<`。
  `std::string` 上的 `<` 是逐字符比较的，因此 `{"pear", "zoo", "apple"}` 返回 `"zoo"`，尽管 `"apple"` 更长且排在最后。

从 `fallback` 开始搜索看似省去了非空检查，对于 `{3, 9, 2}` 且 fallback 为 0 会返回 9，对于空 vector 且 fallback 为 -1 会返回 -1。
但一旦每个元素都小于 fallback，就会出错：`{-5, -2}` 且 fallback 为 0 会返回 0（vector 中并不包含该值），而不是 -2。
只有在没有元素可供搜索时，fallback 才用来代替答案。

### 解答

```cpp
#pragma once
#include <vector>

// 空 vector 返回 fallback，否则返回最大元素
const auto largestOr = [](const auto& values, const auto& fallback) {
    if (values.empty()) {
        return fallback;
    }
    auto largest = values.front();
    for (const auto& value : values) {
        if (largest < value) {
            largest = value;
        }
    }
    return largest;
};

// 较大的元素排在前面
const auto descending = [](const auto& a, const auto& b) { return b < a; };
```
