一个拥有 `Scale` 对象的 `std::unique_ptr<Stage>` 会通过对其持有的 `Stage*` 执行 `delete` 来销毁该对象。
它不会记住该对象原本是以 `Scale` 的形式创建的，因此它会调用 `~Stage`，这与对任何基类指针执行 `delete` 的效果相同。

如果 `~Stage` 是虚析构函数，该调用将像任何虚函数调用一样进行派发：`~Scale` 执行，然后 `Stage` 部分被销毁，顺序与构造顺序相反。
如果它不是虚函数，则行为是未定义的（undefined behavior）。
在本课程使用的编译器下，仅会执行 `~Stage`，派生类的析构函数永远不会执行，而且不会报错；而其他编译器可能会有不同的行为。
必须防止这种没有任何迹象的错误发生，因此旨在通过基类指针拥有所有权的基类从一开始就应将其析构函数声明为虚函数：

```cpp
class Stage {
public:
    virtual ~Stage() { note("-stage"); }
};

class Scale : public Stage {
public:
    ~Scale() override { note("-scale"); }
};
```

`note()` 来自 `trace.hpp`，用于向共享列表中追加一条记录。
`~Scale` 上的 `override` 作用与其他成员函数相同：编译器会确认 `~Stage` 是否为虚函数，因此如果 `~Stage` 上的 `virtual` 被删除，`~Scale` 将无法通过编译。

初始代码中的 `~Stage() {}` 不是虚函数，在将其改为虚函数之前，`driver.cpp` 对每个测试用例都会返回 `["Stage needs a virtual destructor"]`。

### 基类所有者的 vector

`std::make_unique<Scale>(2)` 返回一个 `std::unique_ptr<Scale>`，只要在需要 `std::unique_ptr<Stage>` 的地方，它就会转换为 `std::unique_ptr<Stage>`，就像 `Scale*` 转换为 `Stage*` 一样。
因此，一个 `std::vector<std::unique_ptr<Stage>>` 可以容纳所有三种 stage。

在 `add` 内部，参数 `stage` 本身是一个具名的所有者，因此 `stages_.push_back(stage)` 会要求 vector 进行复制，导致编译失败。
它需要像任何具名的 `std::unique_ptr` 一样，通过 `std::move` 传入。

`erase` 会通过移动赋值将所擦除元素后面的每个所有者向前移动一个槽位，然后销毁留在最后一个槽位的所有者。
被擦除 stage 的所有者会被下一个所有者覆盖赋值；如果是最后一个，则直接被销毁。
在这两种情况下，`std::unique_ptr` 都会删除它所持有的内容，因此派生类的析构函数和 `~Stage` 都会在 `erase` 返回之前运行。
仍在 vector 中的 stage 会在 `Pipeline` 离开作用域时被销毁，因此 `Pipeline` 不需要自己的析构函数。

### 需要编写的内容

补全 `stages.hpp` 中的类：

- `Stage` 获得上述虚析构函数以及一个返回 `value` 的虚函数 `apply(int value) const`。
- `Scale`、`Offset` 和 `ClampAbove` 重写（override）`apply`。
  `Scale` 将值乘以其 factor，`Offset` 加上其 amount，而 `ClampAbove` 在值高于 ceiling 时返回其 ceiling，否则返回值本身。
  它们的析构函数分别记录 `"-scale"`、`"-offset"` 和 `"-clamp"`。
- `Pipeline` 在 stage 的整个生命周期内将其保存在其 `std::unique_ptr<Stage>` 中，绝不要使用 `release()` 将其取出，也不要手动 delete。
- `run(value)` 按添加顺序将值传递给各 stage 并返回结果；若没有 stage，则返回 `value` 本身。
  `size()` 返回 stage 的数量。
- `removeAt(index)` 擦除位于 `index` 的 stage 并返回 `true`。
  对于超出 0 到 `size() - 1` 范围的任何索引，它不移除任何内容并返回 `false`。

`driver.cpp` 中的 `Solution::runPipeline` 会添加各个 stage，以测试用例的索引调用 `removeAt`，并将起始值传入运行。
它返回三个字符串：`run` 返回的内容；在 `removeAt` 期间记录且无分隔符连接的移除记录（当返回 `false` 时为 `"refused"`）；以及在 `Pipeline` 销毁时记录的结束记录，已排序并用逗号连接。

`runPipeline({"scale", "offset", "clamp"}, {2, 3, 12}, 5, 1)` 构建 Scale(2)、Offset(3) 和 ClampAbove(12)，移除索引 1 并将 5 传入剩余的 stage 运行。
其结果下方是同一个测试用例在 `removeAt` 返回 `true` 但没有擦除任何内容时的输出：

```text
                                 [run(5), 移除记录, 结束记录]
removeAt 擦除了 Offset          ["10", "-offset-stage", "-clamp,-scale,-stage,-stage"]
返回 true，但未擦除任何内容      ["12", "", "-clamp,-offset,-scale,-stage,-stage,-stage"]
```

在第一行中，Offset 的两个析构函数均在 `removeAt` 内部运行，且 5 \* 2 = 10 低于 ceiling。
在第二行中，Offset 仍在 vector 中，因此 5 \* 2 + 3 = 13 被截断（clamped）为 12，其记录直到 `Pipeline` 被销毁时才输出。

当所有测试用例都通过后，仅从 `~Offset` 中删除 `override`。
第一行还会显示 `-offset-stage` 吗？
在运行之前先给出你的判断吧。

### 解答

```cpp
#pragma once
#include <memory>
#include <utility>
#include <vector>
#include "trace.hpp"

class Stage {
public:
    virtual ~Stage() { note("-stage"); }
    virtual int apply(int value) const { return value; }
};

class Scale : public Stage {
public:
    explicit Scale(int factor) : factor_(factor) {}
    ~Scale() override { note("-scale"); }
    int apply(int value) const override { return value * factor_; }

private:
    int factor_;
};

class Offset : public Stage {
public:
    explicit Offset(int amount) : amount_(amount) {}
    ~Offset() override { note("-offset"); }
    int apply(int value) const override { return value + amount_; }

private:
    int amount_;
};

class ClampAbove : public Stage {
public:
    explicit ClampAbove(int ceiling) : ceiling_(ceiling) {}
    ~ClampAbove() override { note("-clamp"); }
    int apply(int value) const override { return value > ceiling_ ? ceiling_ : value; }

private:
    int ceiling_;
};

class Pipeline {
public:
    // 具名的 unique_ptr 必须 move 进 vector
    void add(std::unique_ptr<Stage> stage) { stages_.push_back(std::move(stage)); }

    bool removeAt(int index) {
        if (index < 0 || index >= size()) return false;
        stages_.erase(stages_.begin() + index);
        return true;
    }

    int run(int value) const {
        for (const auto& stage : stages_) value = stage->apply(value);
        return value;
    }

    int size() const { return static_cast<int>(stages_.size()); }

private:
    std::vector<std::unique_ptr<Stage>> stages_;
};
```
