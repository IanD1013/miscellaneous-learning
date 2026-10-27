类可以通过其成员之一来拥有一个堆对象，而该成员是一个与普通成员一起声明的 `std::unique_ptr`：

```cpp
class Session {
public:
    Session(const std::string &label)
        : label_(label), hits_(std::make_unique<Tally>()) {
    }

    void record() { hits_->bump(); }
    int recorded() const { return hits_->total(); }

private:
    std::string label_;
    std::unique_ptr<Tally> hits_;
};
```

`std::unique_ptr<Tally> hits_;` 声明了一个具有所有权的成员。
仅仅声明它并不会构建任何对象，在有内容填充它之前，该成员不包含任何对象。
成员初始化列表是填充它的地方：`hits_(std::make_unique<Tally>())`，它在 `Session` 仍在构建时就将 `Tally` 放置就绪，因此之后的每个成员函数都可以依赖它。
在类内部的每次使用随后都通过 `hits_->` 进行。

清理工作是此类永远无需编写的部分。
销毁一个 `Session` 会随之销毁其所有成员，随着这一过程的发生，拥有所有权的成员会释放 `Tally`，因此不需要自定义析构函数。
添加 `~Session() { delete hits_; }` 会导致文件编译失败，因为该成员是一个所有者而不是原始指针。

你的起始代码提供了包含 `bump()` 和 `total() const` 的 `Counter`，以及已经将文本保存在普通成员 `text_` 中的 `DigitScan`。
在该文本旁边声明 `std::unique_ptr<Counter> seen_;`，在构造函数已有的初始化列表中填充它，在 `scanAll` 中对 `text_` 的每个数字计数一次，并通过 `seen_->total()` 从 `digitsSeen` 返回累计总数。
普通的 `Counter` 成员同样可以完成这些数字的计数；将其放在堆上是为了练习这种结构模式，并没有针对其提出任何运行速度上的优势。

`countDigits` 返回一个 `int`。
文本最多包含 60 个 ASCII 字符，且可能包含字母、空格和标点符号，因此请使用 `std::isdigit` 测试每个转换为 `unsigned char` 的字符值，正如第 8.4 课所规定的规则。
代码中不能出现 `new` 或 `delete`，这不会带来任何麻烦：初始化列表是创建 `Counter` 的地方，而其成员拥有该对象的类没有任何需要显式释放的内容。
没有数字的文本返回 0，空字符串返回 0，`"40506"` 返回 5。

## 解答

```cpp
#include <cctype>
#include <cstddef>
#include <memory>
#include <string>

class Counter {
public:
    void bump() {
        total_ = total_ + 1;
    }

    int total() const {
        return total_;
    }

private:
    int total_ = 0;
};

class DigitScan {
public:
    DigitScan(const std::string &text)
        : text_(text), seen_(std::make_unique<Counter>()) {
    }

    void scanAll() {
        // 遍历 text_，每遇到一个数字就计数一次
        for (std::size_t i = 0; i < text_.size(); i++) {
            if (std::isdigit(static_cast<unsigned char>(text_[i]))) {
                seen_->bump();
            }
        }
    }

    int digitsSeen() const {
        return seen_->total();  // 返回所拥有的 Counter 记录的累计数
    }

private:
    std::string text_;
    // 本对象拥有的 Counter 放在文本旁边。普通成员同样能计数；放在堆上是为了练习这种结构，而不是出于速度考虑。
    std::unique_ptr<Counter> seen_;
};

struct Solution {
    static int countDigits(const std::string &text) {
        DigitScan scan(text);
        scan.scanAll();
        return scan.digitsSeen();
    }
};
```
