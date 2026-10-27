起始代码中的 `plus` 接受两个 `Seconds`，然而这行调用却可以通过编译：

```cpp
int total = plus(2, Seconds{5}).count();
```

写下 `2` 的人本意是两分钟。
但编译器将其处理成了两秒，因此一旦 `plus` 将计数值相加，`total` 就是 7。
`Seconds(int count)` 可以只传入一个实参进行调用，且没有被标记为 `explicit`，这使得它成为了一个转换构造函数（converting constructor）：只要在期望 `Seconds` 的地方出现了一个 `int`，编译器就会替你调用它。
这种隐式转换会发生在函数实参、在返回 `Seconds` 的函数中的 `return 90;`，以及 `Seconds s = 90;` 中，而这些代码行本身都没有显式体现这一点。
`Minutes(int count)` 也会以相同的方式将 `int` 转换为 `Minutes`。

### 将构造函数标记为 explicit

在构造函数前面加上 `explicit`：

```cpp
class Seconds {
public:
    explicit Seconds(int count) : count_(count) {}
    int count() const { return count_; }

private:
    int count_;
};
```

explicit 构造函数不再是转换构造函数。
当代码明确指明类型时，它仍然会构建该对象，因此 `Seconds{90}` 和 `Seconds(90)` 仍会像以前一样编译通过。
只有隐式的用法被阻止了：`plus(2, Seconds{5})` 现在会因 `no matching function for call to 'plus'` 而失败，且 `Seconds s = 90;` 和 `return 90;` 会以开头的错误 `no viable conversion from` 失败。
`Seconds s = Seconds{90};` 也使用了 `=`。
想一想它在使用 explicit 构造函数时是否能编译，然后尝试将其作为 `plus` 的第一行并运行。

分钟仍然需要一种转换成秒的方式。
一个乘以 60 的构造函数 `Seconds(const Minutes& m)` 在算术逻辑上是正确的，但它也是一个转换构造函数：任何 `Minutes` 都会被隐式传递给 `plus`，而 `plus(m, s)` 会掩盖乘以 60 的这一步。
在 `Minutes` 上提供一个成员函数则将这一步骤显式地体现在调用中：`m.toSeconds()`。

### 编写内容

在 `durations.hpp` 中，将两个构造函数都设为 explicit，使 `Minutes::toSeconds()` 以 `Seconds` 的形式返回相同的时长（2 分钟即 120 秒），并使 `plus` 返回一个包含两个计数值之和的 `Seconds`。
`plus` 保留其两个 `Seconds` 参数。

`driver.cpp` 会报告 `plus(Minutes{minutes}.toSeconds(), Seconds{seconds}).count()`，因此 2 分钟和 5 秒应该报告 125。
所有的总和都能放入 `int` 中，所以你的类不需要进行范围检查。

驱动程序还会询问编译器 `int` 是否能转换为 `Seconds`、`int` 是否能转换为 `Minutes`，以及 `Minutes` 是否能转换为 `Seconds`。
这三个检查的答案都必须为 `false`。

### 解答

```cpp
#pragma once

class Seconds {
public:
    // explicit：禁止 int 隐式转换为 Seconds
    explicit Seconds(int count) : count_(count) {}
    int count() const { return count_; }

private:
    int count_;
};

class Minutes {
public:
    explicit Minutes(int count) : count_(count) {}
    int count() const { return count_; }
    // 在调用处显式体现乘以 60
    Seconds toSeconds() const { return Seconds{count_ * 60}; }

private:
    int count_;
};

inline Seconds plus(Seconds a, Seconds b) {
    return Seconds{a.count() + b.count()};
}
```
