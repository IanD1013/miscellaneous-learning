在虚函数声明后加上 `= 0`，该函数就会变成纯虚函数（pure virtual）：类声明了它但没有给出实现。
即使只包含一个纯虚函数的类也是抽象类（abstract class），不能创建它的对象。
C++ 没有 `interface` 关键字；一个成员函数全为纯虚函数且带有虚析构函数的类，就是 C++ 代码实现接口的方式。

```cpp
class Encoder {
public:
    virtual ~Encoder() = default;
    virtual std::string encode(const std::string& text) const = 0;
};

Encoder plain;  // error: variable type 'Encoder' is an abstract class
```

纯虚函数不等于空函数。
如果给 `encode` 一个返回 `""` 的函数体，`Encoder` 就是一个普通类：`Encoder plain;` 可以编译通过，而一个忘记重写 `encode` 的编码器会运行基类版本并返回空文本。
若使用了 `= 0`，编译器会拒绝这两种程序。

派生类只有在重写了所继承的每一个纯虚函数之后，才会成为具体类（concrete），这意味着可以创建它的对象。
如果基类中有两个纯虚函数，只重写其中一个仍会使派生类保持抽象。
类定义本身仍然可以通过编译；错误会在创建该类对象的地方出现。
使用接口的代码会持有 `const Encoder&` 或 `const Encoder*`，通过它们调用 `encode` 会运行派生类的版本，就像任何虚函数一样。

### 使用 `final` 关闭类

```cpp
class ShiftEncoder final : public Encoder {
```

在类名后添加 `final` 会使从 `ShiftEncoder` 派生变为编译错误：`class DoubleShift : public ShiftEncoder` 会报错 `base 'ShiftEncoder' is marked 'final'`。
编写 `ShiftEncoder` 的目的就是为了通过接口使用它，而不是作为基类，因此 `final` 可以将意外的派生转化为编译错误。
它还会告诉阅读 `ShiftEncoder::encode` 的人，后续不会有类覆盖它。
如果改写在成员函数声明之后，例如 `std::string name() const override final`，则 `final` 说明符允许类继续被派生，但会阻止任何派生类重写该特定函数。
这两种形式都不会改变分发（dispatch）：通过指向 `ShiftEncoder` 的 `const Encoder*` 进行的调用仍然会执行 `ShiftEncoder::encode`。

### 需要编写的内容

在 `encoders.hpp` 中：

- `Encoder` 保留其虚析构函数，并声明两个纯虚函数：`std::string encode(const std::string& text) const` 和 `std::string name() const`。
- `ReverseEncoder` 和 `ShiftEncoder` 都标记为 `final` 并重写这两个函数。
- `ReverseEncoder::encode` 返回翻转后的文本，其 `name()` 返回 `"reverse"`。
- `ShiftEncoder::encode` 将每个字母 `a` 到 `z` 以及 `A` 到 `Z` 按位移量向后移动，并在其自身的大小写范围内回绕（`'Z'` 移动 1 位是 `'A'`），并保持所有其他字符不变。
  位移量是一个从 0 到 25 的数字。
  其 `name()` 返回 `"shift "` 加上位移量，例如 `"shift 25"`。
- `encodeAll(steps, text)` 依次将文本通过每个步骤进行处理并返回结果，如果没有步骤，则返回 `text` 本身。

初始代码目前还无法编译，因为 `driver.cpp` 通过 `const Encoder*` 调用了 `name()`，而 `Encoder` 没有声明 `name()`：`no member named 'name' in 'Encoder'`。

`driver.cpp` 中的 `Solution::hierarchyFacts()` 会报告关于你的类的四项事实，1 代表 true，0 代表 false。
对于已完成的类，以及给两个函数都提供了函数体而不是 `= 0` 的 `Encoder`，它会返回：

```text
                     [Encoder 是抽象类, ShiftEncoder 是 final, ReverseEncoder 是 final, ShiftEncoder 是抽象类]
已完成的类           [1, 1, 1, 0]
Encoder 中提供函数体 [0, 1, 1, 0]
```

在提供函数体的情况下，每个编码字符串和步骤名称都保持不变，因为两个编码器都重写了这两个函数，且 `Encoder` 中的函数体从未运行；第一位的 0 是该变化的唯一体现。

`Solution::encodeChain(text, shifts, reverseLast)` 为每个 shift 构建一个 `ShiftEncoder`，当 `reverseLast` 为 `true` 时在最后添加一个 `ReverseEncoder`，并返回 `encodeAll` 的返回值以及用 `">"` 连接的步骤名称：

```text
                                      [encodeAll 结果, 步骤名称]
encodeChain("Hello", {1, 2}, true)    ["roohK", "shift 1>shift 2>reverse"]
encodeChain("Hello", {1, 2}, false)   ["Khoor", "shift 1>shift 2"]
encodeChain("abc", {25}, false)       ["zab", "shift 25"]
```

两次位移总共将每个字母移动了三位，随后的翻转将移位后的 `H` 带到了 `"roohK"` 的末尾。

### 解答

```cpp
#pragma once
#include <string>
#include <vector>

class Encoder {
public:
    virtual ~Encoder() = default;
    virtual std::string encode(const std::string& text) const = 0;
    virtual std::string name() const = 0;
};

class ReverseEncoder final : public Encoder {
public:
    std::string encode(const std::string& text) const override {
        return std::string(text.rbegin(), text.rend());
    }
    std::string name() const override { return "reverse"; }
};

class ShiftEncoder final : public Encoder {
public:
    explicit ShiftEncoder(int shift) : shift_(shift) {}

    std::string encode(const std::string& text) const override {
        std::string result = text;
        for (char& c : result) {
            // 在各自的大小写范围内回绕
            if (c >= 'a' && c <= 'z') c = static_cast<char>('a' + (c - 'a' + shift_) % 26);
            else if (c >= 'A' && c <= 'Z') c = static_cast<char>('A' + (c - 'A' + shift_) % 26);
        }
        return result;
    }

    std::string name() const override { return "shift " + std::to_string(shift_); }

private:
    int shift_;
};

inline std::string encodeAll(const std::vector<const Encoder*>& steps, const std::string& text) {
    std::string result = text;
    for (const Encoder* step : steps) result = step->encode(result);
    return result;
}
```
