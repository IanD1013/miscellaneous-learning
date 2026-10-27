在函数内部编写的 lambda 只能通过其捕获列表（即参数前面的 `[]`）来访问该函数的形参和局部变量。
你之前传递给 `std::sort` 的比较器具有一个空的捕获列表，只要函数体仅读取其自身的形参，这样就没有问题。
如果像下面的 `countAbove` 一样在函数体中读取局部变量，编译器就会报错 `variable 'limit' cannot be implicitly captured`：

```cpp
static int countAbove(const std::vector<int>& values, int limit) {
    return std::count_if(values.begin(), values.end(),
        [](int value) { return value > limit; });
}
```

### 按值捕获

写成 `[limit]` 后，lambda 就会获得 `limit` 的一份独立副本，该副本在创建 lambda 的那一行生成。
每次调用都会读取该副本，因此后续对局部变量的赋值不会被观察到：

```cpp
int limit = 10;
auto isAbove = [limit](int value) { return value > limit; };
limit = 100;
isAbove(50);   // true：该 lambda 仍然与 10 比较
```

列出更多名称以复制更多局部变量：`[low, high]` 会将两者都复制。
通过复制捕获的局部变量在函数体中是只读的：在该 lambda 内部执行 `limit = 0;` 会导致编译错误。
带有捕获的 lambda 是编译器为你编写的函数对象：其成员变量就是在创建 lambda 时设置的副本，而其 `operator()` 负责执行函数体。
这就是为什么在任何接受函数对象的地方，`std::count_if` 都可以接受 lambda。

### 按引用捕获

在名称前加上 `&`，lambda 就会改为存储该局部变量的引用，因此每次调用都会直接读写该变量本身。
`std::for_each(first, last, f)` 从前到后对每个元素调用一次 `f`，并丢弃 `f` 的返回值，因此引用捕获是将结果传递出来的途径：

```cpp
int total = start;
std::for_each(deltas.begin(), deltas.end(), [&total](int delta) { total += delta; });
```

调用结束后，`total` 保存着 `start` 加上每个 delta 的值。
如果写成 `[total]`，编译器会在 `total += delta` 处报错，而且对副本的修改无论如何也无法反映到局部变量上。

引用捕获不会延长局部变量的生命周期：`total` 的生命周期必须长于 lambda 的每一次调用。
在此处是满足该条件的，因为 lambda 的创建、被 `std::for_each` 使用以及销毁，都在拥有 `total` 的函数内部发生。
在 `total` 被销毁后调用持有 `[&total]` 的 lambda 属于未定义行为。

捕获列表中的每个名称都可以单独选择捕获方式，因此 `[&total, limit]` 会按引用捕获 `total` 并按值复制 `limit`。
如果 lambda 仅读取局部变量，请使用复制。
如果 lambda 必须修改局部变量，或者必须观察到 lambda 创建之后赋给局部变量的新值，请使用引用。

捕获列表也可以以默认捕获开头，以进行隐式捕获：`[=]` 会复制函数体使用的每一个局部变量，而 `[&]` 则会按引用捕获每一个局部变量。
这就是前面 `countAbove` 报错信息末尾 `in a lambda with no capture-default specified` 所指的内容。
显式列出每个局部变量的名字可以使选择在创建 lambda 的那一行保持清晰可见，而在 `[&]` 下，你本打算复制的局部变量也会变成引用。

### 编写内容

在 `captures.cpp` 中实现 `Solution` 的四个静态成员：

- `runningTotals(deltas, start)` 返回从 `start` 开始，在每个 delta 之后的累计总和。
  位置 `i` 保存紧接着 `deltas[i]` 之后的累计总和，因此 `runningTotals({5, -8, 3}, 0)` 返回 `[5, -3, 0]`。
  请使用 `std::for_each` 和一个 lambda，在 lambda 中累加 delta 并将新的累计总和记录在你返回的 vector 中。
- `finalTotal(deltas, start)` 通过 `std::for_each` 和一个以 `[&total]` 方式捕获局部变量 `total` 的 lambda，返回 `start` 加上每个 delta 的结果。
- 两者最多接受 1000 个 delta，且 `start` 和每个 delta 必须在 -1000000 到 1000000 之间（含两端）。
  在这些限制范围内，每个总和都在 -1001000000 到 1001000000 之间，完全在 `int` 范围内，因此不会发生加法溢出。
  在进行任何相加操作之前检查输入。
  当输入超出限制时，`runningTotals` 返回一个空的 vector，而 `finalTotal` 返回 `std::numeric_limits<int>::min()`（即 -2147483648，低于任何有效总和）。
  空的 `deltas` 是有效的，`finalTotal({}, 7)` 应返回 7。
- `countBetween(values, low, high)` 使用 `std::count_if` 和一个 lambda，返回介于 `low` 到 `high` 之间（均包含两端）的值的数量。
- `captureTiming(start, later)` 从其形参 `start` 构建两个 lambda。
  `byValue` 为 `[start] { return start; }`（无参数的 lambda 可以省略 `()`），而 `byReference` 则是同一个 lambda 但按引用捕获 `start`。
  当两者都创建好后，将 `later` 赋值给 `start` 并返回 `{byValue(), byReference()}`。
  通过该测试后，预测如果将 `start = later;` 移动到创建 `byValue` 的代码行上方，`captureTiming(1, 5)` 会返回什么，然后移动该行代码并运行验证。

### 解答

```cpp
#include <algorithm>
#include <limits>
#include <vector>

struct Solution {
    // 检查 delta 数量和取值范围
    static bool valid(const std::vector<int>& deltas, int start) {
        auto inRange = [](int v) { return v >= -1000000 && v <= 1000000; };
        return deltas.size() <= 1000 && inRange(start) && std::all_of(deltas.begin(), deltas.end(), inRange);
    }

    static std::vector<int> runningTotals(const std::vector<int>& deltas, int start) {
        if (!valid(deltas, start)) {
            return {};
        }
        std::vector<int> totals;
        int total = start;
        // 按引用捕获 total 和 totals
        std::for_each(deltas.begin(), deltas.end(), [&total, &totals](int delta) {
            total += delta;
            totals.push_back(total);
        });
        return totals;
    }

    static int finalTotal(const std::vector<int>& deltas, int start) {
        if (!valid(deltas, start)) {
            return std::numeric_limits<int>::min();
        }
        int total = start;
        std::for_each(deltas.begin(), deltas.end(), [&total](int delta) { total += delta; });
        return total;
    }

    static int countBetween(const std::vector<int>& values, int low, int high) {
        // 按值捕获 low 和 high
        return static_cast<int>(std::count_if(values.begin(), values.end(),
            [low, high](int value) { return value >= low && value <= high; }));
    }

    static std::vector<int> captureTiming(int start, int later) {
        auto byValue = [start] { return start; };      // 创建时复制
        auto byReference = [&start] { return start; }; // 调用时读取
        start = later;
        return {byValue(), byReference()};
    }
};
```
