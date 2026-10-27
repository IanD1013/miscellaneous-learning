在构造函数的参数列表与左大括号之间，冒号引出一个以逗号分隔的列表，用于为每个成员赋予初始值：

```cpp
class Rectangle {
public:
    Rectangle(int width, int height)
        : width_(width), height_(height), area_(width_ * height_) {
    }

    int area() {
        return area_;
    }

private:
    const int width_;
    const int height_;
    const int area_;
};
```

每个条目指定一个成员，并将其值放在括号中。
在 `width_(width)` 中，括号内的名称会被查找为参数，因此成员可以从拼写几乎相同的参数中获取其值，并且大括号之间的函数体可以保持为空。

该列表并不是相同赋值操作的更整洁写法。
在列表中指定的成员只会被初始化一次，而在函数体中赋值的成员会先被初始化，随后再被覆盖；并且声明为 `const` 的成员只有一次获取值的机会：在声明中带有 `const` 时，函数体内的 `width_ = width;` 根本无法通过编译。
该初始化列表是唯一可行的方式。

条目的书写顺序并不起决定作用。
成员是按照类主体中自上而下的声明顺序进行初始化的，这就是为什么 `area_` 声明在它所读取的两个成员之后。
如果颠倒了这个顺序，`area_` 就会将两个尚未持有值的成员相乘，并存储一个看似合理但错误的数值。
关于成员顺序的编译器信息并不会阻止当前运行环境，因此对象将保留该错误数值。

`Increase` 保存基础金额（base amount）、百分比率（percentage rate）以及两者计算出的总和（total）。
在对象的整个生命周期中，这三者都是固定不变的，因此请将这三者都声明为 `const`，第一个成员确切拼写为 `const int base_;`，并在列表中为每一个成员赋值：`base_(base)`，比率以相同方式赋值，总和则为 `base + base * rate / 100`（从构造函数的参数中读取，其中乘法在除法之前执行，除法向零截断）。
`baseRateAndTotal` 构建一个 `Increase` 对象并在 vector 中按顺序返回三个数字：base、rate 以及 `increase.total()`。
rate 介于 0 到 200 之间，base 介于 -10000 到 10000 之间。
rate 为 0 时 base 保持不变，rate 为 150 时正数 base 会增加到两倍以上，而负数 base 则保持其正负号。

## 解答

```cpp
#include <vector>

class Increase {
public:
    Increase(int base, int rate)
        : base_(base), rate_(rate), total_(base + base * rate / 100) {
    }

    int base() {
        return base_;
    }

    int rate() {
        return rate_;
    }

    int total() {
        return total_;
    }

private:
    const int base_;
    const int rate_;
    const int total_;
};

struct Solution {
    static std::vector<int> baseRateAndTotal(int base, int rate) {
        // 用两个值构建一个 Increase，并报告它保存的三个数字
        Increase increase(base, rate);
        return {increase.base(), increase.rate(), increase.total()};
    }
};
```
