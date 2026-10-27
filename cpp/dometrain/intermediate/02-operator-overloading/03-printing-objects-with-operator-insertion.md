一旦存在一个左侧接收流、右侧接收 `Amount` 的 `operator<<`，`std::cout << amount` 就可以编译了。
成员运算符总是将其所属的类作为左操作数，因此作为 `Amount` 的成员，它会被调用为 `amount << std::cout`，而你无法向 `std::ostream` 添加成员。
`operator<<` 是一个非成员函数，它优先接收流作为参数：

```cpp
inline std::ostream& operator<<(std::ostream& out, const Amount& amount) {
    out << amount.hundredths();
    return out;
}
```

`std::cout << "Amount: " << a << '\n'` 的组合方式为 `((std::cout << "Amount: ") << a) << '\n'`。
每个 `<<` 返回它写入的流，下一个 `<<` 接着向该流写入，因此 `return out;` 才能让换行符接在 `a` 后面。
`operator+=` 也是通过以引用方式返回 `*this` 来实现链式操作的，这里的返回类型是 `std::ostream&`，因为流是无法复制的。
如果将其设为 `void`，`<< '\n'` 的左侧就没有流了，driver.cpp 将无法编译。

只向 `out` 写入内容。
它是调用者放在左侧的任意流，因此 `std::cerr << a` 会将 `a` 输出到错误流 `std::cerr`。
如果运算符在内部显式指定了 `std::cout`，则无论调用者使用什么流，它都会打印到 `std::cout`。

### 使用 `std::setw` 和 `std::setfill` 进行填充

`std::setw(2)` 将下一次插入操作填充到至少两个字符，而 `std::setfill('0')` 设置填充字符（即构成填充的字符）。
它们都来自 `<iomanip>`，且 amount.hpp 已经包含了 `#include <iomanip>`。
它们的有效持续时间并不相同：

```cpp
std::cout << std::setfill('0') << std::setw(2) << 7 << ' ' << 7 << '\n';   // 07 7
std::cout << std::setw(3) << 5 << '\n';                                    // 005
```

宽度设置仅对第一个 7 生效，随后便恢复为零。
填充字符则会一直保持为 `'0'`，直到有其他操作修改它，因此在该流后面的任意位置执行 `std::setw(3) << 5` 都会打印出 `005`。
因此，调用 `std::setfill` 的运算符应该保存原先发现的填充字符（可能不是空格），并在返回前恢复该字符。
`out.fill()` 返回当前的填充字符，而 `out.fill(c)` 用于设置它：

```cpp
const char saved = out.fill();
// 使用 std::setfill('0') 进行填充输出
out.fill(saved);
```

### 拆分数值

`Amount` 将百分之一存储在 `int` 中：1205 输出为 `12.05`，7 输出为 `0.07`，-50 输出为 `-0.50`。
`/ 100` 得到整数部分，`% 100` 得到百分位部分。
整数除法向零截断，`%` 给出相应的余数：`-50 / 100` 是 `0`，而 `-50 % 100` 是 `-50`。
如果符号来自整数部分，-50 会输出为 `0.50`；如果百分位部分保留自己的符号，则会输出为 `0.-50`。
因此，`-` 取决于完整数值，而具体数字则来自去除了符号的两个部分。

在拆分数值前将其转为正数对于某一个 `int` 会失败。
最大的 `int` 是 2147483647，因此 -2147483648 没有对应的正 `int` 可以转换，取反会导致溢出。
对完整数值使用 `std::abs(amount.hundredths())` 或诸如 `v < 0 ? -v : v` 的条件表达式都是相同的取反操作，并且会以相同的方式溢出。
请先拆分：`-2147483648 / 100` 是 `-21474836`，`% 100` 是 `-48`，这两个部分都可以安全取反。
由这两个 `int` 部分构建文本，不要转换为 `double`。

### 需要编写的内容

在 amount.hpp 中的 `Amount` 之后添加 `operator<<`；在添加之前，driver.cpp 在打印 `Amount` 的每一行都会报错 `invalid operands to binary expression`。
对于负金额，该运算符先打印 `-`，然后是整数部分、一个 `.`，以及使用 `std::setfill('0')` 和 `std::setw(2)` 填充为恰好两位的百分位部分。
必须能够正确打印所有 `int`，包括取值范围的两个端点值。
请自行对各部分取反，而不是调用 `std::abs`。

这次 driver.cpp 中的 `printAmounts` 不返回任何内容：它打印到 `std::cout` 的行将与预期输出进行比对。
每个值单独占一行，先是 `Amount: `，接着是你编写的运算符生成的文本。
在打印所有这些内容之前，它会将 `std::cout` 的填充字符设置为 `*`，因此你的运算符开始时的填充字符并不是空格。
最后一行来自 `std::cout << "Padded: [" << std::setw(3) << 5 << "]"`，并且输出必须为 `Padded: [**5]`；它展示了你的运算符留在 `std::cout` 上的填充字符：

```text
保存并恢复填充字符        Padded: [**5]
填充字符停留在 '0'          Padded: [005]
填充字符被重置为空格      Padded: [  5]
```

### 解答

```cpp
#pragma once
#include <iomanip>
#include <ostream>

class Amount {
public:
    explicit Amount(int hundredths) : hundredths_(hundredths) {}

    int hundredths() const {
        return hundredths_;
    }

private:
    int hundredths_;
};

inline std::ostream& operator<<(std::ostream& out, const Amount& amount) {
    const int value = amount.hundredths();
    // 先拆分，再分别取反，避免溢出
    int whole = value / 100;
    int cents = value % 100;
    if (value < 0) {
        out << '-';
        whole = -whole;
        cents = -cents;
    }
    const char saved = out.fill();
    out << whole << '.' << std::setfill('0') << std::setw(2) << cents;
    // 恢复原来的填充字符
    out.fill(saved);
    return out;
}
```
