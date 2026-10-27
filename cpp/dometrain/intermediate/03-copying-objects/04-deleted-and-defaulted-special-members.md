`UniqueSlot` 会打开 `slots.hpp` 中的八个 slot 之一，并且其析构函数会将其关闭。
根据三法则（rule of three），拥有该析构函数意味着也需要对拷贝操作给出对策；而对于一个作为其 slot 唯一持有者的对象来说，答案就是拷贝操作绝不能编译通过。
在拷贝构造函数的声明后写上 `= delete`：

```cpp
UniqueSlot(const UniqueSlot&) = delete;
```

这会将其变为弃置函数（deleted function）。
它仍然处于已声明状态，因此编译器不会自行生成对应版本，但任何调用它的代码行都会编译失败，并且错误信息中会指出它：

```cpp
UniqueSlot a(3);
UniqueSlot b = a;   // call to deleted constructor of 'UniqueSlot'
```

拷贝赋值运算符是一个独立的成员，并且编译器仍会生成它。
对已存在的 `UniqueSlot c` 执行 `c = a;` 会拷贝 `handle_`：`c` 所打开的 slot 永远不会被关闭，并且两个析构函数都会去关闭 `a` 的 slot，因此第二次关闭会计入 `badCloses()`。
拷贝赋值运算符也需要单独一行：

```cpp
UniqueSlot& operator=(const UniqueSlot&) = delete;
```

将这两者都弃置（delete）后，`UniqueSlot` 便变为不可拷贝（non-copyable），并且 `c = a;` 会报错 `overload resolution selected deleted operator '='`。
这两种错误都会在文件编译时出现在执行拷贝的代码行处，而绝不会在程序运行时出现。

### 找回默认构造函数

`Limits` 中的 `int low = 0;` 和 `int high = 100;` 是默认成员初始化器（default member initializer）：当构造函数未对其进行设置时，每个初始化器都会为其成员赋予初始值。
声明任何构造函数都会阻止编译器自动生成默认构造函数（即无实参调用的构造函数）。
`Limits` 声明了 `Limits(int low, int high)`。
当该类型没有默认构造函数时，编译像 `Limits limits;` 这样的声明会报错 `no matching constructor for initialization of 'Limits'`。

`Limits() = default;` 用于重新请求编译器生成其默认版本。
它会从每个成员的默认成员初始化器开始初始化，因此 `Limits limits;` 会持有 0 和 100。
它本身不会主动将任何内容置零：在 `Limits limits;` 中，没有初始化器的 `int` 成员将保持未初始化状态。
`Limits(5, 9)` 仍会执行双参数构造函数，其成员初始化列表会覆盖这两个默认值。

`= default` 也适用于拷贝构造函数、拷贝赋值运算符和析构函数，并且只有在编译器逐成员处理的版本符合要求时使用它才是正确的。
对于两个 `int` 来说确实如此，因此 `Limits` 保留了编译器生成的拷贝成员。

### 编写内容

在 `members.hpp` 中，让 `UniqueSlot` 变为不可拷贝，并使用 `= default` 找回 `Limits` 的默认构造函数。
保持其他成员不变，并让 `Limits` 保持可拷贝。
`driver.cpp` 调用了四个函数：

- `copyRules()` 返回编译器针对你的两个类型的四个问题的回答，1 表示是，0 表示否，顺序依次为：`UniqueSlot` 是否可以被拷贝构造、一个 `UniqueSlot` 是否可以赋值给另一个、`Limits` 是否可以在无实参的情况下构建，以及 `Limits` 是否可以被拷贝构造。
- `defaultLimits()` 构建 `Limits limits;` 并返回 `[low, high]`。
- `customLimits(low, high)` 构建 `Limits limits(low, high);` 并返回 `[low, high]`。
- `uniqueSlotLifetime(value)` 在内部作用域中创建一个持有 `value` 的 `UniqueSlot`，并从 slot 表中返回四个数值：`slot` 存在时的 `slot.value()` 和 `openSlots()`，以及其作用域结束后的 `openSlots()` 和 `badCloses()`。
  使用初始代码中的析构函数时，`uniqueSlotLifetime(7)` 会返回 `[7, 1, 0, 0]`。

### 解答

```cpp
#pragma once
#include "slots.hpp"

class UniqueSlot {
public:
    explicit UniqueSlot(int value) : handle_(openSlot(value)) {}

    ~UniqueSlot() {
        closeSlot(handle_);
    }

    // 唯一持有者：禁止拷贝
    UniqueSlot(const UniqueSlot&) = delete;
    UniqueSlot& operator=(const UniqueSlot&) = delete;

    int value() const { return readSlot(handle_); }

private:
    int handle_;
};

struct Limits {
    int low = 0;
    int high = 100;

    // 找回默认构造函数
    Limits() = default;
    Limits(int low, int high) : low(low), high(high) {}
};
```
