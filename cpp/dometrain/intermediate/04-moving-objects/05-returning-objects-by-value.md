按值返回 `Tracked` 的开销可能是零、一次移动或一次拷贝，具体取决于 `return` 后面的表达式。

```cpp
inline Tracked makeTracked(int id) { return Tracked(id); }
```

`Tracked(id)` 直接在驱动程序的 `result` 中构造，因此既不执行拷贝构造函数，也不执行移动构造函数。
C++17 对返回的临时对象有此强制要求，该规则被称为保证复制消除（guaranteed copy elision）。
写成 `return std::move(Tracked(id));` 则会增加一次移动：`std::move` 需要一个引用的对象，因此会先创建临时对象，然后再将 `result` 从中移动构造出来。

返回一个名称（具名对象）的工作方式则有所不同：

```cpp
inline Tracked passOn(Tracked t) { return t; }
```

`t` 有名称，因此是一个左值（lvalue），但如果 return 语句指明的是整个局部变量或按值传递的形参，则会将其视为右值（rvalue）。
这就是隐式移动（implicit move）：在原本会调用拷贝构造函数的地方运行了移动构造函数。
`return std::move(t);` 同样执行单次移动，因此在这里 `std::move` 没有带来额外效果。

形参总是需要消耗那一次移动，因为调用者在调用发生之前就已经构造了它。
局部变量的开销则可能更小。
当一个函数在所有执行路径上都返回同一个局部变量时，编译器通常会直接从一开始就在调用者的对象中构建该局部变量，此时不执行任何操作；标准允许这样做，但并不保证。
只有 `return local;` 能够享受这种优化：`return std::move(local);` 是一个函数调用，因此局部变量会先独立构建，然后再移动到调用者的对象中。
像 `pick` 和 `clampedToZero` 这样返回两个对象之一的函数，无法将两个对象都预先构建在调用者的对象中，因此对它们而言，隐式移动是避免返回时发生拷贝的关键。

### 隐式移动不适用的情况

隐式移动仅在 `return` 后面的整个表达式是一个局部变量或形参的名称时才适用。
`return` 后面的任何其他左值都会被拷贝，即使该对象之后不再被使用：

- `chooseFirst ? a : b` 是一个条件表达式。
  它引用了 `a` 或 `b`，但并不是其中任意一个的名字，因此结果会从选中的那个对象拷贝而来。
- `pair.first` 是一个成员。
  在 `takeFirst` 返回后，没有任何代码会再读取 `pair`，但返回语句指代的是形参的一部分，而不是它的整体。
  `std::move` 会将该成员转换为右值，从而转而运行移动构造函数：

```cpp
struct Holder { Tracked kept; };
inline Tracked release(Holder holder) { return std::move(holder.kept); }
```

一个 `const` 局部变量也不会被移动。
即使被当作右值处理，它依然是 `const` 的，而移动构造函数接受非常量的 `Tracked&&`，因此会转而运行拷贝构造函数。
这只有在编译器没有在调用者的对象中直接构造局部变量时才会体现出来，例如初始代码中的 `clampedToZero`，它返回两个 `const` 局部变量中的一个，因此在两条路径上都会发生拷贝。

### 需要修改的内容

修改 `returns.hpp` 中的 `pick`、`takeFirst` 和 `clampedToZero`，使它们在返回 `Tracked` 时不发生任何拷贝，并保持 `makeTracked` 不变。
保留这四个函数的签名，包括 `takeFirst` 按值接受其 `TrackedPair` 参数。

- `pick(a, b, chooseFirst)` 当 `chooseFirst` 为 true 时返回 `a`，否则返回 `b`。
- `takeFirst(pair)` 返回 `pair.first`。
- `clampedToZero(id)` 当 `id` 为负数时返回一个 id 为 0 的 `Tracked`，否则返回 id 为 `id` 的 `Tracked`。

`pick` 和 `takeFirst` 返回传入给它们的形参或成员，而不是通过其 `id()` 构造的新 `Tracked`。

驱动程序使用 `std::move` 传递 `pick` 的两个实参，并将一个 `TrackedPair` 移动传递给 `takeFirst`，因此构建这些形参需要两次移动且不发生拷贝。
每个驱动函数都会返回调用期间产生的拷贝次数以及返回的 `Tracked` 的 id。
`Tracked` 为每个新构造的对象赋予一个 origin 编号；拷贝和移动都会保留该编号。
`pickCost` 和 `takeFirstCost` 还会报告结果是否保留了所选输入的 origin：1 表示是，0 表示否。
额外的移动不会改变此值：

```text
                       [拷贝次数, 返回的 id, origin 是否相同 (1=是, 0=否)]
                       初始代码     你的版本
makeCost(4)            [0, 4]       [0, 4]
pickCost(1, 2, true)   [1, 1, 1]    [0, 1, 1]
takeFirstCost(5, 6)    [1, 5, 1]    [0, 5, 1]
clampCost(9)           [1, 9]       [0, 9]
clampCost(-3)          [1, 0]       [0, 0]
```

两列中的 id 是一致的，因为拷贝和移动都会传递 id，因此拷贝计数能够展示哪些 return 语句仍在进行拷贝。
origin 值独立于其 id，用于记录结果来自哪个输入。

### 解答

```cpp
#pragma once
#include <utility>
#include "tracked.hpp"

struct TrackedPair {
    Tracked first;
    Tracked second;
};

inline Tracked makeTracked(int id) { return Tracked(id); }

inline Tracked pick(Tracked a, Tracked b, bool chooseFirst) {
    // 分别返回形参名称，触发隐式移动
    if (chooseFirst) { return a; }
    return b;
}

// 成员不会隐式移动，需要 std::move
inline Tracked takeFirst(TrackedPair pair) { return std::move(pair.first); }

inline Tracked clampedToZero(int id) {
    // 去掉 const，才能隐式移动
    Tracked zero(0);
    Tracked given(id);
    if (id < 0) { return zero; }
    return given;
}
```
