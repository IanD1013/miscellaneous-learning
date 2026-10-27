在变量前加上 `constexpr` 会使其成为编译器在构建程序时（即编译期）计算出的常量：

```cpp
constexpr int kBlockSize = 16;
```

其初始值设定项必须是常量表达式，即编译器无需运行程序即可计算出的值，否则构建将会停止。
作为回报，`kBlockSize` 可以用于 C++ 中需要常量的任何地方，例如另一个 `constexpr` 变量的初始值设定项或 `static_assert` 的条件。
`const` 则是一个较弱的承诺：值一旦设定就绝不会改变，但它可能是由仅在运行时可知的内容（例如函数参数）设定的。

constexpr 函数，即在前面声明了 `constexpr` 的函数，可以用同一个函数体服务两类调用者：

```cpp
constexpr int clampPercent(int percent) {
    if (percent < 0) {
        return 0;
    }
    if (percent > 100) {
        return 100;
    }
    return percent;
}

constexpr int kDefaultPercent = clampPercent(140);
static_assert(kDefaultPercent == 100, "clampPercent(140) must return 100");

int fromInput(int typed) {
    return clampPercent(typed);
}
```

`kDefaultPercent` 需要其值为常量，而 140 是一个常量，因此编译器在编译期运行 `clampPercent` 并存储 100。
`fromInput` 传递的值仅在程序运行时存在，因此该调用运行相同的函数体作为普通的运行时代码。
没有任何机制强制 `constexpr` 函数必须在编译期运行；当其实参为常量且需要其结果作为常量时，它才会在编译期运行。
其函数体可以使用局部变量、`if` 语句以及多个 `return`。
如果移除 `constexpr`，`fromInput` 仍然可以编译，但构建会在 `kDefaultPercent` 和 `static_assert` 处停止，因为对普通函数的调用不是常量表达式。

`static_assert(condition, "message");` 由编译器做出判定。
条件为 false 时会停止构建并打印该消息；条件为 true 时则不会留下任何痕迹，因此在程序后续阶段不会运行任何检查。
它可以放置在文件作用域中，位于其所守护的常量旁边，且其条件必须是常量表达式：`kBlockSize % 8 == 0` 符合条件，而函数参数永远不符合条件。

### 在相加前检查溢出

来自 `<limits>` 的 `std::numeric_limits<int>::max()` 是最大的 `int`，对于 32 位 `int` 来说是 2147483647，并且它也是一个常量表达式。
要得知对于正数 `b`，`a + b` 是否放得下，应在相加前进行比较，因为 `max() - b` 不会发生溢出：

```cpp
if (a > std::numeric_limits<int>::max() - b) {
    // a + b 放不下在一个 int 中
}
```

先相加然后再检查和是否变为负数是行不通的。
在 C++ 中，有符号整数溢出属于未定义行为（undefined behavior），因此编译器可能会假定它永远不会发生并优化掉该检查。
像 `value > 999999999` 这样的固定边界也不适用：它会拒绝对 1000000000 到 2147483647 的所有 `int`。

### 需要编写的内容

`driver.cpp` 以两种方式使用 `alignUp`。
在文件作用域中，它包含 `static_assert(alignUp(10, 4) == 12, ...)`、`static_assert(alignUp(2147483641, 10) == -1, ...)` 以及 `constexpr int kHeaderSize = alignUp(5, kBlockSize);`，编译器会在编译期对它们进行求值。
`roundUp(value, alignment)` 在运行时使用每个测试的值调用 `alignUp`，而 `headerSize()` 返回 `kHeaderSize`。
起始代码中的 `alignUp` 会直接返回未更改的 `value`，因此在完成它之前，驱动程序中的两个 `static_assert` 都会导致构建停止，第一个报错为 "alignUp(10, 4) must give 12 while compiling"。

在 `align.hpp` 中，完成 `constexpr int alignUp(int value, int alignment)`。
它返回不小于 `value` 的最小 `alignment` 倍数：`alignUp(10, 4)` 返回 12，`alignUp(12, 4)` 返回 12，而 0 保持为 0。
当 alignment 为 1 时，每个非负值都会原样返回，包括 2147483647。
当 `value` 为负数、`alignment` 小于 1（在对 `alignment` 使用 `%` 或 `/` 之前先检查这一点，因为对 0 进行模或除运算是未定义行为），或者该倍数大于 `std::numeric_limits<int>::max()` 时，它返回 -1。
所有有效结果都大于或等于 0，因此 -1 不会被误认为是有效结果。

在接近 `int` 上限处，alignment 10 还剩下一个倍数，即 2147483640：

```text
alignUp(2147483639, 10)   2147483640
alignUp(2147483640, 10)   2147483640
alignUp(2147483641, 10)   -1
```

2147483639 需要加上 1，而 2147483640 不需要加任何值。
2147483641 需要加上 9，这会得到 2147483650，超出了 `int` 的最大值。
驱动程序中的第二个 `static_assert` 在编译期进行该调用，而发生溢出的计算不是常量表达式。
在检查之前就进行加法操作的版本会在该行停止构建，报错为 `static_assert expression is not an integral constant expression`。
在溢出检查中，`b` 是 `alignUp` 实际要加上的量。
如果直接使用整个 alignment 编写检查（如 `value > std::numeric_limits<int>::max() - alignment`），即使 2147483640 放得下，它也会对 2147483639 返回 -1。

保持 `kBlockSize` 为 16，以便 `headerSize()` 返回 16，并在其下方添加一个带有消息的 `static_assert`，断言 `kBlockSize` 是 8 的正整数倍。

### 解答

```cpp
#pragma once
#include <limits>

constexpr int alignUp(int value, int alignment) {
    // 先检查参数，避免对 0 取模
    if (value < 0 || alignment < 1) {
        return -1;
    }
    int remainder = value % alignment;
    if (remainder == 0) {
        return value;
    }
    // 实际要加上的量
    int toAdd = alignment - remainder;
    // 相加前检查溢出
    if (value > std::numeric_limits<int>::max() - toAdd) {
        return -1;
    }
    return value + toAdd;
}

constexpr int kBlockSize = 16;
static_assert(kBlockSize > 0 && kBlockSize % 8 == 0, "kBlockSize must be a positive multiple of 8");
```
