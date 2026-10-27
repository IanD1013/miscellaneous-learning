来自 `<functional>` 的 `std::function<int(int)>` 可以容纳任何接受一个 `int` 并返回一个 `int` 的可调用对象。
它的模板参数是调用签名：返回类型，后跟括号中的参数类型。
捕获型 lambda、像 `Multiply` 这样的函数对象以及像 `negate` 这样的普通函数都具有不同的类型，而 vector 中的每个元素必须具有相同的类型。
一个 `std::function<int(int)>` 可以容纳它们中的任何一个，并且每个都可以用相同的方式调用：

```cpp
int negate(int value) { return -value; }

int amount = 3;
std::function<int(int)> f = [amount](int value) { return value + amount; };
f(5);              // 8
f = Multiply{2};   // Multiply::operator() 返回 value * factor
f(5);              // 10
f = negate;
f(5);              // -5
```

`std::function` 会存储可调用对象自身的一份副本。
`f` 内部的 lambda 副本保存了它自己的一份 `amount` 副本，因此在构建 `f` 所用的 lambda 销毁后，`f` 仍能继续工作。
拷贝按引用捕获的 lambda 会拷贝该引用，而不是局部变量，因此该局部变量的生命周期仍然必须长于通过该 `std::function` 发起的每一次调用。

函数指针 `int (*)(int)` 可以容纳 `negate`，并且空捕获列表的 lambda 可以转换为函数指针。
捕获了 `amount` 的 lambda 则没有这种转换，因为函数指针没有地方来保存 `amount`，而携带因数的 `Multiply` 对象同样无法转换。
`std::vector<int (*)(int)>` 会拒绝本课存储的三种步骤中的两种；而 `std::vector<std::function<int(int)>>` 则能容纳全部三种。

### 空的 std::function

`std::function<void(int)>` 容纳接受一个 `int` 且无返回值的可调用对象。
默认构造的 `std::function` 不包含任何可调用对象；它是空的。
调用一个空的 `std::function` 并不会静默地什么都不做；程序会在该处终止。
它可以转换为 `bool`，为空时为 `false`，因此可能未设置的回调在每次调用之前都会进行检查：

```cpp
int last = 0;
std::function<void(int)> observer;                // 空
if (observer) { observer(1); }                    // 跳过，last 仍为 0
observer = [&last](int value) { last = value; };
if (observer) { observer(2); }                    // last 现在为 2
```

在 `Pipeline` 中，`observer_` 是默认构造的，因此在 `setObserver` 存储可调用对象之前，`if (observer_)` 均为 false。

### 编写内容

在 `pipeline.hpp` 中补全 `Pipeline`：

- `addStep(step)` 将 `step` 添加到已存储的步骤之后，而 `setObserver(observer)` 将 `observer` 存储到 `observer_` 中。
  两者均按值接收 `std::function`，以便移动到成员中。
- `run(value)` 按添加顺序依次应用各个步骤，每个步骤都作用于前一个步骤的结果，并返回最后一个结果；当没有步骤时返回 `value` 本身。
  当设置了 observer 时，`run` 会在每个步骤之后调用它一次并传入该步骤的结果。
  在未设置 observer 的情况下，所有步骤仍会正常运行。
- `stepCount()` 返回已存储步骤的数量。

`driver.cpp` 为每个 op 添加一个步骤：对于 `"add"`，添加一个按值捕获其 amount 的 lambda；对于 `"mul"`，添加一个 `Multiply` 对象；对于 `"negate"`，添加函数 `negate`（它会忽略其 amount）。
`Solution::runObserved` 设置一个按引用捕获局部 `std::vector<int>` 并追加其收到的每个值的 observer，然后返回 `run` 的结果以及这些值。
`runObserved({"add", "mul"}, {3, 2}, 5)` 从 5 开始，先加 3 然后乘 2：

```text
[结果, 第 1 步之后的值, 第 2 步之后的值]
[16, 8, 16]
```

`Solution::runQuiet` 从不调用 `setObserver`，并返回结果以及随后的 `stepCount()`。

在运行之前先检查一下：`runObserved({}, {}, 7)` 设置了一个 observer 且未添加任何步骤。
它会返回多少个值？

### 解答

```cpp
#pragma once
#include <functional>
#include <utility>
#include <vector>

class Pipeline {
public:
    void addStep(std::function<int(int)> step) {
        steps_.push_back(std::move(step));
    }

    void setObserver(std::function<void(int)> observer) {
        observer_ = std::move(observer);
    }

    int run(int value) const {
        for (const auto& step : steps_) {
            value = step(value);
            // 空的 observer 不调用
            if (observer_) {
                observer_(value);
            }
        }
        return value;
    }

    int stepCount() const {
        return static_cast<int>(steps_.size());
    }

private:
    std::vector<std::function<int(int)>> steps_;
    std::function<void(int)> observer_;
};
```
