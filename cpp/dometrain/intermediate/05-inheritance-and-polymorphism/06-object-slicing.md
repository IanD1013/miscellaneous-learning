`HexFormatter` 重写了 `Formatter` 的虚函数 `format`，然而两个均始于同一 `hex` 对象的调用却返回了不同的字符串：

```cpp
HexFormatter hex;
Formatter copy = hex;
const Formatter& same = hex;

copy.format(255);  // "255"
same.format(255);  // "0xff"
```

`same` 引用了 `hex` 本身，因此虚调用会到达 `HexFormatter::format`。
`copy` 是一个独立的 `Formatter` 对象。
`Formatter` 的拷贝构造函数构建了它，而该构造函数接受一个 `const Formatter&`，因此它只能看到 `hex` 的基类部分：即每个 `HexFormatter` 中包含的 `Formatter`。
将派生类对象拷贝到基类对象中只会保留该基类部分，其余部分均被丢弃。
这被称为对象切片（slicing）。
被切片的副本执行虚调用时会运行 `Formatter::format`，因为已经不存在可供 `virtual` 调用的 `HexFormatter`。
被切片的 `PaddedFormatter` 也会丢失其存在于基类部分之外的 `width_`。

任何从派生类对象构建新 `Formatter` 的代码行都会对其进行切片：

- 无论 `Formatter` 的拷贝开销多么小、多么廉价，声明为 `Formatter formatter` 的形参在函数体运行之前都会从实参的基类部分进行构造。
- 向 `std::vector<Formatter>` 中 `push_back` 会从基类部分创建一个新的 `Formatter` 元素，即使该对象是通过引用传入的也是如此。
- `std::make_unique<Formatter>(formatter)` 会在堆上创建同样的切片副本。

为了保留派生类的行为，应该引用调用者的对象而不是拷贝它。
对于函数来说，`const Formatter&` 形参可以做到这一点。
由于 `std::vector` 不能容纳引用，必须访问原始对象的容器会将它们的地址保存在 `std::vector<const Formatter*>` 中，通过 `&formatter` 获取每个地址，并通过 `->` 进行调用。
这里的 `const` 必不可少，因为 `const Formatter&` 的地址是 `const Formatter*`。

存储指针使 `Report` 成为非拥有型（non-owning）对象。
它绝不会删除格式化器，且只要 `Report` 还在调用 `row`，调用者就必须保证每个格式化器保持存活；通过指向已销毁格式化器的指针调用 `format` 是未定义行为（undefined behavior）。
仅通过引用和指针使用的基类也可以删除其拷贝构造函数和拷贝赋值运算符，从而使切片拷贝无法通过编译。
此处的 `Formatter` 保持可拷贝，是因为 `driver.cpp` 故意对其进行了一次拷贝。

### 修复 report.hpp

这三个格式化器类已经实现完毕。
`Formatter` 以十进制写入数值，`HexFormatter` 写入 `"0x"` 和小写十六进制数字，而 `PaddedFormatter(width)` 会添加前导零直至达到 `width` 宽度，且绝不会截断更长的数字。
找出起始代码中将格式化器拷贝到 `Formatter` 中的每一处位置，使调用改为直接访问调用者的对象：

- `formatOnce(formatter, value)` 返回调用者的格式化器针对 `value` 返回的内容。
- `addColumn(formatter)` 添加一个引用调用者格式化器的列，绝不能添加其副本。
  `row(value)` 保留起始代码的输出格式：按列添加的顺序排列各列的结果，以 `" | "` 连接；当没有列时返回空字符串。

`driver.cpp` 在其 `Report` 之前声明了 `HexFormatter`、`PaddedFormatter` 和 `Formatter`，因此它们会在 `Report` 之后被销毁。
`reportRow(kinds, width, value)` 会为每种类型（`"hex"`、`"padded"` 或 `"plain"`）添加一列并返回 `row(value)`。
对于 `reportRow({"hex", "padded", "plain"}, 6, 255)`，各列依次为 `HexFormatter`、`PaddedFormatter(6)` 和 `Formatter`：

```text
Report 存储列的方式                     row(255): hex | padded | plain
std::vector<Formatter>（起始代码）      "255 | 255 | 255"
std::vector<const Formatter*>           "0xff | 000255 | 255"
```

`formatOnceWith(kind, width, value)` 返回单次 `formatOnce` 调用的结果。
`slicedCopy(value)` 执行上面所示的 `Formatter copy = hex;` 拷贝并返回其格式化结果。

### 解答

```cpp
#pragma once
#include <string>
#include <vector>

class Formatter {
public:
    virtual ~Formatter() = default;
    virtual std::string format(int value) const { return std::to_string(value); }
};

class HexFormatter : public Formatter {
public:
    std::string format(int value) const override {
        const std::string digits = "0123456789abcdef";
        unsigned int rest = static_cast<unsigned int>(value);
        std::string hex;
        do {
            hex = digits[rest % 16] + hex;
            rest /= 16;
        } while (rest > 0);
        return "0x" + hex;
    }
};

class PaddedFormatter : public Formatter {
public:
    explicit PaddedFormatter(int width) : width_(width) {}
    std::string format(int value) const override {
        std::string text = std::to_string(value);
        while (static_cast<int>(text.size()) < width_) text = "0" + text;
        return text;
    }

private:
    int width_;
};

// 按引用传参，避免切片
inline std::string formatOnce(const Formatter& formatter, int value) { return formatter.format(value); }

class Report {
public:
    // 保存调用者对象的地址，而不是副本
    void addColumn(const Formatter& formatter) { columns_.push_back(&formatter); }

    std::string row(int value) const {
        std::string line;
        for (std::size_t i = 0; i < columns_.size(); ++i) {
            if (i > 0) line += " | ";
            line += columns_[i]->format(value);
        }
        return line;
    }

private:
    std::vector<const Formatter*> columns_;
};
```
