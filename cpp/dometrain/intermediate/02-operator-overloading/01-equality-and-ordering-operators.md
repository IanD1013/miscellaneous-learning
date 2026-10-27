定义 `operator<` 就足以对结构体进行排序，因为不带比较器的 `std::sort` 仅使用 `operator<` 进行比较，`std::set` 也是如此；它们都绝不会调用 `operator==`。
直接比较两个日期的代码也会写成 `a == b`、`a != b` 或 `a >= b`，而 C++ 既不会为结构体自动编写这六个比较运算符，也不会相互推导：如果只定义了 `operator<`，`a > b` 将无法编译。
如果给这六个运算符中的每一个都分别编写逐个成员比较的函数体，你就会写出四份包含年、月、日顺序的代码副本；一旦修改了其中一份却遗漏了另一份，`a <= b` 和 `a > b` 可能会对同一对日期同时返回 true。
因此，请完整编写 `operator==` 和 `operator<`，并在此基础上构建其余四个运算符。

测试驱动代码（driver）会比较 `const` 日期，因此请确保每个非成员运算符的两个参数都为 `const Date&`。

`operator==` 仅在年、月、日全部匹配时才为 true。
`operator!=` 本身不比较任何成员：它返回 `!(a == b)`，这样相等性只在一处决定，两者绝不会产生冲突。

### 通过 operator< 进行排序

`<tuple>` 中的 `std::tie`（初始代码中已包含 `#include <tuple>`）可以将 `operator<` 简化为单次比较：

```cpp
std::tie(a.year, a.month, a.day) < std::tie(b.year, b.month, b.day)
```

`std::tie` 会返回一个包含你所列出成员引用的 tuple（tuple 是具有任意数量元素的 `std::pair`），两个 tuple 之间的 `<` 比较会先比较第一个元素，仅当它们相等时才会继续比较下一对。
第一个出现的不同之处将决定大小，因此列出成员的顺序就是它们的重要程度顺序。

两个相等的日期不存在差异，因此 `a < b` 和 `b < a` 均为 false。
其余三个顺序关系则是将 `operator<` 的参数调换、取反或两者兼有。
`a > b` 询问 `b` 是否早于 `a`，因此等价于 `b < a`。
`!(a < b)` 看起来像是同一个问题，但对于两个相等的日期它也为 true，而此时 `a > b` 必须为 false。
这就为 `operator<=` 和 `operator>=` 留下了取反形式以及调换参数后取反的形式；请推导哪种形式对应哪个运算符。

当两个日期彼此都不小于对方时，`std::set<Date>` 会将它们视为同一个日期，而 `a == b` 则调用 `operator==`。
只有当这两个运算符读取相同的三个成员时，它们对“哪些日期相同”的判断才会达成一致。
如果 `operator<` 仅比较年份，集合会将 2024 年 1 月 1 日和 1 月 2 日视为同一个日期。
如果 `operator==` 忽略了 `day`，1 月 9 日和 1 月 10 日会被判定为相等，但同时 `a < b` 也为 true。

### 编写内容

在 `date.hpp` 中实现这六个运算符。
`driver.cpp` 会从整型数据构建日期：

- `compareDates(y1, m1, d1, y2, m2, d2)` 以 1 或 0 返回一对日期的六个比较结果，顺序依次为 `==`、`!=`、`<`、`<=`、`>`、`>=`。
- `sortDates(flat)` 接受一个由年、月、日三元组组成的扁平化 vector，使用 `std::sort` 对日期进行排序，并以排序后的扁平化形式返回它们。
  空 vector 则返回 `[]`。
- `distinctDates(flat)` 从相同类型的输入构建一个 `std::set<Date>` 并返回其大小。

`Date` 没有日历合法性检查，因此 2 月 31 日也是一个普通的值。

### 解答

```cpp
#pragma once
#include <tuple>

struct Date {
    int year;
    int month;
    int day;
};

inline bool operator==(const Date& a, const Date& b) {
    // 三个成员全部相等
    return a.year == b.year && a.month == b.month && a.day == b.day;
}

inline bool operator!=(const Date& a, const Date& b) {
    return !(a == b);
}

inline bool operator<(const Date& a, const Date& b) {
    // 按年、月、日的顺序比较
    return std::tie(a.year, a.month, a.day) < std::tie(b.year, b.month, b.day);
}

inline bool operator>(const Date& a, const Date& b) {
    return b < a;
}

inline bool operator<=(const Date& a, const Date& b) {
    return !(b < a);
}

inline bool operator>=(const Date& a, const Date& b) {
    return !(a < b);
}
```
