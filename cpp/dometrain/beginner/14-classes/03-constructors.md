构造函数（constructor）是在对象创建时自动运行一次的成员函数，在任何其他代码访问该对象之前执行。
它的名称与类名完全一致，并且不声明任何返回类型，即使是 `void` 也不行：

```cpp
class Point {
public:
    Point(int x, int y) {
        x_ = x;
        y_ = y;
    }

    int x() {
        return x_;
    }

    int sum() {
        return x_ + y_;
    }

private:
    int x_ = 0;
    int y_ = 0;
};

Point corner(3, 4);
```

`Point corner(3, 4);` 创建了该对象并将 3 和 4 传递给构造函数，就像任何函数调用按位置匹配实参与形参一样，因此 `corner` 从创建的第一行起就立即可用。
构造函数位于 `public:` 下，因为创建对象的代码位于类外部。
它的函数体将每个形参赋值给保存它的成员变量，成员变量命名为 `x_` 和 `y_` 是为了区分这两个名称：在函数体内部，`x` 是形参，因此写成 `x = x;` 会将形参赋值给其自身，从而使 `x_` 永远保持为 0。

有两种写法看起来像是在创建对象，但实际上并不是。
给构造函数指定返回类型会被直接拒绝，该行会报错 `constructor cannot have a return type`。
而 `Point corner();` 实际上声明了一个不接受任何参数并返回 `Point` 的函数，因此通过 `corner` 编写的第一次调用会失败，并报错提示类型错误而非对象错误。
一旦一个类声明了自己的任何构造函数，`Point corner;` 也会无法通过编译，因为类中不再存在不带参数的构造函数。

为 `Interval` 编写一个接收 `start` 和 `end` 并保存两者的构造函数，然后完成它已声明的两个查询函数：`start()` 返回创建该对象时传入的起始值，而 `difference()` 返回 `end` 减去 `start` 的结果。
`startAndDifference` 根据其两个参数创建一个 `Interval` 对象，并在一个 vector 中返回两个条目：首先是 `span.start()`，其次是 `span.difference()`，这两个值都应当通过向该对象查询获取，而不是在对象外部计算得出。
传入的两个值介于 -1000 到 1000 之间，不会有任何一对值被拒绝或重新排序：两个相等的值对应的差值为 0，负的起始值保持为负，若起始值为 9 且结束值为 2 则差值为 -7，因为减法运算是按照构造函数存储的顺序进行的。

## 解答

```cpp
#include <vector>

class Interval {
public:
    Interval(int start, int end) {
        // 在构造时保存两个值，让对象从第一行起就可用
        start_ = start;
        end_ = end;
    }

    int start() {
        return start_;
    }

    int difference() {
        return end_ - start_;
    }

private:
    int start_ = 0;
    int end_ = 0;
};

struct Solution {
    static std::vector<int> startAndDifference(int start, int end) {
        // 用两个值创建一个 Interval，并向它查询两个数字
        Interval span(start, end);
        return {span.start(), span.difference()};
    }
};
```
