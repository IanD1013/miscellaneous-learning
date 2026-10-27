`template <typename T> class RunningTotal` 声明了一个类模板：它是根据类型 `T` 编写的一个定义，编译器会为你尖括号中指定的每种类型生成一个具体的类。
在类主体内定义成员函数：

```cpp
template <typename T>
class RunningTotal {
public:
    void add(const T& value) { total_ = total_ + value; }
    T total() const { return total_; }

private:
    T total_{};
};

RunningTotal<int> sums;
RunningTotal<std::string> joined;
```

`RunningTotal<int>` 和 `RunningTotal<std::string>` 是两个独立的类，各自拥有属于自身类型的 `total_`。
执行 `joined = sums;` 会报错 `no viable overloaded '='`，就像在任意两个互不相关的类之间进行赋值一样。

对函数模板的调用可以根据其实参推导出 `T`。
而 `RunningTotal<int> sums;` 没有传入任何实参，因此无法推导 `T`，声明中必须显式指明它。

编译器仅在代码调用成员函数时，才会针对给定的 `T` 生成该成员函数的主体，因此只要一个类型缺少某个成员函数所需的操作，它仍然可以与其他成员函数正常配合使用。
例如 `RunningTotal<std::vector<int>> lists;` 可以正常编译，`lists.total()` 也是如此。
只有在第一次调用 `lists.add(...)` 时，编译器才会在 `add()` 内部的 `+` 处报错 `invalid operands to binary expression`，因为 `std::vector` 没有 `+` 运算符。

`total_{}` 将总和初始化为 `T{}`：对于 `int` 是 0，对于 `std::string` 是空字符串。
这正是总和的正确初始值，因为加上 0 或追加空字符串不会产生任何改变。

### 追踪最小值和最大值

在 `range.hpp` 中，编写类模板 `RunningRange`。
它一次接收一个值，并在不存储这些值本身的情况下，记录它已处理的值的数量以及迄今为止的最小值和最大值。
它的公共成员函数包括：

- `void add(const T& value)` 记录一个值。
  每次调用都计入，包括重复的值。
- `int count() const` 返回调用 `add()` 的次数。
- `std::optional<T> lowest() const` 和 `std::optional<T> highest() const` 返回已添加的最小值和最大值；如果尚未添加任何内容，则返回空的 `std::optional<T>`。

仅使用 `<` 比较值，以便 `RunningRange` 可以适用于任何支持 `<` 且可拷贝的 `T`。

对于边界值来说，`T{}` 是错误的初始值。
它是一个真实的值，而不是“暂无数据”：如果下限从 0 开始，那么依次添加 4 和 9 后，它永远不会改变，并且 `lowest()` 会返回 0，一个从未被添加过的数字。
`std::numeric_limits<T>::max()` 可以修复 `int` 的这个问题，但 `std::numeric_limits` 只对算术类型提供真正的极值。
对于 `std::string`，其 `max()` 返回空字符串，并且没有任何字符串比它更小，因此无论添加什么单词，下限都会保持为空字符串。
没有任何初始值适用于所有的 `T`，所以第一个添加的值应该同时设置两个边界；在此之前，两端都没有值，这正是空的 `std::optional<T>` 的含义。

`driver.cpp` 会创建 `RunningRange<int>` 和 `RunningRange<std::string>`，按顺序添加每个列表，并对每个包含值的对象返回 `count()` 以及随后的 `*lowest()` 和 `*highest()`。
`wordRange` 会将计数输出为文本。
正常工作的 `RunningRange` 会输出：

```text
positions                            [count(), lowest, highest]

intRange({4, -2, 9, 9})              [4, -2, 9]
intRange({7})                        [1, 7, 7]
intRange({})                         [0]
wordRange({"pear", "apple", "fig"})  ["3", "apple", "pear"]
```

### 解答

```cpp
#pragma once
#include <optional>

template <typename T>
class RunningRange {
public:
    void add(const T& value) {
        ++count_;
        // 第一个值同时设置两个边界
        if (!lowest_ || value < *lowest_) {
            lowest_ = value;
        }
        if (!highest_ || *highest_ < value) {
            highest_ = value;
        }
    }
    int count() const { return count_; }
    std::optional<T> lowest() const { return lowest_; }
    std::optional<T> highest() const { return highest_; }

private:
    int count_{};
    std::optional<T> lowest_;
    std::optional<T> highest_;
};
```
