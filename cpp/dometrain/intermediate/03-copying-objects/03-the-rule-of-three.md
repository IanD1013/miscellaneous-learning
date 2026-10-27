`SlotHandle` 拥有 `slots.hpp` 中 8 槽位表里的一个槽位，而不是一块内存，其析构函数必须关闭该槽位。
有了这个析构函数后，编译器生成的拷贝构造函数和拷贝赋值运算符对该类来说就是错误的：它们将 `handle_` 作为普通 `int` 进行复制，导致两个句柄指向同一个槽位，并且两个析构函数都会尝试关闭它。
这就是三法则（rule of three）：一个管理资源并且需要自定义析构函数、拷贝构造函数或拷贝赋值运算符的类，无论该资源是什么，都需要同时实现这三者。
封装文件描述符的类具有相同的结构：它持有一个必须恰好关闭一次的 `int`。

`slots.hpp` 是只读的。
句柄是一个从 0 到 7 的槽位编号，存储在槽位中的值可以是任意 `int`：

- `openSlot(value)` 打开编号最小的空闲槽位，将 `value` 存入其中并返回其句柄。
- `duplicateSlot(handle)` 打开另一个槽位，保存 `handle` 对应槽位中的值，并返回新的句柄。
- `closeSlot(handle)` 关闭槽位。
  关闭一个尚未打开的槽位不会导致程序崩溃，而是会使 `badCloses()` 增加 1，因此重复关闭会以计数的形式呈现。
- `openSlots()` 统计处于打开状态的槽位数量。

当所有 8 个槽位都已打开时，两个打开函数均返回 -1；对于未打开的句柄，`duplicateSlot` 也会返回 -1。
值为 -1 的句柄不拥有任何资源：`valid()` 返回 false，`value()` 返回 0，且 `closeSlot(-1)` 不执行任何操作。

### 拷贝句柄

拷贝需要拥有自己独立的槽位并保存相同的值，以便在执行 `SlotHandle b = a;` 之后，`a.setValue(6)` 仍能保持 `b.value()` 不变。
`driver.cpp` 中的 `copyIndependence(5, 6)` 正是测试了这种情况：它构建持有 5 的 `a`，执行 `SlotHandle b = a;`，然后将 `a` 设置为 6。
它会汇报五个数字：作用域内的 `a.value()`、`b.value()` 和 `openSlots()`，以及作用域结束后的 `openSlots()` 和 `badCloses()`。

```text
仅有析构函数     [6, 6, 1, 0, 1]
三个成员齐全     [6, 5, 2, 0, 0]
```

如果只编写了析构函数，`b` 会指向 `a` 的槽位：它读取到 6，只有一个槽位处于打开状态，并且第二个析构函数对该槽位的关闭操作就是那次错误关闭。

当所有 8 个槽位均已打开时，`duplicateSlot` 返回 -1，此时创建的拷贝将没有可用槽位。
这是正确的结果：该拷贝的 `valid()` 返回 false，且其析构函数不会关闭任何内容。
如果改为赋予它 `a` 的句柄，就会再次导致两个句柄指向同一个槽位，从而使其变为有效。

### 赋值句柄

拷贝赋值承担了另外两个成员的工作：`a = b` 会为 `a` 分配一个保存 `b` 的值的新槽位，并关闭 `a` 之前持有的槽位。
`assignAcross(1, 2, 3)` 构建持有 1 的 `a` 和持有 2 的 `b`，执行 `a = b;`，然后将 `b` 设置为 3，并汇报相同的五个数字：

```text
编译器的 operator=       [3, 3, 2, 1, 1]
从不关闭的 operator=     [2, 3, 3, 1, 0]
先拷贝的 operator=       [2, 3, 2, 0, 0]
```

编译器生成的 `operator=` 会使 `a` 指向 `b` 的槽位，因此 `a` 读取到 `b` 的新值 3，`a` 最初打开的槽位在离开作用域后仍处于打开状态，而 `b` 的槽位被关闭了两次。
中间一行获取了正确的值，但从未关闭 `a` 的第一个槽位，该槽位是作用域内的第三个打开槽位，也是离开作用域后遗留下来的槽位。

`IntBuffer` 的 `operator=` 中采用的“先拷贝后释放”顺序在这里同样适用：先获取新槽位，再关闭旧槽位。
先关闭旧槽位会破坏 `a = a` 的情况，因为 `duplicateSlot` 随后要读取的正是刚刚被关闭的槽位。
单纯依靠“先拷贝后释放”会留下一个 `IntBuffer` 中不存在的问题，因为 `duplicateSlot` 可能会失败。
当所有 8 个槽位均已打开时，在 `a = a` 内部 `duplicateSlot` 会返回 -1，随后 `operator=` 会关闭 `a` 持有的唯一槽位，导致 `a` 最终变为无效。
在 `operator=` 开头加入自赋值检查，当 `this == &other` 时直接返回 `*this`，这样无论表有多满，`a = a` 都不会产生任何改变。

### 需要编写的内容

在 `slot_handle.hpp` 中的 `SlotHandle` 里添加拷贝构造函数、拷贝赋值运算符和析构函数，确保每个拷贝和每个被赋值的句柄都保留各自独立的值，并且在所有句柄被销毁后，`openSlots()` 和 `badCloses()` 均为 0。
除了上述两个函数外，`driver.cpp` 还会运行以下测试：

- `selfAssign(4)` 通过引用将 `a` 赋值给其自身，并汇报作用域内的 `a.value()` 和 `openSlots()`，以及作用域结束后的 `openSlots()` 和 `badCloses()`。
  `a` 应保留其值及其打开的一个槽位。
- `copyWhenFull()` 直接打开 7 个槽位，在最后一个空闲槽位中构建 `a` 并对其进行拷贝。
  它会汇报作用域内的 `copy.valid()`（1 或 0）和 `openSlots()`，以及在一切关闭后的 `openSlots()` 和 `badCloses()`。

### 解答

```cpp
#pragma once
#include "slots.hpp"
#include <utility>

class SlotHandle {
public:
    explicit SlotHandle(int value) : handle_(openSlot(value)) {}

    // 拷贝：打开独立槽位，表满时为 -1
    SlotHandle(const SlotHandle& other) : handle_(duplicateSlot(other.handle_)) {}

    // 自赋值检查，然后先拷贝再关闭旧槽位
    SlotHandle& operator=(const SlotHandle& other) {
        if (this == &other) {
            return *this;
        }
        int fresh = duplicateSlot(other.handle_);
        closeSlot(handle_);
        handle_ = fresh;
        return *this;
    }

    ~SlotHandle() {
        closeSlot(handle_);
    }

    bool valid() const { return handle_ != -1; }
    int value() const { return readSlot(handle_); }
    void setValue(int value) { writeSlot(handle_, value); }

private:
    int handle_;
};
```
