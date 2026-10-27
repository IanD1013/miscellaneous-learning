对成员进行赋值的成员函数是一个 mutator：它会更改状态，并且不是 const。
仅用于报告状态的函数是一个 accessor，它只读取状态而不更改任何内容，因此在参数列表后带有 `const`：

```cpp
class Level {
public:
    Level() : value_(0) {}

    void raise(int by) {
        if (value_ + by <= 10) {
            value_ += by;
        }
    }

    int value() const {
        return value_;
    }

private:
    int value_;
};
```

`value()` 与其左大括号之间的 `const` 是对对象做出的承诺，编译器会确保你遵守该承诺：在 `value` 内部写 `value_ = 0;` 会导致文件无法通过编译。
给 `raise` 加上 `const` 也会以同样的方式失败，因为对 `value_` 进行赋值正是它的全部工作。

因为 `value_` 是 private 的，`raise` 是唯一的修改途径，这也是该类在操作过程中应用其规则的方式。
`raise` 会拒绝任何会使 level 超过 10 的操作，任何调用者都无法通过直接赋值来绕过它。
保留在 mutator 内部的规则对每个调用者都有效；而写在调用代码中的相同规则只对记住了该规则的调用者有效。

这种差异会被计分。
你无法编辑的 `direct.cpp` 会构建一个 `Toggle`，在没有命令字符串的情况下依次调用各个 mutator，并通过 `const Toggle &` 读取返回的状态词。
它会在请求机器开启前将其锁定，并对未被锁定的机器调用 `unlock`。

### 要求

- `Toggle` 从状态 `off` 开始，并将其状态词保留在 `private:` 标签之后，即使 `class` 在没有该标签时也会默认隐藏成员，这里也必须显式写出。
- mutator 分别命名为 `turnOn`、`turnOff`、`lock` 和 `unlock`，accessor 为 `std::string state() const`。
  `direct.cpp` 对其拥有的 `Toggle` 调用这四个 mutator，并通过 `const Toggle &` 读取返回的状态词，因此如果 accessor 缺少 `const`，将无法在其中通过编译。
- `runCommands` 逐字符遍历 `commands` 并使用 `switch` 分发每个字符：`n` 表示开启，`f` 表示关闭，`l` 表示锁定，`u` 表示解锁。
  任何其他字符都将被忽略，遍历继续进行。
- 当状态为 `locked` 时，`n` 和 `f` 会被拒绝，状态保持为 `locked`。
  `u` 会将处于锁定状态的机器转换为 `off`。
  对未锁定的机器执行 `u` 则保持原样不变。
- 返回机器结束时的状态词，拼写必须完全为 `off`、`on` 或 `locked`，并进行精确比较。
  空命令字符串绝不会改变其初始状态。

### 解答

```cpp
#include <string>

class Toggle {
public:
    Toggle() : state_("off") {}

    void turnOn() {
        // 锁定时拒绝开启
        if (state_ != "locked") {
            state_ = "on";
        }
    }

    void turnOff() {
        // 锁定时拒绝关闭
        if (state_ != "locked") {
            state_ = "off";
        }
    }

    void lock() {
        state_ = "locked";
    }

    void unlock() {
        // 只有锁定的机器才会解锁为 off
        if (state_ == "locked") {
            state_ = "off";
        }
    }

    std::string state() const {
        return state_;
    }

private:
    std::string state_;
};

struct Solution {
    static std::string runCommands(const std::string &commands) {
        // 构建一个 Toggle，用 switch 分发每个命令字符，返回访问器报告的状态
        Toggle machine;
        for (char command : commands) {
            switch (command) {
                case 'n':
                    machine.turnOn();
                    break;
                case 'f':
                    machine.turnOff();
                    break;
                case 'l':
                    machine.lock();
                    break;
                case 'u':
                    machine.unlock();
                    break;
                default:
                    break;
            }
        }
        return machine.state();
    }
};
```
