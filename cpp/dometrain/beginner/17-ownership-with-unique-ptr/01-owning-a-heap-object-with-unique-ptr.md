一个局部变量可以持有一个堆对象并自行归还。
`std::unique_ptr` 就是这样的变量，而 `std::make_unique` 负责填充它：

```cpp
#include <memory>

class Meter {
public:
    Meter(int start) : reading_(start) {}
    void step() { reading_ += 1; }
    int reading() const { return reading_; }

private:
    int reading_;
};

int twoSteps() {
    std::unique_ptr<Meter> owner = std::make_unique<Meter>(4);
    owner->step();
    owner->step();
    return owner->reading();
}
```

`std::unique_ptr<Meter>` 声明了一个名为 `owner` 的普通局部变量。
尖括号内的类型是被拥有的对象本身的类型（即 `Meter` 本身），绝不是指针类型：`std::make_unique<Meter *>()` 会生成一个指针的拥有者，而在其后编写的第一个箭头操作符会被拒绝，因为指针没有成员。
只要 `owner` 处于生存期内，它的行为就类似于指向该 `Meter` 的指针，这也是通过 `owner->step()` 访问其成员的原因。

`std::make_unique<Meter>(4)` 在一个表达式中完成了三项工作。
它在堆上分配单个 `Meter`，将其自身括号内的所有内容作为构造函数参数传递给该类型的构造函数，并生成构建好的拥有者。
空括号会运行不接受参数的构造函数，因此在您接触该对象之前它就已经被构建和初始化完毕，并且您的文件中绝不会出现原始指针。

当 `owner` 超出作用域时会触发释放。
`twoSteps` 的闭合花括号结束了该变量的生命周期，它所持有的 `Meter` 会在同一时刻自动释放，这适用于退出函数的所有路径（包括提前返回）。
因为 `owner` 不是指针，所以在那里编写 `delete owner;` 并不能清理任何东西，反而会导致文件编译失败。

这两个名称都来自声明它们的头文件 `#include <memory>`，初始代码已经在文件顶部包含了该指令。

初始代码定义了包含 `add(int)` 和 `total() const` 的 `Accumulator`，并且 `accumulateValues` 接收 `const std::vector<int> &values` 并返回一个供评分器直接比较的 `int`。
在循环上方使用 `std::make_unique<Accumulator>()` 构建一个 `Accumulator`（在禁用 `new` 和 `delete` 后，这是唯一的途径）。
使用 `owner->add(value)` 将 `values` 的每个元素输入其中，并返回 `owner->total()`。
除了 `std::make_unique<` 之外，这两种写法也会被检查，因为在拥有者旁边用普通 `int` 保存累计和虽然能返回相同的数字，但被拥有的对象却始终未被使用。
元素范围为 -1000 到 1000，重复值每次出现都会计算一次，由于构造函数将总和初始设为 0，因此空 vector 返回 0。

## 解答

```cpp
#include <memory>
#include <vector>

class Accumulator {
public:
    Accumulator() : total_(0) {}

    void add(int amount) { total_ += amount; }

    int total() const { return total_; }

private:
    int total_;
};

struct Solution {
    static int accumulateValues(const std::vector<int> &values) {
        // 用 unique_ptr 持有一个 Accumulator，调用结束时自动释放；把每个元素加进去，再返回它累计的总和
        std::unique_ptr<Accumulator> owner = std::make_unique<Accumulator>();
        for (int value : values) {
            owner->add(value);
        }
        return owner->total();
    }
};
```
