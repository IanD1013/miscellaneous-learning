派生类在冒号后指定其基类。
下面的 `StepCounter` 继承自 `counters.hpp` 中已有的 `Counter`，后者将其计数值保存在 `value_` 中：

```cpp
class StepCounter : public Counter {
public:
    StepCounter(int start, int step) : Counter(start), step_(step) {}
    void advance() { value_ += step_; }

private:
    int step_;
};
```

每个 `StepCounter` 对象都包含一个完整的 `Counter`（即其基类部分），以及与其并列的 `step_`。
`public` 保持了基类的公有成员依然是公有的，因此无需重新编写，`add()` 和 `value()` 即可直接作用于 `StepCounter`。
如果没有 `public`，`class` 默认以 private 方式继承，类外部的代码若在派生类对象上调用 `value()`，将会报错 `'value' is a private member of 'Counter'`。
`StepCounter` 也可以绑定到 `const Counter&` 参数，而该函数在另一侧只能看到 `Counter` 部分：它可以调用 `value()`，但不能调用 `advance()`。

### Protected 成员

`advance()` 会写入 `value_`，而 `StepCounter` 从未声明过该变量。
它之所以能这样做，是因为 `Counter` 将 `value_` 置于 `protected:` 下。
`Counter` 的成员函数可以使用 protected 成员，派生类的成员函数也可以在该派生类对象上使用它。
任何其他访问都会被拒绝，就如同 private 成员一样：类外部的函数若从 `StepCounter` 读取 `value_`，会收到 `'value_' is a protected member of 'Counter'`，而 `StepCounter` 的成员函数若通过 `const Counter&` 参数读取 `value_` 也是如此。
位于 `private:` 下的成员保留在其自身类内部，因此只有 `StepCounter` 的成员函数可以访问 `step_`，从 `StepCounter` 派生的类则不能访问。

### 构建基类部分

只有 `Counter` 的构造函数才能构建 `Counter` 部分，因此派生类的构造函数在其成员初始化列表中首先指明基类构造函数 `Counter(start)`，然后再初始化自己的成员。
`value_` 属于 `Counter`，因此在该列表中放置 `value_(start)` 会报错：`member initializer 'value_' does not name a non-static data member or base class`。
如果不为基类指定任何内容，编译器会尝试使用默认构造函数构建 `Counter` 部分，但 `Counter` 并没有默认构造函数：它唯一的构造函数是 `explicit Counter(int start)`。

### 编写内容

在 `counters.hpp` 中的 `Counter` 下方，编写 `class CappedCounter : public Counter`，即一个带上限的计数器。
它将计数值保存在继承来的 `value_` 中，该变量保持在 `protected:` 下，以便 `addCapped` 可以写入它。
只有 `addCapped` 会检查上限。
继承来的 `add()` 仍然是公有的，因此 `capped.add(50)` 会使计数超过上限。

- `CappedCounter(int start, int cap)` 将计数从 `start` 开始，并将溢出量初始化为 0。
- `void addCapped(int amount)` 增加 `amount`，同时不允许计数超过 `cap`。
  `amount` 中任何会导致超出的部分都会被累加到溢出量中。
- `int overflow() const` 返回到目前为止的溢出总量。
- 上限和溢出总量是私有成员，分别为 `cap_` 和 `overflow_`。

`driver.cpp` 中的 `Solution::runCapped(start, cap, amounts)` 构建 `CappedCounter capped(start, cap)`，按顺序使用每个数值调用 `addCapped`，并返回 `{capped.value(), capped.overflow(), readThroughBase(capped)}`，其中 `readThroughBase` 接收一个 `const Counter&` 并返回其 `value()`。

在下方的第一次调用中，前两个数值使计数达到 8，第三个数值只剩下容纳 2 的空间，因此其剩余的 2 进入溢出量。
另外两行是边界情况：增加量刚好达到上限，以及计数器从其上限开始。

```text
                               [value(), overflow(), readThroughBase(capped)]
runCapped(0, 10, {4, 4, 4})    [10, 2, 10]
runCapped(0, 10, {10})         [10, 0, 10]
runCapped(5, 5, {1})           [5, 1, 5]
```

在 `CappedCounter` 中再次声明 `int value_;` 并不能访问到继承来的成员。
它会添加第二个独立的 `value_`，并且在 `CappedCounter` 内部该名称现在指代的是新成员。
若从 `start` 设置该新成员，`runCapped(0, 10, {4, 4, 4})` 将返回 `[0, 2, 0]`。
溢出量是正确的，因为 `addCapped` 操作的是新成员。
但计数却不正确：`value()` 是 `Counter` 的成员函数，因此 `capped.value()` 和 `readThroughBase` 读取的都是基类部分的 `value_`，而它根本没有改变。

### 解答

```cpp
#pragma once

class Counter {
public:
    explicit Counter(int start) : value_(start) {}
    void add(int amount) { value_ += amount; }
    int value() const { return value_; }

protected:
    int value_;
};

class CappedCounter : public Counter {
public:
    CappedCounter(int start, int cap) : Counter(start), cap_(cap), overflow_(0) {}

    void addCapped(int amount) {
        // 剩余空间，超出部分计入溢出量
        int room = cap_ - value_;
        if (amount > room) {
            overflow_ += amount - room;
            value_ = cap_;
        } else {
            value_ += amount;
        }
    }

    int overflow() const { return overflow_; }

private:
    int cap_;
    int overflow_;
};
```
