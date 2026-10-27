本章中没有任何内容向评分系统直接传递过对象，事实上也无法做到。
评分系统只能比较数字、布尔值、字符、字符串以及由这些类型构成的一维 vector。
如果返回其他任何内容，自定义类、`std::pair`、`std::tuple` 或是嵌套 vector，文件依然能够编译通过，但每个测试用例都会失败：实际值显示为空，并提示返回类型无法比较。

外部只能调用自由函数和静态函数，因此对类的检验是通过静态驱动函数（driver）来完成的：由一个被评分的函数构建对象、驱动其运行，并读取返回的普通数字。

```cpp
static int highestSeen(const std::vector<int> &values) {
    Peak peak;
    for (int value : values) {
        peak.offer(value);
    }
    return peak.highest();
}
```

### 返回的结果是全部的检验依据

驱动函数会读回任务中涉及的每一个值，因为测试用例只能检查它所返回的内容。
一个在连续序列结束后就停止计数的类，可能仍能报告出正确的最长连续长度，因此如果驱动函数只返回这一个数字就会让它蒙混过关；而如果同时返回当前的连续长度，就能在 `{1, 1, 1, 0, 2}` 这样的用例中捕获这个错误。
每个测试用例都会启动一个全新的程序，所以即便将对象提升到文件作用域，它也依然会重置回初始值。
请将其构建为驱动函数的局部变量。

### `Streak` 遵循的规则

该类维护两个计数：当前处于的连续正读数长度，以及见过的最长连续长度。
`record` 接收一个读数并应用该规则。
大于 0 的读数会使当前连续计数加 1；其他任何值（包括 0）都会将当前连续计数重置为 0。
与最长连续长度的比较应当在扩展连续计数的读数处进行，而不是在循环结束后才比较，否则输入前期出现的较长连续记录在最后一个元素到达时就已经丢失了。
正是这种比较机制确保了最长计数永远不会低于当前计数。

`runLengths` 构建一个 `Streak` 对象，按顺序对每个元素调用一次 `run.record(reading)`，并在一个 `std::vector<int>` 中返回两个条目：先是 `run.current()`，然后是 `run.best()`。
在另一个您无法编辑的文件中还提供了第二个驱动函数。
它会构建自己的 `Streak` 对象，传入相同的读数，并报告两个计数中的某一个。
因此，如果一个类什么都不记录，无论您自己的驱动函数计算得多么精确，都无法通过这些用例。
最多会传入 60 个读数，数值范围均在 -1000 到 1000 之间。
在没有读数的情况下，两个计数都保持构造函数设置的 0，而对于 `{4, 5, 0}`，结果应返回 `[0, 2]`，因为 0 结束了当前连续计数，而最长连续计数保持为 2。

### 解答

```cpp
#include <vector>

class Streak {
public:
    Streak() : currentRun_(0), bestRun_(0) {}

    void record(int reading) {
        // 正读数延长当前连续段，其他读数结束它，
        // 并在延长时更新目前见过的最长连续段
        if (reading > 0) {
            currentRun_ += 1;
            if (currentRun_ > bestRun_) {
                bestRun_ = currentRun_;
            }
        } else {
            currentRun_ = 0;
        }
    }

    int current() const {
        return currentRun_;
    }

    int best() const {
        return bestRun_;
    }

private:
    int currentRun_;
    int bestRun_;
};

struct Solution {
    static std::vector<int> runLengths(const std::vector<int> &readings) {
        Streak run;
        // 把每个读数交给对象，然后报告当前连续段和最长连续段
        for (int reading : readings) {
            run.record(reading);
        }
        return {run.current(), run.best()};
    }
};
```
