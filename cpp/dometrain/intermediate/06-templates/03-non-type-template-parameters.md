模板参数不一定必须是类型。
将其声明为 `int Bins`，它就会接受一个值，因此每次使用该模板时都会提供一个常量，例如 `Histogram<10>`。
这就是非类型模板参数（non-type template parameter）：

```cpp
template <int Bins>
class Histogram {
    static_assert(Bins > 0, "a Histogram needs at least one bin");
public:
    static constexpr int bins() { return Bins; }
private:
    std::array<int, Bins> counts_{};
};

Histogram<10> scores;  // counts_ 是一个 std::array<int, 10>
Histogram<4> ratings;
```

在类内部，`Bins` 是一个常量表达式，即编译器在编译时已知的值，因此它可以在任何可以使用 `constexpr` 值的地方生效：

- 它用于确定 `std::array` 成员的大小，因此每个 `Histogram<10>` 都在对象内部保存其 10 个计数。
- 它是 `static_assert` 的条件，程序所使用的每个值都会对其进行检查。
  `Histogram<0>` 会以 `static_assert failed due to requirement '0 > 0' "a Histogram needs at least one bin"` 终止构建。
  该错误指向 `static_assert` 所在行，而不是编写 `Histogram<0>` 的那一行，因此错误信息必须明确说明出了什么问题。
- `bins()` 是 `static constexpr`：`Histogram<10>::bins()` 可以在没有对象的情况下返回 10，并且结果本身就是一个常量。

该值是类型的一部分。
`Histogram<10>` 和 `Histogram<4>` 是不同的类型，就像 `std::array<int, 10>` 和 `std::array<int, 4>` 一样，因此 `scores = ratings;` 会因 `no viable overloaded '='` 而失败。
类型在编译时就已确定，因此参数必须是常量表达式。
`constexpr int` 变量符合条件。
而函数参数则不符合，即使每个调用方都传入 10：在 `int f(int n)` 内部，`Histogram<n>` 会因 `non-type template argument is not a constant expression` 而失败。

将大小作为构造函数参数看起来是相同的设计，但该参数仅在程序运行时才存在。
它无法确定 `std::array` 的大小，也不能出现在 `static_assert` 中，因此存储必须变成可动态增长的 `std::vector`，并且所有大小的缓冲区都会共享同一种类型。

### 任务

在 `recent.hpp` 中，编写 `template <typename T, int Capacity> class RecentValues`，用于保存最新推入其中的 `Capacity` 个值，包含以下 public 成员：

- `void push(const T& value)` 存储 `value`。
- `int size() const` 返回存储的值的数量，绝不会超过 `Capacity`。
- `std::vector<T> oldestFirst() const` 按从最旧到最新的顺序返回存储的值；在任何 push 之前返回一个空 vector。
- `static constexpr int capacity()` 返回 `Capacity`。

将这些值存储在 `std::array<T, Capacity>` 中，并使用 `static_assert` 拒绝小于或等于 0 的容量。

一旦数组满了，push 会覆盖最旧的值，而不是将所有存储的值向下移动一位。
以下是 `RecentValues<int, 3>` 在依次 push 1 到 5 后的状态。
`array` 列按顺序展示元素 0、1 和 2，`_` 表示尚未写入的元素，`oldest` 是保存最旧值的元素的索引：

```text
push   array        oldest   size()   oldestFirst()
1      [1, _, _]    0        1        [1]
2      [1, 2, _]    0        2        [1, 2]
3      [1, 2, 3]    0        3        [1, 2, 3]
4      [4, 2, 3]    1        3        [2, 3, 4]
5      [4, 5, 3]    2        3        [3, 4, 5]
```

从第四次 push 开始，只有位于 `oldest` 处的元素会发生改变，并且 `oldest` 向前移动一位。
因此该类需要跟踪两个数字：最旧值的索引以及存储的值的数量，并对每个位置进行 `% Capacity` 操作，使其从最后一个元素回绕到元素 0。
在第五次 push 之后，`oldestFirst()` 会读取元素 2、0 和 1。

`driver.cpp` 将值列表分别推入 `RecentValues<int, 3>`、`RecentValues<int, 1>` 和 `RecentValues<std::string, 5>` 中，并返回各自的 `oldestFirst()`。
列表可以为空或短于容量。
它还会返回 `RecentValues<int, 4>::capacity()`，而 `sizeAfter(pushes)` 会将 1 到 `pushes` 推入 `RecentValues<int, 3>` 并返回其 `size()`。
最后，`sizeDifference()` 返回 `sizeof(RecentValues<int, 5>) - sizeof(RecentValues<int, 3>)`。
由于值保存在 `std::array` 成员中，较大的对象多包含两个 `int`，因此差值为 8 字节。
而 `std::vector` 成员则会得出 0：vector 将其元素保存在堆上，因此 `RecentValues<int, 5>` 和 `RecentValues<int, 3>` 的大小会相同。

### 解答

```cpp
#pragma once
#include <array>
#include <vector>

template <typename T, int Capacity>
class RecentValues {
    static_assert(Capacity > 0, "RecentValues needs a capacity of at least 1");
public:
    void push(const T& value) {
        if (size_ < Capacity) {
            // 未满：写到最旧值之后的第 size_ 个位置
            values_[(oldest_ + size_) % Capacity] = value;
            ++size_;
        } else {
            // 已满：覆盖最旧值，最旧索引前移
            values_[oldest_] = value;
            oldest_ = (oldest_ + 1) % Capacity;
        }
    }
    int size() const { return size_; }
    std::vector<T> oldestFirst() const {
        std::vector<T> result;
        for (int i = 0; i < size_; ++i) {
            result.push_back(values_[(oldest_ + i) % Capacity]);
        }
        return result;
    }
    static constexpr int capacity() { return Capacity; }

private:
    std::array<T, Capacity> values_{};
    int oldest_{};
    int size_{};
};
```
