在类主体内编写的函数是成员函数，其函数体可以直接使用该类的私有成员，无需传入任何参数：

```cpp
class Tally {
public:
    void bump(int amount) {
        count_ += amount;
    }

    int count() {
        return count_;
    }

private:
    int count_ = 0;
};
```

`bump` 写入 `count_`；`count` 返回它。
两者都位于 `public:` 之下，这种放置决定了谁可以调用它们，而不是它们可以访问什么。
位于 `private:` 之下的函数仍然可以被 `Tally` 内部的其他代码调用，并且仍然可以写入 `count_`，但类外部的代码则完全无法再访问它。

每个成员函数都是在对象上调用的，对象名称位于点号的左侧。
`tally.bump(3)` 在 `tally` 上运行 `bump`，并且其函数体所访问的成员均属于该对象。
即使括号内没有任何内容，圆括号也是调用的一部分，因此 `tally.count()` 是对应的数值，而 `tally.count` 则是在预期为数字的地方写下的函数名，编译器会报错拒绝。
在类外部单独编写裸露的 `bump(3)` 也会被拒绝：因为它没有可运行的对象，而且在 `Tally` 外部，名称 `bump` 根本不在作用域内。
此引擎只能独立调用自由函数和静态函数，这就是为什么评分函数是构建并驱动该对象的地方。

完成 `Counter` 及其驱动函数：

- `add` 为私有累计总和增加一个数值，因此三次传入 7 的调用会留下 21 而不是 7。
- `total()` 返回该成员。
  `add` 返回 `void`，因此评分数值没有其他来源。
- `sumAmounts` 接收 `const std::vector<int> &amounts`，构建一个 `Counter`，通过 `counter.add(amount)` 依次向其传递每个元素，并返回 `counter.total()`。
- 空 vector 返回 0，这也是该成员的初始值，且数值可能会重复或为负数。
- `accumulate` 已被禁用，并且这两个通过对象进行的调用必须出现在文件中。

## 解答

```cpp
#include <vector>

class Counter {
public:
    void add(int amount) {
        // 把这个数加到私有的累计总和上
        total_ += amount;
    }

    int total() {
        return total_;
    }

private:
    int total_ = 0;
};

struct Solution {
    static int sumAmounts(const std::vector<int> &amounts) {
        Counter counter;
        // 依次把每个数交给对象，最后报告它的总和
        for (int amount : amounts) {
            counter.add(amount);
        }
        return counter.total();
    }
};
```
