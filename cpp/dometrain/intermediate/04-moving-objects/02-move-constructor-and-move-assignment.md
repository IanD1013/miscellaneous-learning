拷贝构造函数会给新缓冲区分配它自己的内存块并复制每个元素，因为源对象仍会继续使用它自己的内存块。
当源对象是一个右值（rvalue，即临时对象，或者调用者因不再使用而通过 `std::move` 传递的缓冲区）时，这种复制就是无用功，而移动构造函数则会接管源对象的内存块：

```cpp
IntBuffer(IntBuffer&& other)
```

当这两个构造函数都声明后，`IntBuffer b(std::move(a));` 会选择这一个，因为右值与 `IntBuffer&&` 的匹配度优于 `const IntBuffer&`。
如果没有它，同一行代码将执行拷贝构造函数：`std::move(a)` 仅仅进行类型转换，而 `const IntBuffer&` 也能绑定右值。
这就是为什么起始代码中的每一次移动都会执行拷贝。

`driver.cpp` 中的每个函数都会返回它在作用域内读取到的内容，随后紧跟该作用域关闭后的 `liveBlocks()` 和 `badReleases()`。
`acquiredBlocks()` 统计调用期间获取的每个内存块，无论其是否已被释放。
当函数读取缓冲区中不存在的元素时（例如空缓冲区的第一个元素），它会报告 -1。
`moveConstruct(3, 7)` 构建包含三个 7 的 `a`，执行 `IntBuffer b(std::move(a));` 并读取 `b.size()`、`b` 的第一个元素、`a.size()`、`acquiredBlocks()` 以及 `liveBlocks()`。
使用起始代码时，它返回 `[3, 7, 3, 2, 2, 0, 0]`：获取了第二个内存块，且 `a` 的大小仍为 3。
完成移动构造函数后将返回 `[3, 7, 0, 1, 1, 0, 0]`。

接管意味着复制一个指针和一个大小。
移动构造函数不获取任何新内存，元素仍保留在 `a` 放置它们的位置。
这部分可以直接写在成员初始化列表中：

```cpp
IntBuffer(IntBuffer&& other) : data_(other.data_), size_(other.size_) {
}
```

单看这一点，这其实又是编译器逐成员复制的做法。
`a` 和 `b` 持有相同的地址，当作用域结束时，两个析构函数都会释放该内存块。

剩下的工作就是让 `other` 不再拥有任何东西：其指针设为 `nullptr`，大小设为 0。
`releaseBlock(nullptr)` 会直接返回而不做任何事，因此 `a` 的析构函数不会释放任何东西，该内存块便只有一个所有者。
这两个成员都很重要。
无论 `size_` 是多少，析构函数都会将 `data_` 传给 `releaseBlock`；而大小为 3 却没有任何底层内存块会导致 `a.get(0)` 对 `nullptr` 进行读取。

### 移后缓冲区

移动之后，`a` 处于移后（moved-from）状态但仍然存活。
它的析构函数会在作用域结束时运行，这就是为什么它的指针必须是 `nullptr`，并且可以通过 `a = IntBuffer(2, 8);` 赋予新值。
`IntBuffer` 将其移后状态定义为空：`size()` 为 0 且没有内存块。
标准库的保证则更少。
处于移后状态的 `std::string` 或 `std::vector` 是有效但未指定的（valid but unspecified）：安全可销毁或可赋新值，但标准并未说明它持有什么内容，因此代码在再次读取它之前应当赋予其新值。

### 移动赋值

在已存在的 `a` 上执行 `a = std::move(b);` 会调用移动赋值：

```cpp
IntBuffer& operator=(IntBuffer&& other)
```

它在一个可能已经拥有内存块的目标对象上执行移动构造函数的工作。
返回时，`a` 持有 `other` 的指针和大小，并且 `other` 为空。
`a` 之前拥有的内存块必须在此处释放：一旦 `data_` 改变，就再也没有其他途径去释放它了。
与拷贝赋值一样，它以 `return *this;` 结束。
处于移后状态的目标对象持有 `nullptr`，因此 `a = IntBuffer(2, 8);` 在进入时不会释放任何东西。

`moveAssign(2, 1, 3, 5)` 构建包含两个 1 的 `a` 和包含三个 5 的 `b`，执行 `a = std::move(b);` 并读取 `a.size()`、`a` 的第一个元素、`b.size()`、`acquiredBlocks()` 以及 `liveBlocks()`，最后是作用域后的两个计数：

```text
旧内存块从未释放        [3, 5, 0, 2, 2, 1, 0]
与 other 交换内存块     [3, 5, 2, 2, 2, 0, 0]
完成的移动赋值          [3, 5, 0, 2, 1, 0, 0]
```

泄漏的内存块是在作用域后仍存活的 1。
使用 swap 交换的那一行与完成版结尾相同，是因为 `b` 的析构函数释放了 `a` 的旧内存块，但在此之前 `b` 持有了该内存块，而不是文档所规定的空状态。

自我移动（self-move）即 `a = std::move(alias);`（其中 `IntBuffer& alias = a;`），此时 `other` 就是 `*this`。
如果先释放 `data_`，你就会释放掉自己本来要保留的内存块；如果清空 `other`，你就会清空 `a`。
起始代码中的拷贝赋值不需要检查 `a = a`，因为它在释放旧内存块之前会先填充一个崭新的内存块；而移动操作则是直接接管 `other` 的内存块。
在执行其他任何操作之前，先将 `this` 与 `&other` 进行比较，当它们相同时，不作任何更改直接返回 `*this`。

### 编写内容

在 `buffer.hpp` 中注释标明的位置为 `IntBuffer` 添加这两个移动操作，并保持拷贝操作和析构函数原样不变。
`driver.cpp` 中的另外两个函数会检查移后缓冲区和自我移动：

- `reuseAfterMove(size, fill)` 构建 `a`，执行 `IntBuffer b(std::move(a));` 然后执行 `a = IntBuffer(2, 8);`，并返回 `a.size()`、`a` 的第二个元素、`b.size()`，接着是作用域后的两个计数。
- `selfMove(size, fill)` 构建 `a`，如上所述通过 `alias` 对其进行自我移动，并返回 `a.size()`、`a` 的第一个元素、`liveBlocks()`，接着是作用域后的两个计数。

在所有情况下，一旦作用域关闭，`liveBlocks()` 和 `badReleases()` 都应为 0。
手写的移动操作通常还会带有 `noexcept`。
当扩容的 `std::vector` 重新迁移其元素时这非常关键（本章末尾会对此进行讨论），因此这里的两个操作暂时省略了它。

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

    // 移动构造：接管指针和大小，并把 other 置空
    IntBuffer(IntBuffer&& other) : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // 移动赋值：先处理自我移动，再释放旧内存块并接管 other 的内存块
    IntBuffer& operator=(IntBuffer&& other) {
        if (this == &other) {
            return *this;
        }
        releaseBlock(data_);
        data_ = other.data_;
        size_ = other.size_;
        other.data_ = nullptr;
        other.size_ = 0;
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
