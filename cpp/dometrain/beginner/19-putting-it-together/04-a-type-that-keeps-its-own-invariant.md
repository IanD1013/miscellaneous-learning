只要 `BoundedCounter` 存在，就必须始终满足一句话：它的值大于等于下界，且小于等于上界。
这句话就是不变式（invariant），并且进入该值的入口恰好只有两个，因此这两个入口在结束时都必须保证该条件依然成立。

将超出范围的数字限制回区间内需要进行两次比较：

```cpp
if (candidate < low) {
    candidate = low;
}
if (candidate > high) {
    candidate = high;
}
```

构造函数会对初始值执行此区间限制（clamp），但前提是在修复边界本身之后。
`high` 小于 `low` 描述了一个没有任何数字能够满足的区间，因此先将 `high` 收缩（collapse）到 `low` 会留下一个恰好只包含一个值的区间。
`add` 在存储 `value + amount` 之前，也会对其执行相同的限制。
初始代码直接将该和写入成员变量，这就是为什么该对象在第一次调用时会超出自身范围。

你编写的类对象无法直接返回给评测程序，因此验证方式是使用一个驱动程序（driver）：在一个静态函数中构建并驱动该类型，然后以一维 `std::vector<int>` 的形式返回读数。
该驱动程序已在 `driver.cpp` 中为你写好，它包含了你的头文件，并且你无法对其进行编辑。
它会构造计数器，立即记录 `value()` 的返回值，然后依次应用 `amounts` 中的每个增量，并在每次应用后记录结果。
驱动程序内部不会修复或限制任何值，因此落在边界内的每个读数都是通过 `BoundedCounter` 实现的。
第一个读数是构造函数是否执行了限制的唯一依据；在 `amounts` 为空的情况下，它就是完整的返回值。

给定 `low` 为 2、`high` 为 6、`start` 为 10 以及增量 `{-1, -9}`，读数将为 `{6, 5, 2}`：构造时将 10 拉低到 6，随后的 5 处于区间内保持不变，而 5 - 9 则被拉高回 2。

- `class BoundedCounter` 将 `low_`、`high_` 和 `value_` 保留在 `private:` 下，并将构造函数、`add` 和 `value` 放在 `public:` 下。
- `int value() const` 保持与初始代码完全一致。
  `const` 承诺此调用不会修改对象，这也就是它所承诺的全部内容。
- `BoundedCounter.hpp` 是你的文件，由 `#pragma once` 保护，且仅包含该类。
  `main` 作为标记被禁止使用，因为运行器会提供一个 `main`，并通过固定的文件调用 `driveCounter`。
- 用于评测的 `driveCounter(int low, int high, int start, const std::vector<int> &amounts)` 会返回构造后的值，然后按顺序返回应用每个增量后的值，因此空的增量列表仍会返回包含单个元素的向量。

## 解答

```cpp
#pragma once

class BoundedCounter {
public:
    BoundedCounter(int low, int high, int start) : low_(low), high_(high), value_(start) {
        // 如果上下界交叉，先把上界收缩到下界，再把初始值限制到区间内
        if (high_ < low_) {
            high_ = low_;
        }
        if (value_ < low_) {
            value_ = low_;
        }
        if (value_ > high_) {
            value_ = high_;
        }
    }

    void add(int amount) {
        // 先把和限制到区间内，再存储
        int candidate = value_ + amount;
        if (candidate < low_) {
            candidate = low_;
        }
        if (candidate > high_) {
            candidate = high_;
        }
        value_ = candidate;
    }

    int value() const {
        return value_;
    }

private:
    int low_;
    int high_;
    int value_;
};
```
