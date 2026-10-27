目前该项目无法编译。
构建在 `Tally` 的重复定义处停止，报错位于您正在编辑的文件 `tally.hpp` 中，它是通过一个您从未打开过的文件第二次被引入的。
项目中并没有任何地方重复声明了该 struct。
`program.cpp` 包含了 `tally.hpp`，并且它还包含了 `report.hpp`，而 `report.hpp` 又反过来包含了 `tally.hpp`，因此相同的内容会第二次进入正在编译的文件中，导致编译器拒绝接受第二份副本。

阻止这种情况发生的代码行是：

```cpp
#pragma once
```

`#pragma once` 是一个预处理器指令，因此它在 include 内容被粘贴时（在任何编译发生之前）起作用。
它会标记自身所在的文件。
如果在编译当前文件时再次遇到该文件，预处理器会跳过它，而不是让其内容被第二次处理。
两个 include 都会成功；只是后一个不会传递任何新内容。

保护指令（guard）解决的是单个文件自身的重复副本问题，仅此而已。
一旦头文件被多个独立编译的文件所包含，它无法保证头文件中编写的函数体安全。
那是 `inline` 的职责，它告诉链接器从多个地方预期相同的函数体并只保留一个。
本项目是作为一个单元编译的，因此 `tallyOf` 和 `netScore` 上的两个 `inline` 关键字在这里不起任何作用；它们是头文件为最终所属的构建所保留的编写习惯。
将它们保留在初始代码中的原处即可。

您需要编辑 `tally.hpp`；`report.hpp` 和 `program.cpp` 是固定的。
将保护指令放在第一行（位于 include 和 struct 之上），这样第二次引入就不会成为第二份副本。
`Tally` 包含 `int hits` 和 `int misses`。
`tallyOf(values, threshold)` 用于构建一个实例，将大于或等于 `threshold` 的值计为 hit，将较小的值计为 miss，因此两者的总和始终等于 values 的数量。
`netScore(tally)` 返回 hits 减去 misses 的值，当 misses 更多时结果为负数。
用于评分的 `netFrom` 和 `attemptsFrom` 会从 `program.cpp` 中调用它们。

## 解答

```cpp
#pragma once

#include <vector>

struct Tally {
    int hits;
    int misses;
};

inline Tally tallyOf(const std::vector<int> &values, int threshold) {
    // 不小于 threshold 的值计为 hit，更小的值计为 miss
    Tally tally{0, 0};
    for (int value : values) {
        if (value >= threshold) {
            tally.hits += 1;
        } else {
            tally.misses += 1;
        }
    }
    return tally;
}

inline int netScore(const Tally &tally) {
    // 返回 hits 减去 misses
    return tally.hits - tally.misses;
}
```
