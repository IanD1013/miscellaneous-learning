成员的类型本身也可以是一个类，这就是如何由各自遵守自身规则的各个部分构建出更大类型的方式：

```cpp
class Clock {
public:
    Clock(int start) : minutes_(start) {}

    int minutes() const {
        return minutes_;
    }

private:
    int minutes_;
};

class Session {
public:
    Session(int start) : started_(start) {}

    int startMinute() const {
        return started_.minutes();
    }

private:
    Clock started_;
};
```

`started_` 是一个类类型的成员。
它在 `Session` 的构造函数体开始执行之前完成构造，因此其参数放在成员初始化列表中：`: started_(start)`。
`Clock` 没有无参构造函数，这使得初始化列表成为构建该成员的唯一位置：如果没有它，编译器会因为未初始化 `started_` 而拒绝 `Session` 的构造函数，根本不会执行到函数体。
拥有一个 `Clock` 成员也不会赋予对其内部的额外访问权限。
`minutes_` 是私有的，因此 `Session` 通过 `minutes()` 来查询，这与其他任何调用方使用的公开成员函数相同。

### 持有 Range 而不是两个 int

`Range` 已经为你编写完毕：`low_` 和 `high_` 是私有的，并且当传入的值位于该区间内（包含两端边界）时，`bool contains(int value) const` 返回 true。

- 为 `Selector` 添加一个 `Range allowed_;` 成员，并在构造函数的成员初始化列表中与 `count_(0)` 一同完成构建。
- `offer` 通过 `allowed_.contains(value)` 向该成员发起判断，并且仅在结果为 true 时增加计数。
  你的解答中必须出现 `allowed_.contains(`。
- 不要将 `low` 和 `high` 复制为 `Selector` 的成员。
  同一规则保留两份副本可能会导致不一致，而且负责该规则的类已经在维护它了。
- 当 `low` 大于 `high` 时不包含任何内容，因此接受的数量为 0。
  空的 `values` 同样会得到 0。
  这两种情况都不属于错误，也不会被拒绝。
- `acceptedCount` 和 `accepted()` 已经编写完毕，它们报告的计数即为用于评分的值。

### 解答

```cpp
#include <vector>

class Range {
public:
    Range(int low, int high) : low_(low), high_(high) {
    }

    bool contains(int value) const {
        return value >= low_ && value <= high_;
    }

private:
    int low_;
    int high_;
};

class Selector {
public:
    Selector(int low, int high) : allowed_(low, high), count_(0) {
    }

    void offer(int value) {
        // 交给 Range 成员判断，只有在范围内才计数
        if (allowed_.contains(value)) {
            count_ += 1;
        }
    }

    int accepted() const {
        return count_;
    }

private:
    Range allowed_;
    int count_;
};

struct Solution {
    static int acceptedCount(int low, int high, const std::vector<int> &values) {
        Selector selector(low, high);
        for (int value : values) {
            selector.offer(value);
        }
        return selector.accepted();
    }
};
```
