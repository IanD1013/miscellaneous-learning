`Labeled` 会将其接收到的 `Tracked` 保存在 `item_` 中。
初始代码将其作为 `const Tracked&` 接收并拷贝到 `item_` 中，因此每次调用都会进行一次拷贝。
在 `Labeled l(t, "a")` 中，这种拷贝是必需的：调用者保留了 `t`，之后 `t` 和 `item_` 都持有该 id。
而在 `Labeled l(Tracked(4), "a")` 中，这种拷贝则是浪费的，因为临时对象绑定到 const 引用，被拷贝，然后在语句结束时被销毁。
`std::move(t)` 同样绑定到 const 引用，并以相同的方式被拷贝。
函数保留的参数称为接收端参数（sink parameter），按值传递并在之后将其 move 到成员中，可以仅让保留自身对象的调用者承担拷贝开销。

按值传递时，`item` 是调用时从实参初始化的新 `Tracked`：

- 对于具名的 `t`，运行拷贝构造函数。
  这是唯一的一次拷贝，且 `t` 不会改变。
- 对于像 `Tracked(4)` 这样的临时对象，C++17 直接将对象构造到 `item` 中，既无拷贝也无移动。
- 对于 `std::move(t)`，运行移动构造函数，`t` 的 id 变为 -1，即 `Tracked` 赋予被移走对象的 id。

`item` 此时还不是成员。
它是一个具有名称的局部变量，因此它是一个左值，成员初始化列表中的 `item_(item)` 会对其进行第二次拷贝。
如果这样写，按值传递的构造函数表现得比初始代码更差：具名实参需要两次拷贝，而临时对象或 `std::move` 实参仍需要一次拷贝。
`std::move` 将 `item` 转换为右值，移动构造函数以此构造 `item_`：

```cpp
item_(std::move(item))
```

该 `std::move` 仅从形参移走资源。
在 `Labeled l(t, "a")` 之后，`t` 仍然保留其 id，因为 `item` 是 `t` 的拷贝。

`replace()` 通过将其赋值给 `item_` 来保留其实参，而在 `replace()` 内部形参 `item` 同样也是左值，因此未使用 `std::move` 的赋值会调用拷贝赋值。

一组重载可以达到相同的拷贝次数：一个函数接收 `const Tracked&` 执行拷贝，另一个接收 `Tracked&&` 执行移动。
与按值传递形式相比，它为具名或 `std::move` 实参每次调用节省了一次移动，这在当前场景下影响不大：移动 `Tracked` 仅拷贝一个 `int` 并将源对象的 id 设置为 -1。
其代价在于函数数量。
每个保留的形参都会使函数所需的重载数量翻倍，因此一个同时保留 `item` 和 `label` 的构造函数需要四个重载。
而按值传递时，每个函数只需编写一次。

### 任务

修改 `labeled.hpp` 中的构造函数和 `replace()`，使具名实参仅需一次拷贝，临时对象或 `std::move` 实参无需拷贝，且 `item_` 从实参拷贝或移动，而不是根据其 `id()` 构建新的 `Tracked`。
构造函数同样保留 `label`，因此为其采用相同的形式。
`item()`、`label()` 以及这两个成员保持原样。

`tracked.hpp` 是只读的。
一个 `Tracked` 包含一个 `int` 类型的 id。
它的拷贝构造函数和拷贝赋值操作符每次都会使 `Tracked::copies()` 返回的计数加 1，而其移动构造函数和移动赋值操作符每次都会使 `Tracked::moves()` 加 1。
每次从 `int` 构造还会获得一个唯一的 origin 标记；拷贝或移动会保留该标记。
`origin()` 返回该标记。
计数器是 `inline static` 数据成员，C++17 允许类在其自身主体内部定义此类成员，因此头文件无需单独的定义。
`driver.cpp` 包含四个函数：

- `fromNamed(id)` 构建 `Tracked t(id)` 然后构建 `Labeled l(t, "a")`，并返回产生的拷贝次数、`l.item().id()` 和 `t.id()`。
- `fromTemporary(id)` 构建 `Labeled l(Tracked(id), "a")` 并返回产生的拷贝次数、是否发生移动（1 表示是，0 表示否）以及 `l.item().id()`。
- `fromMoved(id)` 构建 `Tracked t(id)` 然后构建 `Labeled l(std::move(t), "a")`，并返回产生的拷贝次数和 `l.item().id()`。
- `replaceBoth(first, second)` 从 `Tracked(first)` 构建 `l`，然后使用持有 `second` 的具名 `Tracked` 调用 `l.replace()`，接着使用 `Tracked(first + second)` 再次调用。
  它返回第一次调用产生的拷贝次数、两次调用总共产生的拷贝次数、`l.item().id()`，随后紧跟两项 origin 检查：当成员保留具名实参的 origin 时为 1，当保留临时对象的 origin 时为 1（否则为 0）。

对于 `replaceBoth`，结果可解读为 [具名调用后的拷贝次数, 两次调用后的拷贝次数, 最终 id, 具名 origin 是否保留, 临时 origin 是否保留]。
当两个函数都完成后，`replaceBoth(1, 2)` 返回 `[1, 1, 3, 1, 1]`：具名 `Tracked` 进行一次拷贝，临时对象无额外拷贝，得到 `Tracked(1 + 2)` 的 id，且两个 origin 均得以保留。

### 解答

```cpp
#pragma once
#include <string>
#include <utility>
#include "tracked.hpp"

class Labeled {
public:
    // 按值接收，再 move 到成员中
    Labeled(Tracked item, std::string label) : item_(std::move(item)), label_(std::move(label)) {}
    void replace(Tracked item) { item_ = std::move(item); }

    const Tracked& item() const { return item_; }
    const std::string& label() const { return label_; }

private:
    Tracked item_;
    std::string label_;
};
```
