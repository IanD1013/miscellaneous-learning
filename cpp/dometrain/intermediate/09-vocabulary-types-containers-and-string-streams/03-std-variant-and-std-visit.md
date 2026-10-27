`std::variant<int, ParseError>` 一次只保存一个值，要么是 `int`，要么是 `ParseError`，并记录当前保存的是两者中的哪一个。
列表中的每个类型都是一个 alternative。
variant 并不是一个同时拥有 `int` 成员和 `ParseError` 成员的 struct：当它保存 `int` 时，其内部根本不存在 `ParseError`。
这使它适合作为可能因多种原因失败的操作的返回类型。
`std::optional<int>` 只能表示值缺失；而 variant 还能说明原因。

```cpp
enum class ParseError { Empty, NotANumber, OutOfRange };
using ParseResult = std::variant<int, ParseError>;

ParseResult digitValue(char c) {
    if (c < '0' || c > '9') {
        return ParseError::NotANumber;
    }
    return c - '0';
}
```

`return` 根据其表达式的类型选择 alternative：`ParseError::NotANumber` 存储的是 `ParseError`，而 `c - '0'` 存储的是 `int`。

### 查询当前保存的是哪一个 alternative

读取 variant 有三种调用方式，它们在猜测错误时的行为有所不同：

```cpp
ParseResult r = digitValue('x');   // 保存的是 ParseError::NotANumber

std::holds_alternative<int>(r)     // false
std::get_if<int>(&r)               // nullptr
std::get_if<ParseError>(&r)        // 指向所保存的 ParseError 的指针
std::get<int>(r)                   // 在此运行环境中会终止程序
```

`std::get_if<int>` 接收 variant 的地址，并返回指向所保存的 `int` 的指针；当 variant 保存的是另一个 alternative 时，它返回 `nullptr`，因此对该指针的一次检查既能完成判断又能完成读取。
`std::get<int>` 则跳过了检查，因此只有在已经通过检查确认的情况下才可以使用它。

### 使用 std::visit 处理每个 alternative

`std::visit(visitor, v)` 会将 variant 中保存的值解包后传入 visitor 进行调用：传入的是 `int` 或 `ParseError`，绝不是 variant 本身。
visitor 是一个函数对象，当它为每个 alternative 都提供了一个 `operator()` 时，常规的重载决议（overload resolution）会挑选参数与所保存类型匹配的那一个。
visitor 内部不需要编写任何测试类型的逻辑。

```cpp
struct IsError {
    bool operator()(int) const { return false; }
    bool operator()(ParseError) const { return true; }
};

std::visit(IsError{}, digitValue('x'))   // true
std::visit(IsError{}, digitValue('7'))   // false
```

每个重载都必须返回相同的类型，并且每个 alternative 都需要一个重载。
无论 variant 在运行时保存什么，编译器都会为每个 alternative 构建调用代码，因此即使程序永远不会产生某个 alternative，缺少该重载的 visitor 也无法通过编译。
如果在 variant 中添加 `std::string` 作为第三个 alternative，那么访问它的每个 visitor 都会编译失败，直到为新类型添加了重载；而相比之下，一连串的 `std::get_if` 检查虽然能编译通过，但会遗漏新的分支。

### parse.hpp 必须定义的内容

初始代码只包含 include 指令。
`driver.cpp` 使用了下面列出的所有名称，因此在所有这些名称都存在之前，每个用例都会失败并在 `driver.cpp` 中报告编译错误，首先报出的会是 `unknown type name 'ParseResult'`。

- `ParseError` 和 `ParseResult`，与上方所示完全一致。
- `inline ParseResult parseCount(const std::string& text)`：对于 `""` 返回 `ParseError::Empty`；当任何字符不在 `'0'` 到 `'9'` 之间（包括正负号或空格）时返回 `ParseError::NotANumber`，即使文本过长无法存入 `int` 也是如此。
  否则返回该数值，或者当数值大于 `std::numeric_limits<int>::max()`（2147483647）时返回 `ParseError::OutOfRange`。
- `struct Describe`：包含 `std::string operator()(int value) const`（返回 `"value "` 后接该数字，例如 `"value 42"`），以及 `std::string operator()(ParseError error) const`（返回 `"error empty"`、`"error not a number"` 或 `"error out of range"`）。
- `inline std::string describe(const ParseResult& result)`：通过 `std::visit` 返回 `Describe` 对 `result` 给出的文本描述。
- `inline int countValid(const std::vector<std::string>& texts)`：返回文本列表中有多少个文本能够解析为 `int`。
- `inline int valueOr(const ParseResult& result, int fallback)`：返回所保存的 `int`；当 `result` 保存的是错误时，返回 `fallback`。

`"1o"`（数字 1 后面跟着字母 o）不是一个数字。
如果循环在遇到第一个不在 `'0'` 到 `'9'` 范围内的字符时停止并返回迄今读取到的数字，就会将其转换为数值 1，从而导致 `{"10", "1o", "007", "5"}` 的 `countValid` 返回 4 而不是 3。

边界是针对数值本身的：`"2147483647"` 可以成功解析，`"2147483648"` 则不行，而长达 12 个字符的 `"000000000042"` 其值为 42。
请自行转换数字，不要使用 `std::stoi` 或其他库转换函数。
在循环中通过 `value * 10 + digit` 构建数值时，可能会在途中超出边界，而有符号整数溢出是未定义行为（undefined behavior），因此在乘法之后再检查就太迟了。
在每次相乘之前，将 `value` 与 `std::numeric_limits<int>::max()` 减去该数字后再除以 10 的结果进行比较；这可以在不实际计算表达式的情况下，判断 `value * 10 + digit` 是否会超出边界。

在 `driver.cpp` 中，`Solution::describeParse` 返回 `parseCount(text)` 的描述，`Solution::validAndInvalid` 返回 `[valid, invalid]`（其中 `valid` 来自你的 `countValid`），而 `Solution::valueOr` 返回你的 `valueOr(parseCount(text), fallback)`。

在测试用例全部通过后，将类型别名改为 `std::variant<ParseError, int>`。
你的代码中有哪些行需要更改？
思考一下，然后运行它。

### 解答

```cpp
#pragma once
#include <limits>
#include <string>
#include <variant>
#include <vector>

enum class ParseError { Empty, NotANumber, OutOfRange };
using ParseResult = std::variant<int, ParseError>;

inline ParseResult parseCount(const std::string& text) {
    if (text.empty()) {
        return ParseError::Empty;
    }
    // 先检查所有字符，长文本中的非数字也算 NotANumber
    for (char c : text) {
        if (c < '0' || c > '9') {
            return ParseError::NotANumber;
        }
    }
    int value = 0;
    for (char c : text) {
        int digit = c - '0';
        // 相乘之前判断是否会超出边界
        if (value > (std::numeric_limits<int>::max() - digit) / 10) {
            return ParseError::OutOfRange;
        }
        value = value * 10 + digit;
    }
    return value;
}

struct Describe {
    std::string operator()(int value) const {
        return "value " + std::to_string(value);
    }

    std::string operator()(ParseError error) const {
        switch (error) {
            case ParseError::Empty:
                return "error empty";
            case ParseError::NotANumber:
                return "error not a number";
            case ParseError::OutOfRange:
                return "error out of range";
        }
        return "";
    }
};

inline std::string describe(const ParseResult& result) {
    return std::visit(Describe{}, result);
}

inline int countValid(const std::vector<std::string>& texts) {
    int valid = 0;
    for (const std::string& text : texts) {
        ParseResult result = parseCount(text);
        if (std::holds_alternative<int>(result)) {
            ++valid;
        }
    }
    return valid;
}

inline int valueOr(const ParseResult& result, int fallback) {
    if (const int* value = std::get_if<int>(&result)) {
        return *value;
    }
    return fallback;
}
```
