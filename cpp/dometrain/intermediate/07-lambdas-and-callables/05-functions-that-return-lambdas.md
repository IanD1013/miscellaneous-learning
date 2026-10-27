`makeAffine(2, 3)` 返回一个 lambda，而 `driver.cpp` 仅在 `makeAffine` 返回之后（此时形参 `scale` 和 `offset` 已经被销毁）才调用该 lambda。
该 lambda 仍然能正常工作，原因在于值捕获（capture by value）：捕获列表在 `return` 语句处将两者都复制到了 lambda 对象中，并且这些副本的生命周期与 lambda 本身一样长。
下面是具有相同形式的一个单配置示例：

```cpp
inline auto makeShift(int amount) {
    return [amount](int value) { return value + amount; };
}

auto addTen = makeShift(10);
int result = addTen(5);   // 15，来自 addTen 内部的 amount 副本
```

将捕获改为 `[&amount]`，编译器仍然不会报错。
但此时 lambda 引用了 `makeShift` 的形参，而该形参在 `makeShift` 返回时就已销毁，因此每次调用 `addTen` 都会读取一个不再存在的变量。
这是未定义行为（undefined behavior）：它今天可能返回 15，但在一次无关的修改之后就可能返回其他内容。

每个 lambda 表达式都有其自己独有的类型，且无法直接写出该类型的名称，因此 `makeShift` 将其返回类型声明为 `auto`，编译器会根据 `return` 语句对其进行推导：调用者将获得 lambda 本身。
返回类型写为 `std::function<int(int)>` 也能通过编译，并在返回时将 lambda 包装起来。
不过，`auto` 只能推导单一类型，因此如果一个函数根据其参数返回两种不同 lambda 之一，则需要使用 `std::function`。
`makers.hpp` 中的返回类型已经写好：`makeAffine` 使用了 `auto`，而当其 lambda 传递给 `compose` 或 `repeat` 时会转换为 `std::function<int(int)>`。

### 组合可调用对象

`compose(outer, inner)` 接收两个可调用对象并返回一个新的可调用对象。
这就是函数组合（function composition）：其结果是在其参数上运行 `inner`，然后在 `inner` 的返回值上运行 `outer`，即 `outer(inner(value))`。
`outer` 写在前面但运行在后，因为 `inner(value)` 是它的实参，而在调用函数之前必须先对其传入的实参求值。
返回的 lambda 需要拥有自己的 `outer` 和 `inner`，其原因与 `makeShift` 捕获 `amount` 相同。
`compose` 是按值接收这两者的，且在 `return` 之后不会再使用它们，因此请使用初始化捕获（init captures）将它们移动到 lambda 中，而不是复制它们：复制 `std::function` 会复制其持有的可调用对象。

执行顺序决定了 offset 是否会被缩放。
以下是使用参数 5 调用 `compose(makeAffine(3, 0), makeAffine(1, 4))` 的情况，旁边对比了先运行 `outer` 的版本：

```text
                     第一次调用          第二次调用          结果
先 inner 后 outer    5 * 1 + 4 = 9       9 * 3 + 0 = 27      27
先 outer 后 inner    5 * 3 + 0 = 15      15 * 1 + 4 = 19     19
```

在第一行中，4 是在翻三倍之前加上的，因此它也会被翻三倍。

`Solution::composed` 会从其第一个 scale 和 offset 构建 `outer`，从第二个构建 `inner`。
有两个测试用例会以相反的顺序传入相同的 maker 来调用它：`(2, 0, 1, 3, 5)` 和 `(1, 3, 2, 0, 5)`。
手动算出这两个结果，然后运行程序验证你的执行顺序是否正确。

`repeat(step, times)` 将单步操作与自身进行组合：当 `times` 为 3 时，它计算 `step(step(step(value)))`；当 `times` 为 0 时，它原样返回 `value`。

### 需要编写的内容

补全 `makers.hpp` 中的四个 maker，每个 maker 都要返回一个通过值捕获所需内容的 lambda：

- `makeAffine(scale, offset)`：该 lambda 将其参数乘以 `scale`，然后加上 `offset`。
- `compose(outer, inner)` 和 `repeat(step, times)`：按照上文描述的方式工作。
- `makeRangeCheck(low, high)`：当值介于 `low` 到 `high` 之间（均包含两端边界）时，该 lambda 返回 `true`。

`driver.cpp` 会调用每个 maker，待其返回后，再调用返回的结果。
`Solution::countInRange` 会统计列表中使范围检查返回 `true` 的值的数量。

### 解答

```cpp
#pragma once
#include <functional>
#include <utility>

inline auto makeAffine(int scale, int offset) {
    // 按值捕获，maker 返回后依然有效
    return [scale, offset](int value) { return value * scale + offset; };
}

inline std::function<int(int)> compose(std::function<int(int)> outer, std::function<int(int)> inner) {
    // 移动进 lambda，先运行 inner 再运行 outer
    return [outer = std::move(outer), inner = std::move(inner)](int value) { return outer(inner(value)); };
}

inline std::function<bool(int)> makeRangeCheck(int low, int high) {
    return [low, high](int value) { return value >= low && value <= high; };
}

inline std::function<int(int)> repeat(std::function<int(int)> step, int times) {
    // 调用 times 次 step，times 为 0 时原样返回
    return [step = std::move(step), times](int value) {
        for (int i = 0; i < times; ++i) {
            value = step(value);
        }
        return value;
    };
}
```
