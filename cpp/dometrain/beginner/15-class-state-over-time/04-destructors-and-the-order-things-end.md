析构函数（destructor）是当对象的生命周期结束时编译器调用的成员函数。
它的名称是一个波浪号后接类名，它不接受任何参数，并且在通常放置返回类型的地方没有任何内容：

```cpp
class Handle {
public:
    Handle() {
    }

    ~Handle() {
    }
};
```

没有任何代码会显式调用 `~Handle()`。
它会在该对象生命周期结束时自动运行；对于局部对象而言，其生命周期的终点就是声明它的代码块的右闭花括号。
在同一个代码块中声明的对象会按相反的顺序销毁，即后构造的先销毁：

```cpp
{
    Handle one;
    Handle two;
}
```

`two` 在该闭合花括号处结束生命周期，然后是 `one`。
嵌套代码块比外层函数更早结束，因此在嵌套代码块中声明的对象在该代码块之后编写的任何内容被创建之前就已经销毁了。

对象本身的结束不会打印任何内容，因此观察顺序的唯一方法是让构造函数和析构函数写入一个比所有对象都存活得更久的内容中。
在 `Marker` 中，这就是 `record_`，一个 `static` 成员：在类中声明、在类下方定义，并且已经被构造函数追加了内容（构造函数会添加一个 `+` 和对象的标签）。
你的文件中只包含该类，没有其他内容。
编写 `~Marker()`，使其追加 `-` 和 `label_`。

这些对象是在 `blocks.cpp` 中构建的，你无法编辑该文件。
`buildAndEnd` 声明了 `Marker a("A")`，当数量为 2 时添加 `B`，当数量为 3 时添加 `B` 和 `C`；当 `nestMiddle` 为 true 时，`B` 位于一个在创建 `C` 之前就已关闭的代码块中。
`lifetimeRecord` 调用该函数，并且仅在其返回后才读取 `Marker::record()`，因为如果在 `lifetimeRecord` 本身中声明 `Marker`，它在计算返回值时仍然存活，其 `-` 标记将永远无法写入记录中。

在开始之前请先阅读该文件，因为它构建对象的顺序决定了你的析构函数必须生成的输出顺序。
当 `nestMiddle` 为 false 时，一个对象记录为 `+A-A`，两个对象记录为 `+A+B-B-A`，三个对象记录为 `+A+B+C-C-B-A`。
当 `B` 处于嵌套块中的三个对象记录为 `+A+B-B+C-C-A`。
数量小于 1 或大于 3 时不构建任何对象并返回 `none`，这在任何对象存在之前就已经确定。

## 解答

```cpp
#include <string>

class Marker {
public:
    Marker(const std::string &label) : label_(label) {
        record_ += "+";
        record_ += label_;
    }

    // 析构函数：对象生命周期结束时追加减号和标签
    ~Marker() {
        record_ += "-";
        record_ += label_;
    }

    static std::string record() {
        return record_;
    }

private:
    std::string label_;
    static std::string record_;
};

std::string Marker::record_ = "";
```
