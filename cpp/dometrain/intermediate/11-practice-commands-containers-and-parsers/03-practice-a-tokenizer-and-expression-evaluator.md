本练习将构建一个用于计算整数表达式（例如 `3 - 2147483647 - 2 * 2`）的求值器，并且它绝不会发生静默溢出。
你将在 `evaluator.hpp` 中编写两个函数：`tokenize(std::string_view text)` 将文本转换为 `std::vector<Token>`，而 `evaluate(const std::vector<Token>& tokens)` 计算其 `int` 值。
每个函数都在 `std::variant` 中返回其结果或一个 `EvalError`。
文本包含非负十进制字面量、`+ - * /`、括号和空格。
没有一元负号，因此负值只能由减法产生。
头文件已经声明了这两个类型：

```cpp
enum class EvalError { Empty, BadToken, Syntax, DivisionByZero, Overflow };
using Token = std::variant<int, char>;
```

`tokenize` 从前往后遍历视图，并在使用每个字符时通过 `remove_prefix` 缩短它。
空格会被丢弃，而 `+ - * / ( )` 中的每一个都会变成一个 `char` token。
一连串连续的数字会变成一个 `int` token。
你需要自己逐位构建它，而不是将文本交给库转换函数（例如 `std::stoi`、`std::strtol` 或 `std::from_chars`）或 `std::istringstream` 处理。
在执行 `value * 10 + digit` 之前，将 `value` 与根据 `std::numeric_limits<int>::max()` 和该数字计算出的界限进行比较，以确保比较本身也不会溢出。
统计数字位数不能作为限制依据，因为 `2147483647` 有十位且是有效字面量，而 `2147483648` 则返回 `EvalError::Overflow`。
任何其他字符都会返回 `EvalError::BadToken`。
从左侧遇到的第一个错误即为返回的错误。

### 优先级与结合性

如果严格从左向右求值，`2 + 3 * 4` 的结果将是 20。
`*` 和 `/` 的优先级高于 `+` 和 `-`，因此正确答案是 14。
相同优先级的运算符从左向右结合：`8 - 2 - 2` 是 `(8 - 2) - 2`，结果为 4，而将其结合为 `8 - (2 - 2)` 则会得到 8。
括号可以覆盖这两种规则。

递归下降解析器通过三个函数来实现这一点，每个级别对应一个函数：

```text
expression:  一个 term，然后是任意数量的  + term  或  - term
term:        一个 factor，然后是任意数量的  * factor  或  / factor
factor:      一个字面量，或  ( expression )
```

这些函数相互调用。
`expression` 调用 `term`，`term` 调用 `factor`，而以 `(` 开头的 factor 会再次调用 `expression` 处理括号内的内容，然后要求匹配 `)`。
这使得解析器具有递归性：当第一个 `expression` 仍在等待其 `term` 返回时，第二个 `expression` 调用已经开始运行。
使用 `std::stack` 自行维护待处理运算符栈的版本同样有效。

从左到右的结合性源于循环：`expression` 将已有的值与下一个 `term` 结合，然后进入下一轮循环。
如果 `expression` 在 `-` 的右侧调用了自身，那么 `8 - 2 - 2` 将变成右结合。

这三个函数共享 token vector 中的一个位置。
可以将它们作为保存 tokens 和位置的小型类的成员，或者将 `std::size_t&` 传递给自由函数。
每次调用都有其自己的局部变量，因此请将组合过程中的值保存在局部变量中：在 `1 + (2 + 3)` 中，外层的 `expression` 在局部变量中保存 1，而内层的调用在其自己的局部变量中计算出 5。
如果将当前值存储在成员变量中，它会被内层调用覆盖。
成员函数可以按任意顺序相互调用。
自由函数则需要在定义之前提供声明，因为它们中至少有一个会调用在更下方定义的函数；缺少声明时编译器会报错 `use of undeclared identifier`。

每个解析函数都返回 `std::variant<int, EvalError>`，与 `evaluate` 的返回类型相同。
当调用的结果包含错误时，请原样返回该错误，以便报告遇到的第一个问题。
使用 `std::get_if` 读取 token，或者仅在 `std::holds_alternative` 确认其持有的类型后再使用 `std::get`；对错误的类型使用 `std::get` 会终止程序。

`EvalError::Syntax` 涵盖所有格式错误的序列：缺少操作数（`2 *`）、连续两个字面量（`1 2`）、前导 `-`（`-3`）、空括号、缺少 `)` 的 `(`，以及完整表达式后遗留的 token（如 `1)`）。
对于空的 token vector，`evaluate` 返回 `EvalError::Empty`，这源于为空或仅包含空格的文本。

### 溢出

有符号 `int` 溢出属于未定义行为（undefined behavior），因此无法在计算出结果后再进行检查。
必须在运算执行之前，与 `std::numeric_limits<int>::max()` 和 `std::numeric_limits<int>::min()` 进行比较，绝不能与写死的数字字面量比较。

当 `b > 0` 时，`a + b` 发生溢出当且仅当 `a > std::numeric_limits<int>::max() - b`，且该减法本身不会溢出。
请针对 `b < 0` 推导出与 `min()` 对应的比较条件，然后再推导出针对 `-` 的两个比较条件。

`std::numeric_limits<int>::min()` 是 -2147483648，比最大值离零更远一个单位。
因此，写成 `-max()` 的下界会错误地拒绝 `0 - 2147483647 - 1`，而该式的结果恰好就是 `min()`。

对于 `*`，用一个界限除以其中一个操作数，并将另一个操作数与商进行比较，需要对每种符号组合分别进行比较。
`(0 - 46341) * 46341` 将是 -2147488281，低于 `min()`，因此应返回 `EvalError::Overflow`。
在可以容纳任意两个 int 乘积的 `long long` 中计算乘积，并将其与边界进行比较，这也是可行的。

除数为零时返回 `EvalError::DivisionByZero`。
除法自身存在一种溢出情况，因为 `min()` 没有对应的正数：`(0 - 2147483647 - 1) / (0 - 1)` 即为 `min() / -1`，其结果将是 2147483648，因此它会返回 `EvalError::Overflow`。
任何其他除法均向零截断，正如整数 `/` 一贯的表现。

### driver 的返回内容

`driver.cpp` 中的 `Solution::evaluateText` 会先调用 `tokenize`，再调用 `evaluate`，并返回 `"value "` 后接具体数字，或者返回 `"error empty"`、`"error bad token"`、`"error syntax"`、`"error division by zero"` 和 `"error overflow"` 之一：

```text
text                      evaluateText 返回值
"2 + 3 * 4"               "value 14"
"(2 + 3) * 4"             "value 20"
"8 - 2 - 2"               "value 4"
"(0 - 7) / 2"             "value -3"
"0 - 2147483647 - 1"      "value -2147483648"
"2147483647 + 1"          "error overflow"
"-3"                      "error syntax"
"   "                     "error empty"
```

### 解答

```cpp
#pragma once
#include <limits>
#include <string_view>
#include <variant>
#include <vector>

enum class EvalError { Empty, BadToken, Syntax, DivisionByZero, Overflow };
using Token = std::variant<int, char>;

inline std::variant<std::vector<Token>, EvalError> tokenize(std::string_view text) {
    constexpr int max = std::numeric_limits<int>::max();
    std::vector<Token> tokens;
    while (!text.empty()) {
        char c = text.front();
        if (c == ' ') {
            text.remove_prefix(1);
        } else if (c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')') {
            tokens.push_back(c);
            text.remove_prefix(1);
        } else if (c >= '0' && c <= '9') {
            // 逐位构建，乘加之前先检查是否会超过 max
            int value = 0;
            while (!text.empty() && text.front() >= '0' && text.front() <= '9') {
                int digit = text.front() - '0';
                if (value > (max - digit) / 10) return EvalError::Overflow;
                value = value * 10 + digit;
                text.remove_prefix(1);
            }
            tokens.push_back(value);
        } else {
            return EvalError::BadToken;
        }
    }
    return tokens;
}

namespace detail {

using Result = std::variant<int, EvalError>;

// 运算之前与边界比较，绝不让 int 溢出
inline Result combine(int a, char op, int b) {
    constexpr int max = std::numeric_limits<int>::max();
    constexpr int min = std::numeric_limits<int>::min();
    switch (op) {
    case '+':
        if ((b > 0 && a > max - b) || (b < 0 && a < min - b)) return EvalError::Overflow;
        return a + b;
    case '-':
        if ((b < 0 && a > max + b) || (b > 0 && a < min + b)) return EvalError::Overflow;
        return a - b;
    case '*': {
        // long long 能容纳任意两个 int 的乘积
        long long product = static_cast<long long>(a) * b;
        if (product > max || product < min) return EvalError::Overflow;
        return static_cast<int>(product);
    }
    default:
        if (b == 0) return EvalError::DivisionByZero;
        if (a == min && b == -1) return EvalError::Overflow;
        return a / b;
    }
}

class Parser {
public:
    explicit Parser(const std::vector<Token>& tokens) : tokens_(tokens) {}

    Result parse() {
        Result result = expression();
        // 完整表达式之后不能有剩余 token
        if (std::holds_alternative<int>(result) && pos_ != tokens_.size()) return EvalError::Syntax;
        return result;
    }

private:
    // 当前 token 是指定运算符时返回 true
    bool peekOperator(char op) const {
        if (pos_ >= tokens_.size()) return false;
        const char* c = std::get_if<char>(&tokens_[pos_]);
        return c != nullptr && *c == op;
    }

    // expression: term 后接任意个 + term 或 - term
    Result expression() {
        Result left = term();
        while (std::holds_alternative<int>(left) && (peekOperator('+') || peekOperator('-'))) {
            char op = std::get<char>(tokens_[pos_++]);
            Result right = term();
            if (std::holds_alternative<EvalError>(right)) return right;
            left = combine(std::get<int>(left), op, std::get<int>(right));
        }
        return left;
    }

    // term: factor 后接任意个 * factor 或 / factor
    Result term() {
        Result left = factor();
        while (std::holds_alternative<int>(left) && (peekOperator('*') || peekOperator('/'))) {
            char op = std::get<char>(tokens_[pos_++]);
            Result right = factor();
            if (std::holds_alternative<EvalError>(right)) return right;
            left = combine(std::get<int>(left), op, std::get<int>(right));
        }
        return left;
    }

    // factor: 字面量，或 ( expression )
    Result factor() {
        if (pos_ >= tokens_.size()) return EvalError::Syntax;
        if (const int* value = std::get_if<int>(&tokens_[pos_])) {
            ++pos_;
            return *value;
        }
        if (!peekOperator('(')) return EvalError::Syntax;
        ++pos_;
        Result inner = expression();
        if (std::holds_alternative<EvalError>(inner)) return inner;
        if (!peekOperator(')')) return EvalError::Syntax;
        ++pos_;
        return inner;
    }

    const std::vector<Token>& tokens_;
    std::size_t pos_ = 0;
};

}  // namespace detail

inline std::variant<int, EvalError> evaluate(const std::vector<Token>& tokens) {
    if (tokens.empty()) return EvalError::Empty;
    return detail::Parser(tokens).parse();
}
```
