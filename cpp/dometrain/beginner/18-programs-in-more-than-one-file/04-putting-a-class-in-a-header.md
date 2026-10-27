如果一个类需要被多个文件使用，则应将其放在头文件中，并且每个方法都直接在类主体中定义：

```cpp
#pragma once

class Meter {
public:
    Meter(int start) : reading_(start) {}

    void bump() { reading_ += 1; }

    int reading() const { return reading_; }

private:
    int reading_;
};
```

首先是包含保护指令（guard），然后 `class Meter {` 开启类主体，直到闭合的 `};` 之间的所有内容都属于该类。
`public:` 开启了一个任何代码都可以访问的区域，`private:` 则开启了一个只有该类自身的方法才能访问的区域。
访问修饰符标签在下一个标签出现之前一直有效，这使得其下方的数据成员处于无法直接访问的状态。
这里的每个方法都与声明一起定义，因此任何包含该头文件的文件都可以构建一个 `Meter` 并在其上调用 `bump()`，无需添加其他内容。
在类主体内部定义的方法会自动成为内联（inline），这就是为什么即使在头文件中的普通函数需要 `inline` 的规则仍然对其适用的情况下，这些方法体上方也没有任何关键字的原因。

`int reading() const` 参数列表后面的 `const` 使其成为一个 const 成员函数，这是一种承诺，保证调用它不会对对象进行任何更改。
正是这一承诺允许通过 `const Meter &` 进行调用；如果去掉它，此类调用将无法通过编译。

你将编辑 `Counter.hpp`。
`program.cpp` 是固定的，它在读取对象时将其保存为 `const Counter &`，并提供用于评分的 `valueAfter` 和 `limitReached`。
构造函数已经为你写好：它存储限制值，并将负数限制值转换为 0。
请完成其余部分。

- `add(int amount)` 忽略小于或等于零的 amount。
  否则累加总数将增加 `amount`，但会在达到限制值时精确停止，因此在限制为 10 的情况下，`{3, 4, 9}` 最终结果为 10，绝不会是 16。
- `int value() const` 返回当前的累加总数：在限制为 10 的情况下，`{5, -2, 0, 1}` 返回 6，空列表则返回 0。
- 一旦总数达到限制，`bool atLimit() const` 为 `true`，而在低于限制时为 `false`。
  限制为 0 时不接受任何增加，使总数保持在 0。
- 将 `count_` 和 `limit_` 放在 `private:` 标签下。
  虽然 `class` 在没有任何标签的情况下也会将其成员保持为私有，但运行前的检查需要读取该文件中的标签本身。
  请保持类型为 `class`，因为 `struct` 已被禁用。

## 解答

```cpp
#pragma once

class Counter {
public:
    Counter(int limit) : count_(0), limit_(limit < 0 ? 0 : limit) {}

    void add(int amount) {
        // 忽略小于或等于零的 amount，并且累计总数绝不超过限制值
        if (amount <= 0) {
            return;
        }
        count_ += amount;
        if (count_ > limit_) {
            count_ = limit_;
        }
    }

    int value() const {
        return count_;
    }

    bool atLimit() const {
        return count_ >= limit_;
    }

private:
    int count_;
    int limit_;
};
```
