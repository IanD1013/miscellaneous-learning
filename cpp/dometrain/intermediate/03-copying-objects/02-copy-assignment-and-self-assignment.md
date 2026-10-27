`IntBuffer b = a;` 会创建 `b`，因此调用的是拷贝构造函数。
而对已存在的 `b` 执行 `b = a;` 是拷贝赋值（copy assignment），它会调用另一个不同的成员：

```cpp
IntBuffer& operator=(const IntBuffer& other)
```

在 `b = a` 中，`b` 是目标对象，即 `operator=` 内部的 `*this`，而 `a` 是 `other`。
拷贝构造函数在开始时没有内存块；而 `operator=` 运行在一个已经拥有内存块的目标对象上。
它必须释放该内存块，并最终获得 `other` 的大小以及 `other` 元素的独立副本。

如果你不编写 `operator=`，编译器会生成一个逐成员拷贝的版本，这与拷贝构造函数所做的浅拷贝（shallow copy）相同：`b.data_` 获取 `a` 的内存块地址，`b` 原有的内存块永远不会被释放，且随后两个析构函数都会尝试释放 `a` 的内存块。

直接运行初始代码，"assign a larger buffer" 用例会展示编译器生成的 `operator=` 的运行表现。
`assignAndChange(2, 1, 3, 5)` 构建了包含两个 1 的 `a` 和包含三个 5 的 `b`，然后执行 `a = b; a.set(0, 99);`。
从左到右，其输出结果分别是作用域内的 `a.size()`、`a.get(0)`、`b.get(0)` 和 `liveBlocks()`，以及作用域结束后的 `liveBlocks()` 和 `badReleases()`：

```text
编译器的 operator=   [3, 99, 99, 2, 1, 1]
你的 operator=       [3, 99, 5, 2, 0, 0]
```

`b.get(0)` 读取到 99 是因为 `a` 现在写入的是 `b` 的内存块。
之后仍然存活的内存块是 `a` 原有的那个，而错误的释放（bad release）是因为第二个析构函数再次释放了 `b` 的内存块。

`operator=` 以 `return *this;` 结尾，通过引用返回目标对象，原因与 `operator+=` 相同。
`a = b = c` 会先执行 `b = c` 并将其结果赋值给 `a`，而 `(a = b).set(1, 7)` 之所以修改的是 `a`，是因为该结果正是 `a` 本身。
如果返回类型为 `void`，`a = b = c` 将无法通过编译，因为 `b = c` 没有可供赋值的值。
如果按值返回 `IntBuffer`，两行代码都可以编译，但 `.set(1, 7)` 修改的将是一个临时副本而不是 `a`。

### 缓冲区自赋值

没有人会故意写 `a = a`，但只要 `i` 等于 `j`，`buffers[i] = buffers[j]` 就会发生这种情况，测试驱动代码也通过引用模拟了这一点：`IntBuffer& alias = a; a = alias;`。
这就是自赋值（self-assignment）。
在 `operator=` 内部，此时 `other` 就是 `*this`，因此 `other.data_` 就是 `data_`。

直觉上的执行顺序在此处会失效：先释放旧内存块，再从 `other` 拷贝。
释放 `data_` 会导致原本要读取的内存块被提前释放，而在 `blocks.hpp` 中，已释放的内存块读取到的每个元素都是 -1。
一旦 `data_` 指向新内存块，`other.data_` 也会随之指向新内存块。
`a` 最初持有的元素在循环读取之前就已经丢失了。

以下两种修复方案均可让 `a` 保持不变：

- 先检查自赋值。
  `&other` 是 `other` 所引用的缓冲区的地址，因此仅当两侧是同一个对象时，`this == &other` 才为 true，此时 `operator=` 可以直接返回 `*this`，无需进行任何拷贝。
- 先拷贝。
  在旧内存块未被触动的情况下获取新内存块并从 `other` 填充，之后才释放旧内存块并切换到新内存块。
  在副本生成之前，`other` 持有的任何内容都不会被释放，因此 `a = a` 无需额外检查。

“先拷贝”是更好的习惯做法：相同的顺序适用于每一次赋值，因此不会遗漏特殊情况。
在“先释放”顺序前加上自检查同样是正确的。

### 编写内容

在 `buffer.hpp` 中为 `IntBuffer` 添加拷贝赋值运算符。
`driver.cpp` 中的三个函数会用到它：

- `assignAndChange` 将一个缓冲区赋值给另一个不同大小的缓冲区，一次源缓冲区较大，一次源缓冲区较小。
  目标缓冲区最终拥有源缓冲区的大小，而源缓冲区保持自身元素不变。
- `selfAssign(size, fill)` 构建包含 `size` 个设为 `fill` 的元素的 `a`，并执行上面展示的 `a = alias;`。
  它返回作用域内的 `a.size()`、`a.get(0)`、`a.get(size - 1)` 和 `liveBlocks()`，以及作用域结束后的 `liveBlocks()` 和 `badReleases()`。
- `chainAssign(fillA, fillB, fillC)` 使用三个填充值构建三个 2 元素的缓冲区 `a`、`b` 和 `c`，执行 `a = b = c;`，随后执行 `(a = b).set(1, fillA);`，并返回 `a.get(0)`、`a.get(1)`、`b.get(0)`、`b.get(1)`、`c.get(1)` 和 `liveBlocks()`。

缓冲区销毁后，`liveBlocks()` 和 `badReleases()` 必须都为 0。

### 解答

```cpp
#pragma once
#include "blocks.hpp"
#include <utility>

class IntBuffer {
public:
    IntBuffer(int size, int fill) : data_(acquireBlock(size)), size_(size) {
        for (int i = 0; i < size_; ++i) {
            data_[i] = fill;
        }
    }

    IntBuffer(const IntBuffer& other) : data_(acquireBlock(other.size_)), size_(other.size_) {
        for (int i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
    }

    // 先拷贝：新块填好后再释放旧块，自赋值也安全
    IntBuffer& operator=(const IntBuffer& other) {
        int* fresh = acquireBlock(other.size_);
        for (int i = 0; i < other.size_; ++i) {
            fresh[i] = other.data_[i];
        }
        releaseBlock(data_);
        data_ = fresh;
        size_ = other.size_;
        return *this;
    }

    ~IntBuffer() {
        releaseBlock(data_);
    }

    int size() const { return size_; }

    int get(int index) const {
        return (index >= 0 && index < size_) ? data_[index] : 0;
    }

    void set(int index, int value) {
        if (index >= 0 && index < size_) {
            data_[index] = value;
        }
    }

private:
    int* data_;
    int size_;
};
```
