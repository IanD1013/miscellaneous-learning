使用 `IntBuffer copy = original;` 复制一个 `IntBuffer`，调用 `copy.set(1, 9)`，然后 `original.get(1)` 也会返回 9。
初始代码中没有声明拷贝构造函数，因此编译器会生成一个逐成员拷贝（memberwise copy）的拷贝构造函数：它会依次拷贝每个成员。
对于 `IntBuffer`，这相当于：

```cpp
IntBuffer(const IntBuffer& other) : data_(other.data_), size_(other.size_) {}
```

拷贝 `data_` 只是拷贝了一个地址，而不是存储在那里的 int 数据。
这是浅拷贝（shallow copy）：两个缓冲区都指向同一个内存块，因此通过其中任何一个进行 `set` 修改，都会在另一个中反映出来。

析构过程则会造成破坏。
两个析构函数都会对那同一个内存块调用 `releaseBlock`，而第二次调用传入的则是一个已经被释放过的内存块。
如果析构函数中使用的是 `delete[]`，这就会导致 double free。
在 `blocks.hpp` 中，`acquireBlock(count)` 返回一个包含 `count` 个 0 的内存块，`liveBlocks()` 统计已获取但尚未释放的内存块数量，而 `badReleases()` 统计释放已被释放的内存块或越界写入最后一个元素之后的内存块的次数。

`driver.cpp` 中的 `copyThenChange(size, fill, index, value)` 运行了这一序列：它创建一个包含 `size` 个设为 `fill` 的元素的 `original`，执行 `IntBuffer copy = original;` 并将副本中索引为 `index` 的元素设为 `value`。
它按以下顺序返回六个数字：`original.get(index)`、`copy.get(index)`、副本中仍保持为 `fill` 的元素数量、两个缓冲区同时存在时的 `liveBlocks()`，以及两者都被析构后的 `liveBlocks()` 和 `badReleases()`。
对于 `copyThenChange(3, 7, 1, 9)`：

```text
初始代码，编译器的拷贝   [9, 9, 2, 1, 0, 1]
深拷贝                   [7, 9, 2, 2, 0, 0]
```

### 编写拷贝构造函数

深拷贝（deep copy）为新缓冲区分配独立的内存块：获取一个包含 `other.size_` 个 int 的内存块，然后将 `other` 的每个元素拷贝进去。
这样每个缓冲区各拥有一个内存块，每个析构函数也释放各自拥有的内存块。
保持编译器版本所具有的签名：`IntBuffer(const IntBuffer& other)`。

该参数必须是引用类型。
如果按值传递，`other` 本身将通过拷贝缓冲区来创建，而这正是该构造函数要执行的任务，clang 会报错并提示 `copy constructor must pass its first argument by reference`。
它带有 `const` 修饰，是因为拷贝过程仅读取 `other`，并且 `push_back` 在拷贝缓冲区时传入的是 `const IntBuffer&`。

尽管 `other.data_` 和 `other.size_` 都是 private 成员，该构造函数仍然可以读取它们。
访问权限是按类（per class）检查的，而不是按对象（per object）：`IntBuffer` 内部的代码可以使用任何 `IntBuffer` 对象的私有成员，因此不需要 getter。

每当从现有的 `IntBuffer` 构建一个新的 `IntBuffer` 时，编译器都会调用拷贝构造函数：`IntBuffer b(a);`、`IntBuffer b = a;`、将缓冲区传递给类型为 `IntBuffer` 的参数，以及在 `std::vector<IntBuffer>` 上调用 `v.push_back(a)`。
不要为其添加 `explicit`。
`explicit` 构造函数仅用于直接初始化（例如 `IntBuffer b(a);`）和显式转换（例如 `static_cast<IntBuffer>(a)`）。
`IntBuffer b = a;` 以及按值传递缓冲区属于拷贝初始化（copy initialization），如果加上 `explicit`，这两者都将无法通过编译。

将一个已存在的缓冲区赋值给另一个缓冲区（`b = a;`）是另一个独立的操作，它仍然会按成员拷贝指针。
测试驱动程序不会执行该操作，下一节课程中会实现它。

### 需要完成的任务

在 `buffer.hpp` 中的 `IntBuffer` 里添加拷贝构造函数。
随后，对于其构建的任何缓冲区，`copyThenChange` 都必须符合深拷贝（deep copy）那一行的行为：原始缓冲区在 `index` 处依然读取到 `fill`，而副本的其他 `size - 1` 个元素依然保持为 `fill`。

`copiesInVector(count, fill, last)` 会构建一个由 4 个 `fill` 元素组成的缓冲区，将其最后一个元素设为 `last`，并在 `std::vector<IntBuffer>` 上调用 `count` 次 `push_back`。
每次调用都会构建一个独立的副本，因此在作用域内有 `count + 1` 个活跃的内存块。
它返回四个数字：作用域内的 `liveBlocks()`、持有 `fill`、`fill`、`fill`、`last` 的副本数量，以及离开作用域后的 `liveBlocks()` 和 `badReleases()`。
使用深拷贝时，`copiesInVector(3, 6, 2)` 返回 `[4, 3, 0, 0]`。

在这两个函数中，一旦缓冲区被析构，`liveBlocks()` 和 `badReleases()` 都必须为 0。

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

    // 深拷贝：分配独立内存块并逐个拷贝元素
    IntBuffer(const IntBuffer& other) : data_(acquireBlock(other.size_)), size_(other.size_) {
        for (int i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
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
