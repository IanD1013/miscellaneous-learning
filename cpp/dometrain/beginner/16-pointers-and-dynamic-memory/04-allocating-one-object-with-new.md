`new` 会在执行它的函数之外为一个对象分配空间，并在那里构建该对象且返回其地址：

```cpp
int *p = new int(7);

delete p;
```

括号中的内容用于构建对象：`new Item(3)` 会像声明局部变量一样传入 3 来运行构造函数。
返回的是一个指针，而不是对象本身，这也是为什么它被保存在 `Item *` 中。

生命周期是它与局部变量的区别所在。
局部变量在其作用域代码块的右花括号处销毁；而使用 `new` 创建的对象不与任何作用域绑定，它会一直存在，直到被 `delete` 释放。
`delete p` 会运行析构函数并归还内存；除此之外没有任何其他方式能结束该对象的生命周期。
如果在释放操作之前执行了 `return`，对象会被遗弃而不是被清理，因此在每次 return 之前（包括发生错误的分支路径）都必须恰好执行一次释放；位于函数底部的 `delete` 仅在上方没有任何分支提前 return 时才会起作用。
需要注意两个细节：对 `nullptr` 执行 `delete` 是有明确定义的且什么都不做；指针在释放后仍然保留着旧地址，因此写在 `delete` 下方的成员调用依然可以通过编译，但读取的却是一个不再属于你的内存块。
请在对象存活期间将所需的数据复制出来。

该文件提供了 `destroyedCount` 和类 `LongestSoFar`；请保持这两者完全不变。
它的构造函数接受上限值，`offer(label)` 保留该上限内最长的标签，`length()` 报告该长度，其析构函数会给 `destroyedCount` 加 1。
在每个测试用例中计数器都从 0 开始，因此结果中的 1 可以证明你的对象已被销毁。

`longestLabelReport` 接收 `const std::vector<std::string> &labels` 和一个 `int maxLength`，并返回包含两个 int 的 `std::vector<int>`。
使用 `new LongestSoFar(maxLength)` 构建一个 tracker（会检查拼写），并按顺序将每个 label 传给它。
在 tracker 存活期间将其 `length()` 复制到一个 `int` 中，将其释放，然后返回结果，其中复制的长度放在第一位，`destroyedCount` 放在第二位。
通过指针访问成员可以使用 `tracker->offer(label)`。
tracker 必须在每条路径上都被释放，因此如果某个 label 的长度超过 `maxLength`，在执行其自身的 `delete` 之后，第一个位置应返回 -1。
长度等于 `maxLength` 是允许的，而没有标签时应返回 `[0, 1]`。
`unique_ptr` 被禁用；下一章会介绍更整洁的方式，而本节课练习的是手动管理。

## 解答

```cpp
#include <string>
#include <vector>

// 提供的固定代码：保持下面的计数器和类完全不变。
int destroyedCount = 0;

class LongestSoFar {
public:
    LongestSoFar(int maxLength) : cap_(maxLength), best_(0) {}
    ~LongestSoFar() { destroyedCount = destroyedCount + 1; }
    void offer(const std::string &label) {
        int size = label.size();
        if (size <= cap_ && size > best_) {
            best_ = size;
        }
    }
    int length() const { return best_; }
private:
    int cap_;
    int best_;
};

struct Solution {
    static std::vector<int> longestLabelReport(const std::vector<std::string> &labels, int maxLength) {
        // 用 new 构建 tracker，把每个标签交给它，每条路径上都用 delete 释放
        LongestSoFar *tracker = new LongestSoFar(maxLength);
        for (const std::string &label : labels) {
            int size = label.size();
            if (size > maxLength) {
                delete tracker;
                return std::vector<int>{-1, destroyedCount};
            }
            tracker->offer(label);
        }
        int length = tracker->length();
        delete tracker;
        return std::vector<int>{length, destroyedCount};
    }
};
```
