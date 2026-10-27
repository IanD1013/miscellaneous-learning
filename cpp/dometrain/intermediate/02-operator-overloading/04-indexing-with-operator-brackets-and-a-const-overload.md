在类对象上调用 `arr[i]` 会以 `i` 作为参数调用其成员 `operator[]`。
要使 `arr[i] = 5` 或 `arr[i] += 1` 能够修改 `arr`，该函数必须返回对所存储元素的引用：

```cpp
int& operator[](int index)
```

调用者通过其返回的 `int&` 进行写入。
若将返回类型声明为普通的 `int`，调用者获取的将是一个临时副本，从而导致驱动程序中的 `arr[index] += 1` 无法通过编译并报错 "expression is not assignable"。

`SparseArray` 仅在从索引到值的 `std::map<int, int> cells_` 中保留被写入过的索引。
所有其他索引都保存传递给构造函数并保存在 `fill_` 中的填充值，并且不占用条目：稀疏数组正是通过将未使用的索引排除在 map 之外来存储填充值的。
对全新索引的写入操作始于该填充值。
map 自身的 `operator[]` 会返回与 key 关联的值的引用；当 map 中不存在该 key 时，它会先插入一个值为 0 的条目。
因此，如果用于写入的重载函数仅返回 `cells_[index]`，全新的索引就会从 0 开始；它必须在返回引用之前将填充值存入缺失的索引下。

### const 重载

通过 `const SparseArray& view` 你只能调用 `const` 成员函数，而上面的运算符并不是 const 成员函数，因此 `view[3]` 会报错 "no viable overloaded operator[] for type 'const SparseArray'"。
通过 `view` 进行读取需要第二个 `operator[]`，在其参数列表之后带有 `const`：

```cpp
int operator[](int index) const
```

两者都接受一个 `int` 参数，因此正是末尾的 `const` 将它们区分开来。
编译器会在 const 对象上或通过 const 引用调用这一个重载，并在非 const 对象上调用 `int&` 重载。
这意味着在非 const 的 `arr` 上调用 `arr[3]` 时，即使你只是读取结果，也会走写入重载，并为 3 添加一个条目。

在 const 重载内部，`cells_` 也是 const 的。
map 的 `operator[]` 具有插入功能，因此 const map 不提供此操作，在此处使用 `cells_[index]` 会报错 "no viable overloaded operator[] for type 'const std::map<int, int>'"。
`find` 永远不会执行插入；将它的结果与 `end()` 进行比较，即可区分已存储的索引和缺失的索引。
`at` 在这里没有帮助，因为对于缺失的索引它没有条目可以返回。
按值返回 `int`：此重载仅执行读取操作，而且返回值可以直接作为缺失索引的填充值，其背后无需存在实际元素。

### 需要编写的内容

`sparse.hpp` 最初包含构造函数和一个返回 0 的 `stored()`。
添加两个 `operator[]` 重载并完成 `int stored() const`，后者返回 `cells_` 容纳的条目数（无论值是多少，每个被写入的不同索引计为一个）。
`driver.cpp` 同时使用了这两个重载，因此在它们实现之前，构建会在此中断并报错 "type 'SparseArray' does not provide a subscript operator"。

任何 `int` 都是有效索引，包括负数和两个极值。
`driver.cpp` 中的 `Solution::writeThenRead(fill, writes, reads)` 构建了 `SparseArray arr(fill)`，对 `writes` 中的每个索引执行 `arr[index] += 1`，绑定 `const SparseArray& view = arr`，并对 `reads` 中的每个索引累加 `view[index]`。
数组存储的每个值以及读取的总和都能容纳在 `int` 中。

`writeThenRead(10, {3, 3, 7}, {3, 7, 9})` 会在索引 3 下存储 12，在索引 7 下存储 11。
通过 `view` 读取 9 会将填充值 10 累加到总和中，且不会向 map 添加条目。
结果包含读取的总和，随后是 `stored()` 的返回值：

```text
[33, 2]
```

在 "read a negative index twice" 中，填充值为 -3，索引 -5 被写入一次，然后被读取两次。
该测试用例应该返回哪一对值？

### 解答

```cpp
#pragma once
#include <map>

class SparseArray {
public:
    explicit SparseArray(int fill) : fill_(fill) {}

    int& operator[](int index) {
        // 新索引先存入填充值
        auto it = cells_.find(index);
        if (it == cells_.end()) {
            it = cells_.emplace(index, fill_).first;
        }
        return it->second;
    }

    int operator[](int index) const {
        // 只读，不插入
        const auto it = cells_.find(index);
        return it == cells_.end() ? fill_ : it->second;
    }

    int stored() const {
        return static_cast<int>(cells_.size());
    }

private:
    std::map<int, int> cells_;
    int fill_;
};
```
