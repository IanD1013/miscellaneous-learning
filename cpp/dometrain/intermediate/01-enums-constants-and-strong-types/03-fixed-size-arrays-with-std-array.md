`std::array<int, 9>` 在对象自身内部恰好容纳 9 个 int。
`std::vector` 将其元素保存在一个可扩容的独立内存块中；而 `std::array` 没有这样的内存块，因此元素数量在编写类型时就已固定，并成为该类型的一部分。
`std::array<int, 8>` 与 `std::array<int, 9>` 是不同的类型，两者都不能传入期望接收另一种类型的地方。

```cpp
using Grid = std::array<int, 9>;

Grid a{};
a[4] = 5;
Grid b = a;
b[4] = 6;
bool same = (a == b);
constexpr std::size_t cellCount = Grid{}.size();
```

`Grid a{};` 将所有 9 个单元格初始化为 0。
如果不加花括号，局部 `Grid` 将保留内存中原有的任意内容，就像未初始化的局部 `int` 一样。
`a[4]` 读取和写入单元格的方式与 vector 相同，并且与 vector 一样不会检查索引，因此请确保索引小于 `size()`。
`Grid b = a;` 会复制每个元素，这就是为什么设置 `b[4]` 后 `a[4]` 仍保持为 5，而 `==` 会按顺序比较所有 9 个单元格，因此 `same` 为 false。
函数还可以通过值返回 `Grid`，这是内置的 `int[9]` 所无法做到的。
对于每个 `Grid`，`size()` 都会返回 9，这是直接从类型读取的，而不是统计得出的，因此它可以用来初始化 `constexpr` 变量。

第一行是一个类型别名：`using` 为现有类型赋予了第二个名字。
与 `enum class` 不同，它不会创建新类型。
`Grid` 和 `std::array<int, 9>` 是同一个类型，因此在使用这两种名称的代码之间可以自由传递值。
`driver.cpp` 从不写 `Grid`：它将 `gridFrom` 的结果存储在 `std::optional<std::array<int, 9>>` 中，并将 `std::array<int, 9>` 值传递给接收 `const Grid&` 的函数。
该别名添加了一个能够说明这 9 个 int 代表什么的名称，并且如果将来元素类型发生更改，只需修改一行代码。
在编写真正的别名之前，可以先将其写为 8 而不是 9 并运行：看看是哪个文件报告了错误？

### 3x3 网格中的九个单元格

单元格采用行优先（row-major）排列：第 0 行是单元格 0 到 2，第 1 行是单元格 3 到 5，第 2 行是单元格 6 到 8，因此第 `r` 行第 `c` 列就是单元格 `r * 3 + c`。
一个值为 3 的 `constexpr` 边长可以让嵌套的行和列循环中的算术运算保持良好的可读性。

没有任何东西能将 `std::vector<int>` 隐式转换为 `Grid`，即使是包含 9 个值的 vector 也不行，因为 vector 的长度只有在程序运行时才能确定。
转换意味着先检查 `size()`，然后再进行复制。
`>= 9` 的检查会允许包含 10 个值的 vector 作为前 9 个值通过，而在任何检查之前就复制 9 个值的循环则会越界读取长度较短的 vector。

### 需要编写的内容

在 `grid.hpp` 中，按照初始代码注释的指示声明 `Grid`，然后编写以下四个函数：

- `gridFrom(cells)`：当 `cells` 恰好包含 9 个值时，返回一个按原始顺序保存这些值的 `Grid`；对于任何其他长度，返回 `std::nullopt`。
- `transposed(g)`：返回一个新的网格，其第 `r` 行第 `c` 列保存 `g` 的第 `c` 行第 `r` 列的值。
- `rotatedClockwise(g)`：返回顺时针旋转四分之一周后的 `g`：自底向上读取的左侧列变为顶行。
- `isSymmetric(g)`：当 `g` 与其转置相等时返回 true。

对于包含值 1 到 9 的 `g`，这两个函数返回如下所示的网格。
每个网格都是逐行绘制的，因此从左到右、从上到下读取会按顺序得到单元格 0 到 8：

```text
g        transposed(g)   rotatedClockwise(g)
1 2 3    1 4 7           7 4 1
4 5 6    2 5 8           8 5 2
7 8 9    3 6 9           9 6 3
```

测试驱动程序的 `transpose`、`rotate` 和 `symmetric` 会使用 `gridFrom` 构建网格，并将其结果的 9 个单元格作为 vector 报告出来；当没有网格时返回 `[]`（`symmetric` 报告 false）。
`rotate(cells, quarterTurns)` 每顺时针旋转四分之一周调用一次 `rotatedClockwise`，对于 -1 则调用三次。

### 解答

```cpp
#pragma once
#include <array>
#include <cstddef>
#include <optional>
#include <vector>

// 3x3 网格，按行优先存储
using Grid = std::array<int, 9>;

// 网格边长
constexpr std::size_t kSide = 3;

inline std::optional<Grid> gridFrom(const std::vector<int>& cells) {
    // 先检查长度再复制
    if (cells.size() != Grid{}.size()) {
        return std::nullopt;
    }
    Grid g{};
    for (std::size_t i = 0; i < g.size(); ++i) {
        g[i] = cells[i];
    }
    return g;
}

inline Grid transposed(const Grid& g) {
    Grid result{};
    for (std::size_t r = 0; r < kSide; ++r) {
        for (std::size_t c = 0; c < kSide; ++c) {
            result[r * kSide + c] = g[c * kSide + r];
        }
    }
    return result;
}

inline Grid rotatedClockwise(const Grid& g) {
    Grid result{};
    for (std::size_t r = 0; r < kSide; ++r) {
        for (std::size_t c = 0; c < kSide; ++c) {
            // 左侧列自底向上变为顶行
            result[r * kSide + c] = g[(kSide - 1 - c) * kSide + r];
        }
    }
    return result;
}

inline bool isSymmetric(const Grid& g) {
    return g == transposed(g);
}
```
