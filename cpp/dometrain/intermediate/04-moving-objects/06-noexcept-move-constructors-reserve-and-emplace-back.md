`growth.hpp` 中的 `Entry` 会统计自身被拷贝和移动的次数。
向一个空的 `std::vector<Entry>` 执行五次 `push_back(Entry(i))` 调用，在这里会产生 7 次拷贝，尽管每个参数都是右值且 `Entry` 拥有移动构造函数。
这五次调用确实将它们的临时对象移动了进去。
拷贝来自于容量增长（growth）。
`std::vector` 将其元素保存在一块缓冲区中，容量为 `capacity()` 个元素，其中 `size()` 个槽位正在使用中。
当 `push_back` 发现 `size()` 等于 `capacity()` 时，就会引发重新分配（reallocation）：vector 会分配一个更大的缓冲区，将已存储的每个元素移动或拷贝到其中，并释放旧的缓冲区。
逐个元素构建的 vector 会反复重新分配，因此其靠前的元素会被移动或拷贝多次。

每个新缓冲区要大多少取决于标准库的实现，而不是 C++ 语言本身。
当前运行环境中的库从容纳一个元素的空间开始，并在每次 vector 满时将容量翻倍。
以下是五次调用后各自的 `capacity()` 以及每次调用拷贝了多少个 entry：

```text
调用          1   2   3   4   5
capacity()    1   2   4   4   8
拷贝次数      0   1   2   0   4
```

第二、第三和第五次调用发现 vector 已满并发生重新分配，分别拷贝了 1、2 和 4 个 entry：这也就是那 7 次拷贝的来源。

### noexcept 承诺

函数上的 `noexcept` 是一种承诺，保证它不会中途失败：一旦开始执行，就会一直运行到结束。
在重新分配时，`std::vector` 仅当元素的移动构造函数带有该承诺，或者它们根本无法被拷贝（例如 `std::unique_ptr`）时，才会移动其元素。
否则它就会拷贝它们。
原因在于移动操作留下的状态。
如果四个移动操作中的第三个失败了，前两个旧元素就已经处于 moved-from 状态，vector 无法恢复到原本保存的状态。
拷贝操作会保持每个旧元素的原样，直到新缓冲区准备就绪，因此只有在无法使用拷贝时，vector 才会无视承诺去进行移动。

`noexcept` 放在参数列表之后、开始初始化列表的 `:` 之前：

```cpp
Entry(Entry&& other) noexcept : id_(other.id_) { other.id_ = -1; ++moves_; }
```

函数体的执行与之前完全相同。
该承诺是提供给调用构造函数的代码的信息：vector 在这里会读取它，标准库的其他部分也会读取它。
仅当函数中没有任何东西可能失败时才做出此承诺。
`Entry` 的移动构造函数只涉及 `int`，而本章前面为 `IntBuffer` 编写的移动构造函数只接管了一个指针和一个大小，因此两者都可以带有 `noexcept`。
有了它，不断扩容的 `std::vector<IntBuffer>` 会直接交接每个内存块，而不是重新分配并拷贝新的内存块。
必须分配内存的移动构造函数不应该做出此承诺，因为内存分配可能会失败。

你并不总是需要自己编写该承诺。
编译器生成的移动构造函数，或者声明为 `= default` 的移动构造函数，只要其每个成员的移动操作都带有该承诺，它就会带有该承诺。
一个成员为 `std::string` 和 `std::vector` 的零法则（rule-of-zero）类，即使其内部任何地方都没写 `noexcept`，在扩容时也会被移动。

### 预留空间与就地构造

即使有了该承诺，扩容仍然会多次移动靠前的元素。
当最终大小已知时，`reserve(n)` 可以一步分配容纳 `n` 个元素的空间。
它不会添加任何元素：`size()` 保持不变，而 `capacity()` 至少变为 `n`。
只要 `size()` 保持在 `n` 以内，就不会发生重新分配。

`push_back(Entry(i))` 会构造一个临时的 `Entry`，然后将其移动到对应的槽位中，因此即使在预留的空间中，每个元素也会耗费一次移动。
`emplace_back` 接受构造函数参数而不是元素本身，并将它们传递给元素的构造函数，从而在 vector 自身的槽位中就地构建元素：

```cpp
std::vector<std::pair<int, std::string>> names;
names.reserve(2);
names.emplace_back(1, "one");
names.emplace_back(2, "two");
```

每次调用都会在其预留的槽位中运行 `std::pair` 构造函数，而不会产生临时的 pair。
如果传给 `emplace_back` 一个已经构建完成的对象，例如 `emplace_back(Entry(i))`，那么临时对象及其移动操作就又回来了。

### 需要构建的内容

在 `growth.hpp` 中编写 `buildReserved(count)` 和 `buildGrowing(count)`，使它们各自返回一个按顺序包含 id 0 到 `count - 1` 的 `std::vector<Entry>`，并修改 `Entry` 使扩容的 vector 能够移动其内部元素。
`count` 的范围是 0 到 10000。
编译器通常会在调用者的对象中直接构造返回的局部 vector，最坏情况下也是移动它。
移动 vector 只会交接其缓冲区而不会触及任何 `Entry`，因此统计次数仅涵盖填充过程。

- `reservedCost(count)` 调用 `buildReserved` 并返回 `[copies, moves, size]`，结果必须为 `[0, 0, count]`：没有一个 `Entry` 被拷贝或移动。
- `growingCost(count)` 调用 `buildGrowing` 并返回 `[copies, size, capacity]`。
  `buildGrowing` 在不调用 `reserve` 的情况下逐个添加 entry，因此其 vector 会扩容：拷贝次数必须为 0，并且容量是翻倍增长所达到的值（对于 5 个 entry 来说是 8）。
- `moveIsNoexcept()` 询问编译器 `Entry` 的移动构造函数是否带有 `noexcept` 承诺，并且必须返回 `true`。

先编写 `buildGrowing`，此时移动构造函数还没有 `noexcept`。
在运行 `growingCost(100)` 之前，利用容量翻倍的规则算一算它会报告多少次拷贝。

### 解答

```cpp
#pragma once
#include <vector>

class Entry {
public:
    explicit Entry(int id) : id_(id) {}
    Entry(const Entry& other) : id_(other.id_) { ++copies_; }
    // noexcept：扩容时 vector 才会移动而不是拷贝
    Entry(Entry&& other) noexcept : id_(other.id_) { other.id_ = -1; ++moves_; }
    int id() const { return id_; }
    static int copies() { return copies_; }
    static int moves() { return moves_; }
    static void resetCounts() { copies_ = 0; moves_ = 0; }

private:
    int id_;
    inline static int copies_ = 0;
    inline static int moves_ = 0;
};

inline std::vector<Entry> buildReserved(int count) {
    std::vector<Entry> entries;
    entries.reserve(count);  // 一次分配，不再重新分配
    for (int i = 0; i < count; ++i) {
        entries.emplace_back(i);  // 就地构造，无临时对象
    }
    return entries;
}

inline std::vector<Entry> buildGrowing(int count) {
    std::vector<Entry> entries;
    for (int i = 0; i < count; ++i) {
        entries.emplace_back(i);
    }
    return entries;
}
```
