`class` 构建与 `struct` 相同类型的结构，但有一个区别改变了该类型的使用方式：在任何访问标签之前声明的成员都是私有的（private），因此类型外部的任何代码都不能引用它们。

```cpp
class Box {
public:
    int fill(int value) {
        contents_ = value;
        return contents_;
    }

private:
    int contents_ = 0;
};
```

`public:` 和 `private:` 是标签而不是声明。
每个标签都会设置写在它后面的每个成员的访问权限，直到出现下一个标签为止，因此单个 `public:` 可以覆盖多个成员。
公有成员（public member）可以被持有该对象的任何代码引用。
私有成员（private member）只能由写在该类型本身内部的代码引用，从外部尝试访问会在你的代码行停止编译，并指出它拒绝访问的成员。
`class` 的默认访问权限是 private，因此如果省略这两个标签，主体中的所有内容都会被隐藏。

`fill` 是写在类主体内部的函数，这就是为什么它自己的代码行可以直接引用 `contents_` 而无需传入任何内容。
持有 `Box` 的代码通过对象访问它，如 `box.fill(4)`，对象位于点号左侧，参数位于括号中。
右花括号后面的分号属于该类型，就像它在 struct 定义末尾的作用一样，省略它会导致编译停止。

一旦某个成员变为私有，之前的一种习惯做法就会失效。
具有私有成员的类型不能再从外部逐个成员进行填充，因此类似 `Box b{4};` 的花括号初始化会被拒绝；`Box b;` 随后进行调用才是传入值的方式。

将 `TextLine` 重写为 `class`。
将其文本保存在写在其专属 `private:` 标签下的成员中（尽管该关键字无论如何都会隐藏它，但本练习要求你写出来），并为该类型提供一个公有函数 `join`，接收 `const std::string &` 类型的 `left` 和 `right`，将 `left + right` 存储在该成员中并返回该成员当前保存的内容。
如果 `join` 直接返回拼接结果，则成员将不保存任何内容。
然后 `joinParts` 构建一个 `TextLine` 并返回 `line.join(left, right)`。
返回的文本会进行严格比较，因此内部空格和字母大小写都会决定答案，两个空部分将返回一个空字符串。
这里不拒绝任何字符串对。

## 解答

```cpp
#include <string>

// TextLine 的文本成员是私有的，只能通过公有成员函数 join 访问。
class TextLine {
public:
    std::string join(const std::string &left, const std::string &right) {
        // 把两段拼接后存进成员，再返回成员保存的内容
        text = left + right;
        return text;
    }

private:
    std::string text;
};

struct Solution {
    static std::string joinParts(const std::string &left, const std::string &right) {
        TextLine line;
        return line.join(left, right);
    }
};
```
