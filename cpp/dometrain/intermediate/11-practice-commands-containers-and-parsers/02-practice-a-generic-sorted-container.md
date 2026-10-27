`SortedVector<T>` 是一个类模板，其唯一的成员是一个名为 `items_` 的 `std::vector<T>`，它始终保持升序且不存储重复值。
在其中进行的每次查找都可以是二分查找。

已编写了三个成员。
常量 `operator[]` 返回 `const T&`，因此调用者可以读取元素，但无法通过覆盖元素来破坏顺序。
它本身不进行检查：调用者需确保索引满足 `0 <= index < size()`。
`auto begin() const` 和 `auto end() const` 返回该 vector 自身的 const 迭代器，因此可以在不需要额外迭代器类的情况下对 `SortedVector` 使用基于范围的 for 循环（range-for）。

### 插入、查找与删除

`insert` 在成功添加值时返回 `true`，`erase` 在成功移除值时返回 `true`；否则它们各自返回 `false` 并保持容器不变。
`contains` 在值已存储时返回 `true`。
以 `{1, 3, 5}` 为例，以下是关键情况：

- 3 已被存储：`insert(3)` 返回 `false`，而 `contains(3)` 和 `erase(3)` 返回 `true`。
- 4 介于两个元素之间且不等于其中任何一个：`insert(4)` 得到 `{1, 3, 4, 5}`，而 `contains(4)` 和 `erase(4)` 返回 `false`。
- 9 大于每一个元素：`insert(9)` 得到 `{1, 3, 5, 9}`，而 `contains(9)` 和 `erase(9)` 返回 `false`。

### 相等性与拷贝

`operator==` 是一个非成员函数模板（free function template），因此它只能读取公有成员。
当两个容器包含相同的元素时，它返回 `true`。

编译器的拷贝构造函数会逐元素拷贝 `items_`，因此向副本中插入内容不会影响原容器。
这就是零法则（rule of zero）：不要声明这五个特殊成员函数中的任何一个。

### 任务

在 `sorted_vector.hpp` 中完成 `insert`、`contains`、`erase`、`size` 和 `operator==`。
`size()` 将元素数量作为 `int` 返回。
请使用二分查找（`std::lower_bound`、`std::upper_bound` 或 `std::binary_search`），而不是遍历元素的循环；并通过在正确的位置插入来保持 `items_` 有序，而不是在插入后对其排序或将元素存储在 `std::set` 中。

测试驱动程序（driver）通过按给定顺序插入值来构建每个 `SortedVector<int>` 或 `SortedVector<std::string>`。
`insertAll` 和 `insertWords` 返回容器内容，`rejectedCount` 统计返回 `false` 的插入次数，`afterErase` 从容器中删除其第二个列表中的各个值并返回剩余内容，`erasedCount` 统计返回 `true` 的删除次数，`sameContents` 使用 `==` 比较两个容器，`atIndex` 返回 `{c[index]}`。
`copyThenInsert(values, extra)` 拷贝容器，记录 `copy == original` 的结果，然后将 `extra` 插入到副本中。
它返回五个数字，其中 `true` 表示为 1，`false` 表示为 0：

```text
各位置                       [copy == original, original.size(), copy.size(), original.contains(extra), copy.contains(extra)]
copyThenInsert({1, 2}, 5)    [1, 2, 3, 0, 1]
```

### 解答

```cpp
#pragma once
#include <algorithm>
#include <vector>

template <typename T>
class SortedVector {
public:
    bool insert(const T& value) {
        // 二分查找插入位置，已存在则拒绝
        auto it = std::lower_bound(items_.begin(), items_.end(), value);
        if (it != items_.end() && *it == value) return false;
        items_.insert(it, value);
        return true;
    }
    bool contains(const T& value) const { return std::binary_search(items_.begin(), items_.end(), value); }
    bool erase(const T& value) {
        auto it = std::lower_bound(items_.begin(), items_.end(), value);
        if (it == items_.end() || *it != value) return false;
        items_.erase(it);
        return true;
    }
    int size() const { return static_cast<int>(items_.size()); }
    const T& operator[](int index) const { return items_[index]; }
    auto begin() const { return items_.begin(); }
    auto end() const { return items_.end(); }
private:
    std::vector<T> items_;
};

template <typename T>
bool operator==(const SortedVector<T>& a, const SortedVector<T>& b) {
    // 只能使用公有成员
    return std::equal(a.begin(), a.end(), b.begin(), b.end());
}
```
