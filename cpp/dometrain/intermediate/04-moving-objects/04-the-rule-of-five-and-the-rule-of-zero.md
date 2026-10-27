在当前初始代码中，移动一个 `Snapshot` 的开销与复制它完全相同：`Snapshot c(std::move(a))` 会复制 `a` 中的每一个 `Tracked` 项，`d = std::move(a)` 也是如此，而且没有任何报错。
仅当一个类未声明以下三者中的任何一个时，编译器才会为该类自动生成移动构造函数和移动赋值运算符：析构函数、拷贝构造函数、拷贝赋值运算符。
只要声明了其中任何一个，编译器就不会生成这两种移动操作。

关键在于声明本身，无论其函数体是什么。
一个什么都不做的析构函数依然会关闭移动操作的自动生成；即使声明为 `= default` 也是如此，尽管这请求的恰好就是编译器原本会生成的析构函数。
`std::move(a)` 只不过是向右值的类型转换，因此无论怎样都能通过编译。
当 `Snapshot` 没有移动构造函数时，就没有构造函数接受 `Snapshot&&`，该右值便会绑定到拷贝构造函数的 `const Snapshot&` 上，同理 `d = std::move(a)` 也会调用拷贝赋值运算符。

### 零法则（The rule of zero）

编译器生成的特殊成员函数是逐成员（memberwise）操作的。
其拷贝构造函数使用 `std::string` 的拷贝构造函数复制 `name_`，并使用 `std::vector` 的拷贝构造函数复制 `items_`，这会将每个 `Tracked` 复制一次。
而其移动构造函数和移动赋值运算符则分别移动每个成员，被移动的 `std::vector` 会将其缓冲区移交给目标对象，因此不会复制甚至不会移动任何 `Tracked`。
如果一个类的成员已经能够正确地自行复制和移动，那么该类就不应声明这五个特殊成员中的任何一个：析构函数、拷贝构造函数、拷贝赋值运算符、移动构造函数以及移动赋值运算符。
这就是零法则（Rule of Zero）。
在这样的类中，手写的析构函数或拷贝操作要么只是重复编译器本就会生成的操作，要么容易写错，而且一旦声明它们，该类就会失去自动生成的移动操作。

### 五法则（The rule of five）

`IntBuffer` 则是另一种情况。
它的析构函数需要释放一块内存，因此根据三法则（Rule of Three），它定义了自己的拷贝构造函数和拷贝赋值运算符，而这些声明导致它失去了编译器生成的移动操作。
C++ 这样做是有意为之：对 `IntBuffer` 进行逐成员移动会复制其指针，导致两个对象分别释放同一块内存。
只有通过定义移动构造函数和移动赋值运算符来接管该内存块并将源对象置空，它才能重新获得移动操作。
一个直接管理资源的类需要定义或删除这五个特殊成员中的每一个，这就是五法则（Rule of Five）。
删除也算在内：例如一个可以移动但不能复制的类（如 `std::unique_ptr`），会在其拷贝构造函数和拷贝赋值运算符上写 `= delete`，并定义这两个移动操作。

声明移动构造函数或移动赋值运算符在反方向上同样有效：此时编译器的拷贝构造函数和拷贝赋值运算符会被隐式删除（deleted），并且编译器也不会再自动生成另一个移动操作。
因此，一旦一个类声明了这五个中的某一个，就需要声明全部五个。
`= default` 可以显式按名称请求编译器版本的特殊成员，无需担心在函数体中犯错。
这两个移动操作如下所示，析构函数和拷贝操作也以同样的方式 default：

```cpp
Snapshot(Snapshot&& other) = default;
Snapshot& operator=(Snapshot&& other) = default;
```

手写的函数体仍有可能发生复制。
当 `Snapshot c(std::move(a))` 调用以下移动构造函数时，每个项都会被复制：

```cpp
Snapshot(Snapshot&& other) : name_(std::move(other.name_)), items_(other.items_) {}
```

在其内部，`other` 具有名称，因此 `other.items_` 是左值，会调用 `std::vector` 的拷贝构造函数。
若要移动它，需要写成 `items_(std::move(other.items_))`，即每个成员都需要一个 `std::move`，而 `= default` 会为每个成员自动完成这一操作。

对所有五个特殊成员使用 default 对 `Snapshot` 来说是正确的，因为它的成员已经自行管理数据，所以编译器逐成员的版本能够正确地复制和移动它们。
但对于 `IntBuffer` 而言，这会重新引入 bug：default 的拷贝或移动会复制原始指针，导致两个缓冲区释放同一块内存。

### 需要修改的内容

修改 `snapshot.hpp` 中的 `Snapshot`，使拷贝构造和拷贝赋值仍将每个项复制一次，而移动构造和移动赋值不复制任何项。
保持构造函数、`add()`、`count()` 和 `firstId()` 不变。
找出 `Snapshot` 中被上述规则所涉及的声明，并针对每一个声明决定该类是否真正需要它。

`driver.cpp` 中的每个函数都会通过 `add()` 向名为 `a` 的 `Snapshot` 填充 `count` 个项。

- `copyThenMoveCost(count)` 将 `b` 构建为 `a` 的副本，然后从 `a` 移动构造 `c`，并返回五个值。
- `moveAssignCost(count)` 将 `a` 移动赋值给名为 `d` 的空 `Snapshot`，并返回两个值。
- `copyAssignCost(count)` 将 `a` 拷贝赋值给名为 `e` 的空 `Snapshot`，并返回两个值。

对于初始代码和修复后的 `Snapshot`，它们返回：

```text
各位置                 [b 的拷贝次数, b.count(), c 的拷贝次数, c.count(), c.firstId()]

                       初始代码           修复后
copyThenMoveCost(3)    [3, 3, 3, 3, 0]    [3, 3, 0, 3, 0]

各位置                 [d 的拷贝次数, d.count()]

                       初始代码           修复后
moveAssignCost(4)      [4, 4]             [0, 4]

各位置                 [e 的拷贝次数, e.count()]

                       初始代码           修复后
copyAssignCost(3)      [3, 3]             [3, 3]
```

### 解答

```cpp
#pragma once
#include <string>
#include <utility>
#include <vector>
#include "tracked.hpp"

// 零法则：成员能自行拷贝和移动，不声明任何特殊成员函数
class Snapshot {
public:
    explicit Snapshot(std::string name) : name_(std::move(name)) {}
    void add(Tracked item) { items_.push_back(std::move(item)); }
    int count() const { return static_cast<int>(items_.size()); }
    int firstId() const { return items_.empty() ? -1 : items_[0].id(); }

private:
    std::string name_;
    std::vector<Tracked> items_;
};
```
