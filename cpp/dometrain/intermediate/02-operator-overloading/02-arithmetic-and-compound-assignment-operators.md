`p += q` 会调用成员函数 `p.operator+=(q)`。
在函数内部，`other` 是 `q`，而 `*this` 是 `p`，即调用该函数的对象。
该函数会修改 `p`，然后通过引用返回 `*this`：

```cpp
Polynomial& operator+=(const Polynomial& other)
```

将 `Polynomial&` 作为返回类型时，`p += q` 的值就是 `p` 本身，这也使得链式调用能够继续对 `p` 进行操作：

```cpp
(p += q) += r;
```

第二个 `+=` 会作用于第一个 `+=` 返回的对象上，在这里就是 `p`，因此 `p` 最终变为这三者的和。
如果将返回类型声明为普通的 `Polynomial`，`return *this;` 会将 `p` 复制到一个临时对象中，这是一个在语句结束时销毁的未命名对象。
第二个 `+=` 就会将 `r` 加到该临时对象上，而 `r` 永远不会加到 `p` 中。
这两种版本都可以通过编译。
`operator-=` 具有相同的形式。

### 不同长度的系数

`Polynomial` 按从低到高的次幂顺序存储其系数，因此 `[1, 0, 2]` 表示 1 + 2x²。
操作数的长度可以不同，较短的操作数在其最后一个系数之后的位置均视为 0：`[1] + [0, 1]` 结果为 `[1, 1]`。
在减法中，较长的右操作数也是同理。
`[5]` 没有 x² 系数，因此 `[5] - [0, 0, 4]` 将该系数视为 0，结果为 `[5, 0, -4]`。
如果循环在较短长度处停止，则加法结果为 `[1]`，减法结果为 `[5]`，因为超出较短操作数末尾的部分既没有被相加也没有被相减。
当 `other` 是较短的操作数时，如果将循环运行到 `coefficients_.size()`，则会出现另一种错误：它会越界读取 `other` 的 vector。
这种越界读取是未定义行为（undefined behavior），可能会返回任意值，包括恰好使求和看起来正确的 0。

计算结果的长度也可能会变短。
`[1, 2, 3] + [-1, -2, -3]` 会抵消每一个系数，并存储为 `[0]`：最高次项系数绝不能为零，除非它是唯一的系数。
`[1, 2, 0]` 和 `[1, 2]` 是用两个不同 vector 表示的相同多项式，而比较 `coefficients_` 的 `operator==` 会认为它们不同，因此该类在每次修改后都会修剪（trim）掉末尾（高次项）的零。
仅修剪末尾部分：`[5, 0, -4]` 中的 0 是 x 的系数，它应当保留。
vector 构造函数也会进行修剪：由 `[4, 0, 0]` 构建的 `Polynomial` 存储为 `[4]`，而由空 vector 构建的多项式则存储为 `[0]`，与默认构造函数一样。

### 基于 `+=` 实现 `+`

`a + b` 必须保持 `a` 和 `b` 不变。
将 `operator+` 编写为一个非成员函数，并按值传递其左操作数：

```cpp
inline Polynomial operator+(Polynomial left, const Polynomial& right) {
    left += right;
    return left;
}
```

`left` 是专门为此次调用从 `a` 复制的新 `Polynomial`，因此 `+=` 可以随意修改它。
加法逻辑只存在于一处，即 `+=` 内部，并且 `+` 从不触及私有的 `coefficients_`，因此它没有理由成为成员函数。
其他参数类型会以不同的方式引发错误。
使用 `const Polynomial& left` 时，代码行 `left += right;` 无法通过编译，因为 `+=` 不是 `const` 成员函数。
使用 `Polynomial& left` 时可以通过编译，但会直接加到调用方的 `a` 中。
以相同的方式基于 `operator-=` 实现 `operator-`。

在运行之前，先推算一下当 `left` 由 `[1, 2, 0]` 构建且 `right` 由 `[3]` 构建时，执行 `left + right` 后 `left` 中保存的内容。
`driver.cpp` 中的 `leftAfterAdd` 正是返回这个值，因此运行结果将验证你的推算是否正确。

### 编写内容

`polynomial.hpp` 开头包含了两个构造函数、`coefficients()` 以及 `coefficients_` 成员。
请在类中添加 `operator+=` 和 `operator-=`，并在类后添加 `operator+` 和 `operator-`。

- vector 构造函数会修剪其输入，并保持 `explicit`。
- `operator+=` 和 `operator-=` 处理任意长度的操作数。
- `operator+` 和 `operator-` 通过 `+=` 和 `-=` 获取结果，而不是使用它们自己的循环。

`driver.cpp` 构建了 `Polynomial left(a)` 和 `Polynomial right(b)`，然后通过 `add` 返回 `left + right` 的系数，通过 `subtract` 返回 `left - right` 的系数，并通过 `leftAfterAdd` 返回加法后 `left` 本身的系数。
`chainedAdd` 在 `Polynomial p(a)` 上执行 `(p += Polynomial(b)) += Polynomial(c);` 并返回 `p` 的系数。
所有的和与差都可以用 `int` 容纳。

在所有四个运算符都实现之前，`driver.cpp` 无法编译：编译器会在 `left + right` 和 `left - right` 处报错 `invalid operands to binary expression ('Polynomial' and 'Polynomial')`，并在链式调用行处报错 `no viable overloaded '+='`。

### 解答

```cpp
#pragma once
#include <cstddef>
#include <vector>

class Polynomial {
public:
    Polynomial() : coefficients_{0} {}

    explicit Polynomial(const std::vector<int>& coefficients) : coefficients_(coefficients) {
        trim();
    }

    const std::vector<int>& coefficients() const {
        return coefficients_;
    }

    Polynomial& operator+=(const Polynomial& other) {
        // 较短的一方补 0
        if (coefficients_.size() < other.coefficients_.size()) {
            coefficients_.resize(other.coefficients_.size(), 0);
        }
        for (std::size_t i = 0; i < other.coefficients_.size(); ++i) {
            coefficients_[i] += other.coefficients_[i];
        }
        trim();
        return *this;
    }

    Polynomial& operator-=(const Polynomial& other) {
        if (coefficients_.size() < other.coefficients_.size()) {
            coefficients_.resize(other.coefficients_.size(), 0);
        }
        for (std::size_t i = 0; i < other.coefficients_.size(); ++i) {
            coefficients_[i] -= other.coefficients_[i];
        }
        trim();
        return *this;
    }

private:
    // 去掉末尾（高次项）的 0，至少保留一个系数
    void trim() {
        while (coefficients_.size() > 1 && coefficients_.back() == 0) {
            coefficients_.pop_back();
        }
        if (coefficients_.empty()) {
            coefficients_.push_back(0);
        }
    }

    std::vector<int> coefficients_;
};

inline Polynomial operator+(Polynomial left, const Polynomial& right) {
    left += right;
    return left;
}

inline Polynomial operator-(Polynomial left, const Polynomial& right) {
    left -= right;
    return left;
}
```
