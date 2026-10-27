本练习的起始代码无法编译，而它产生的诊断信息正是本节的主题。
`countClearing` 将其阈值作为按值传递的形参 `std::unique_ptr<Threshold> gate`，而 `countPassing` 将它刚创建的所有者传递给它：

```cpp
std::unique_ptr<Threshold> gate = std::make_unique<Threshold>(limit);
return countClearing(samples, gate);
```

按值传递的形参是保存所传入内容的第二个变量，因此该调用要求同一个 `Threshold` 拥有第二个所有者，而两个所有者各自都会负责释放同一个对象。
`std::unique_ptr` 无法被复制：任何操作都不能为已经拥有所有者的对象创建负责管理它的第二个变量。
将新创建的所有者赋值给变量（就像第 17.1 课在其循环内替换所有者那样）仍然是被允许的。
这种拒绝发生在文件编译时，而不是运行时。
编译器会停在该调用处（即你写的代码行），并指出 `std::unique_ptr<Threshold>` 及其所需的构造函数被报告为已删除（deleted）。
`deleted` 和 `constructor` 是在该错误块中要寻找的两个词。

### 传递对象本身，而非传递责任

将辅助函数实际使用的内容传递给它。
它只读取阈值而不作任何修改，因此其形参应为 `const Threshold &`，其函数体内通过点号调用 `gate.passes(sample)`（因为它现在持有该对象），并且调用方传入 `*gate`。
`const Threshold &` 会绑定到所有者持有的对象，因此不会发生所有权转移。
唯一的所有者保留在它声明所在的 `countPassing` 中，并在该调用结束时释放 `Threshold`。

`Threshold` 本身可以正常复制；它从来都不是阻碍。

`countPassing` 接收 `const std::vector<double> &samples` 和 `double limit`，并返回有多少个样本超过了该限制。
`passes` 已经是严格比较，因此等于限制的样本不算在内：针对 7.0 测试 `{7.0, 7.0, 9.5}` 将返回 1。
空向量返回 0，样本和限制都在 -50.0 到 50.0 之间，并且只对返回的计数进行评分。
修复辅助函数的形参，修复该调用，并保持文件其余部分不变。
将检查两种写法：辅助函数形参列表中的 `const Threshold`，以及调用处的 `*gate`。
指向所有者的引用（如 `unique_ptr<Threshold> &`）已被禁用，`std::move` 也是如此，它属于后续课程的主题，并且对于仅进行读取的辅助函数来说毫无用处。

### 解答

```cpp
#include <memory>
#include <vector>

class Threshold {
public:
    Threshold(double limit) : limit_(limit) {}

    bool passes(double sample) const { return sample > limit_; }

private:
    double limit_;
};

struct Solution {
    static int countClearing(const std::vector<double> &samples, const Threshold &gate) {
        int count = 0;
        for (double sample : samples) {
            if (gate.passes(sample)) {
                count += 1;
            }
        }
        return count;
    }

    static int countPassing(const std::vector<double> &samples, double limit) {
        std::unique_ptr<Threshold> gate = std::make_unique<Threshold>(limit);
        // 传入所有者持有的对象本身，所有权仍留在这里
        return countClearing(samples, *gate);
    }
};
```
