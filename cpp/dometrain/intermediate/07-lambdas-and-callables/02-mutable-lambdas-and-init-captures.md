按值捕获的变量在 lambda 体内部是只读的。
在参数列表后添加 `mutable`，函数体就可以修改它们：

```cpp
int start = 10;
auto counter = [n = start]() mutable { return n++; };
counter();  // 返回 10
counter();  // 返回 11；start 仍然是 10
```

捕获的副本之所以是只读的，是因为 lambda 对象（即编译器为 lambda 生成的函数对象）默认具有 `const` 版本的 `operator()`，除非该 lambda 被标记为 `mutable`。
加上 `mutable` 后，`n++` 会修改该对象自身的 `n`，下一次调用将在此基础上继续。
如果没有 `mutable`，编译器会报错 `cannot assign to a variable captured by copy in a non-mutable lambda`。
即使 lambda 不接受任何参数，在写 `mutable` 之前也必须写出 `()`。

mutable lambda 仅修改其自身的成员，因此无论 `counter` 运行多少次，`start` 都保持为 10。
若按引用捕获 `start`，则会修改该局部变量，而 lambda 本身不会保留独立的值。

### 初始化捕获

`[n = start]` 是一种初始化捕获：它声明了一个新成员 `n`，并在创建 lambda 时使用 `=` 后面的表达式对其进行初始化。
`n` 在 lambda 外部并不存在，并且该表达式可以是任何表达式，而不仅仅是局部变量名。
初始化捕获可以与普通捕获混用：在 `[value = start, step]` 中，`value` 是一个从 `start` 开始的新成员，而 `step` 是一个普通的副本。

由于状态保存在对象内部，因此调用的返回值取决于该对象是在何时创建或复制的：

- `auto copy = counter;` 会复制该 lambda 及其成员在彼时的状态。
  从那时起，`counter` 和 `copy` 将各自独立递进。
- 循环体内的 lambda 表达式在每次循环时都会被求值，从而创建一个重新从初始值开始的新对象。
  在四次循环中，一个从 1 开始且每次加 2 的计数器，如果是在循环前创建的，则依次返回 1、3、5 和 7；如果其 lambda 表达式位于循环体内，则每次循环都返回 1。

### 将 std::unique\_ptr 移动到 lambda 中

`[owner]` 和 `[data = owner]` 都会复制 `owner`，但 `std::unique_ptr` 无法被复制：编译器会报错 `call to implicitly-deleted copy constructor of 'std::__2::unique_ptr<...>'`。
初始化捕获可以通过移动来代替复制，就像在两个 `std::unique_ptr` 变量之间使用 `std::move` 那样：

```cpp
auto owner = std::make_unique<std::vector<int>>(values);
auto length = [data = std::move(owner)] { return data->size(); };
```

`data` 是从 `owner` 移动构造而来的，这会使 `owner` 变为空指针：从此时起 `owner == nullptr` 为真。
该 lambda 拥有这个 vector 的所有权，并在 `length` 析构时释放它。
没有参数且没有 `mutable` 的 lambda 可以省略 `()`，就像 `length` 那样。

### 任务

在 `generators.cpp` 中编写 `Solution` 的三个函数。
当参数超出其限制范围时，每个函数均返回一个空的 vector。

`takeSequence(start, step, count)` 调用一个 mutable lambda `count` 次，并按调用顺序返回各个值：首先是 `start`，然后每个值比前一个值增加 `step`。
负的 `step` 表示倒数，因此 `takeSequence(1000, -1000, 3)` 返回 `[1000, 0, -1000]`。
`start` 和 `step` 的取值范围为 -1000 到 1000，`count` 为 0 到 1000，因此任何值都不会导致 `int` 溢出。
当 `count` 为 0 时返回一个空的 vector。

`copiesKeepOwnState(start)` 创建一个计数器 lambda，对其调用会依次返回 `start`、`start + 1` 等。
在进行任何调用之前先复制该 lambda，然后调用原始 lambda 两次。
`start` 的限制范围与 `takeSequence` 相同。
它返回三个值：

```text
位置                      [原始 lambda 的第三次调用, 副本的第一次调用, start]
copiesKeepOwnState(10)    [12, 10, 10]
```

`ownedSum(values)` 如上所述根据 `values` 构建 `owner`，将其移动到一个返回 vector 元素之和的 lambda 中，并返回该和，若此后 `owner` 为 null 则在其后追加 `1`，否则追加 `0`。
`ownedSum({1, 2, 3})` 返回 `[6, 1]`。
`values` 最多包含 1000 个数字，每个数字在 -1000000 到 1000000 之间，因此求和不会发生 `int` 溢出。

### 解答

```cpp
#include <memory>
#include <utility>
#include <vector>

struct Solution {
    static std::vector<int> takeSequence(int start, int step, int count) {
        if (start < -1000 || start > 1000 || step < -1000 || step > 1000 || count < 0 || count > 1000) {
            return {};
        }
        // mutable 让 lambda 修改自己的 value
        auto next = [value = start, step]() mutable {
            int current = value;
            value += step;
            return current;
        };
        std::vector<int> result;
        for (int i = 0; i < count; ++i) {
            result.push_back(next());
        }
        return result;
    }

    static std::vector<int> copiesKeepOwnState(int start) {
        if (start < -1000 || start > 1000) {
            return {};
        }
        auto counter = [n = start]() mutable { return n++; };
        auto copy = counter; // 调用前复制，状态独立
        counter();
        counter();
        int third = counter();
        return {third, copy(), start};
    }

    static std::vector<int> ownedSum(const std::vector<int>& values) {
        if (values.size() > 1000) {
            return {};
        }
        for (int value : values) {
            if (value < -1000000 || value > 1000000) {
                return {};
            }
        }
        auto owner = std::make_unique<std::vector<int>>(values);
        // 移动所有权到 lambda 中
        auto sum = [data = std::move(owner)] {
            int total = 0;
            for (int value : *data) {
                total += value;
            }
            return total;
        };
        return {sum(), owner == nullptr ? 1 : 0};
    }
};
```
