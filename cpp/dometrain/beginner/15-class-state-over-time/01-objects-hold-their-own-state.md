到目前为止，写入类中的每个成员都属于单个对象。
每个对象在被构造的瞬间都会获得属于自己的一份成员副本，并且这些副本的生命周期与持有它们的对象完全一致：

```cpp
class Meter {
public:
    Meter(int start) : reading_(start) {}

    void bump() {
        reading_ += 1;
    }

    int reading() const {
        return reading_;
    }

private:
    int reading_;
};

Meter left(4);
Meter right(4);
left.bump();
```

`left` 和 `right` 是使用相同的参数构建的，此时程序中持有两个对象，每个对象都有自己的 `reading_`，而不是在它们之间共享一个。
`left.bump()` 作用于位于 `left` 内部的副本，因此 `left.reading()` 返回 5，而 `right.reading()` 返回 4。
在 `bump` 内部，名称 `reading_` 指的是发起调用的那个对象的成员；该函数中不存在用于引用第二个对象成员的名称，因为唯一能访问到的对象就是发起调用的那个对象。
没有任何机制会通知 `right` 在 `left` 上发生了什么，也没有这个必要。

一个从未被调用过任何方法的对象也不是空白的。
它的成员保存着构造函数放入的内容，这也是为什么 `right` 会报告它构建时的初始值 4。

编写具有相同三个部分的 `Tally` 类：一个接受一个 `int` 初始总和的构造函数，一个用于将存储的总和增加该数量的 `void add(int amount)`，以及一个用于返回该总和的 `int total() const`。
总和本身保持私有（private）。

然后实现 `tallyTotals`。
构建 `Tally first(firstStart);` 和 `Tally second(secondStart);`，将 `firstAmounts` 中的每个数字传递给 `first.add(amount)`，并将 `secondAmounts` 中的每个数字传递给 `second`，最后返回一个恰好包含两个条目的 `std::vector<int>`，即 `first.total()` 然后是 `second.total()`。
你的答案中必须同时出现 `.add(` 和 `.total()`。
数量和起始总和的范围为 -1000 到 1000，且任一列表都可能为空，此时该对象将保留其构造函数所存储的初始数值。

## 解答

```cpp
#include <vector>

class Tally {
public:
    Tally(int start) : total_(start) {}

    void add(int amount) {
        total_ += amount;
    }

    int total() const {
        return total_;
    }

private:
    int total_;
};

struct Solution {
    static std::vector<int> tallyTotals(int firstStart, const std::vector<int> &firstAmounts, int secondStart, const std::vector<int> &secondAmounts) {
        // 每个列表各建一个 Tally，分别累加后报告两个总和
        Tally first(firstStart);
        Tally second(secondStart);
        for (int amount : firstAmounts) {
            first.add(amount);
        }
        for (int amount : secondAmounts) {
            second.add(amount);
        }
        return {first.total(), second.total()};
    }
};
```
