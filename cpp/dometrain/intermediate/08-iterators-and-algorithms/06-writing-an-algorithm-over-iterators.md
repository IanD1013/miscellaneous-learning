`std::find_if` 和 `std::copy_if` 适用于任何容器，因为它们接收的是迭代器对而不是容器本身。
当你将自己编写的算法写成基于迭代器类型的函数模板时，也能获得同样的通用性：

```cpp
template <typename It>
int countSteps(It first, It last) {
    int steps = 0;
    while (first != last) {
        ++steps;
        ++first;
    }
    return steps;
}
```

当使用 `std::vector<int>` 的迭代器调用 `countSteps` 时，`It` 会被推导为该 vector 的迭代器类型；而使用 `std::set<int>` 的迭代器调用时，则被推导为 set 的迭代器类型。
编译器会为每种类型分别生成一个 `countSteps`，并且函数内部没有指明任何具体的容器。

函数体只能使用调用它的所有迭代器都支持的操作：复制、使用 `++` 步进、使用 `*` 读取元素，以及使用 `==` 和 `!=` 比较两个迭代器。
Vector 和 string 的迭代器还支持 `first + 1`、`first[i]` 以及 `last - first`，因此对于 vector 来说，`return last - first;` 能得到相同的计数。
`std::set` 将每个元素保存在各自的节点中，其迭代器一次只能移动一个元素。
一旦使用 set 迭代器调用该模板，这三种操作中的任何一种都会在模板的对应行引发编译错误，导致整个程序编译失败。

`It` 在函数体内也代表该迭代器类型，因此 `It previous = first;` 会创建一个副本，当 `first` 向前步进时副本仍停留在原位。
这就是在不使用 `first + 1` 的情况下比较相邻元素的方法。
该区间是半开区间，因此空区间满足 `first == last` 且没有元素可读：在进行第一次 `*first` 之前请务必检查这一点。

### 通过输出迭代器写入

生成值的算法会额外接收一个参数作为目标位置，即输出迭代器。
源和目标可以是不同类型的迭代器，例如用于读取的 vector 迭代器和用于写入的 `std::back_inserter`，因此它们各自拥有独立的模板参数。
`std::copy` 的结构如下：

```cpp
template <typename In, typename Out>
Out copyAll(In first, In last, Out out) {
    while (first != last) {
        *out++ = *first;
        ++first;
    }
    return out;
}
```

`out++` 使 `out` 步进，并求值为步进前 `out` 所在的位置，因此 `*out++ = value;` 会将 `value` 赋值给该位置，并使 `out` 指向其后一个位置。
循环结束时，`out` 是步进后的迭代器，指向最后一个写入值的后一位，函数将其返回。

`std::back_inserter` 会掩盖遗漏的步进操作。
它的 `*` 和 `++` 不执行任何操作，而通过它赋值会调用 `push_back`，因此即使某个版本从未对 `out` 进行步进，仍然能通过它正确填充 vector。
普通的 `std::vector<int>::iterator` 只有在你步进它时才会移动。

### 任务

连续段（run）是指一段相等的相邻元素：`[1, 1, 2, 2, 2, 1]` 包含长度分别为 2、3 和 1 的连续段。
在 `runs.hpp` 中编写这两个模板，对迭代器仅使用复制、`++`、`*`、`==` 和 `!=` 操作。
使用迭代器本身来遍历区间：如果在模板内部将其复制到 `std::vector` 中以便使用下标索引，则每次调用都会复制整个区间。

- `longestRun(first, last)` 返回最长连续段的长度，空区间返回 0。
  `driver.cpp` 会使用 `std::vector<int>`、`std::string` 以及由 vector 构建的 `std::set<int>` 的迭代器来调用它。
  如果一个实现仅在值发生变化时才将当前连续段与最长连续段进行比较，那么它对 `[1, 2, 2]` 会返回 1，因为由 2 构成的连续段到达了 `last` 却未遇到不同的值。
- `copyRunStarts(first, last, out)` 按顺序通过 `out` 写入每个连续段的第一个元素，并返回步进到最后一个写入值之后的 `out`。
  空区间不写入任何内容并原样返回 `out`。
  测试驱动程序会传入绑定到空 `std::vector<int>` 和空 `std::string` 的 `std::back_inserter`，以及 `slots.begin()`（其中 `slots` 是一个与输入等长的全 0 `std::vector<int>`），随后擦除从函数返回的迭代器到 `slots.end()` 的区间。
  对于 `[4, 4, 7, 7, 4]`，你的写入操作会使 `slots` 变为 `[4, 7, 4, 0, 0]`，返回的迭代器指向第一个 0，擦除后留下 `[4, 7, 4]`。
  如果你的函数从未对 `out` 进行步进，擦除后会留下什么？
  思考一下，然后删除你实现中步进 `out` 的 `++` 并运行检查。

### 解答

```cpp
#pragma once

template <typename It>
int longestRun(It first, It last) {
    // 空区间返回 0
    if (first == last) {
        return 0;
    }
    int longest = 1;
    int current = 1;
    It previous = first;
    ++first;
    while (first != last) {
        if (*first == *previous) {
            ++current;
        } else {
            current = 1;
        }
        // 每步都比较，覆盖到达 last 的连续段
        if (current > longest) {
            longest = current;
        }
        previous = first;
        ++first;
    }
    return longest;
}

template <typename In, typename Out>
Out copyRunStarts(In first, In last, Out out) {
    if (first == last) {
        return out;
    }
    // 第一个元素总是连续段的开头
    *out++ = *first;
    In previous = first;
    ++first;
    while (first != last) {
        if (!(*first == *previous)) {
            *out++ = *first;
        }
        previous = first;
        ++first;
    }
    return out;
}
```
