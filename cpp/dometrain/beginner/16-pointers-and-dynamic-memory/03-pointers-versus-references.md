引用和指针都可以让函数访问调用者的对象而无需复制它，它们之间的一个区别特性是：引用不能为空（null）。

```cpp
void bump(int &value) {
    value += 1;
}

void bumpIfPresent(int *value) {
    if (value != nullptr) {
        *value += 1;
    }
}
```

`int &value` 在调用时绑定到一个对象。
它之后不能指向其他地方，而且不能定义不指向任何对象的引用，因此 `bump` 可以立即使用它而无需检查。
`int *value` 保存一个地址，可以通过给指针赋值指向其他地方，并且可以保存 `nullptr`，因此 `bumpIfPresent` 获得了报告没有什么可增加的能力，代价是在每次解引用前都要进行比较。
你声明的每个参数都以三种方式解决同一个问题：当函数只读取时复制一个小值；当调用者总是有对象可访问时使用引用；当调用者可能没有任何东西可提供时使用指针。
“是否存在”区分了后两者，而“只读而非访问”将复制与这两者区分开来。
速度并不是决定性的属性。

`int &value` 中的 `&` 属于参数的类型，因此调用写作 `bump(total)`，实参前面不需要添加任何额外内容。

### 三个辅助函数

`combinedTotal` 已经为你编写好并调用了所有这三个函数；保持其不变。
它从 `start` 开始初始化 `total`，构造一个仅在 `factorPresent` 为 `true` 时才为 `&factor` 的 `const int *`，并返回 total 加上标签的权重。

- `applyFactor` 必须接收当前的运行累计值作为 `int &`，并将 factor 作为 `const int *`，因为驱动代码在不携带 factor 的调用中会传递 `nullptr`。
  在相乘之前比较指针；规则要求你的答案中包含 `nullptr)`，例如 `if (factor != nullptr)`。
  当传入 factor 时乘以调用者的 total，未传入时则保持不变。
  如果缺少比较，则会乘以读取空指针产生的 0。
- `raiseToFloor` 也必须接收运行累计值作为 `int &`。
  它的 `int floorValue` 保持为普通拷贝，因为该函数只读取它。
  当 total 低于 `floorValue` 时，将 total 提升至 `floorValue`。
- `labelWeight` 已经接收 `const std::string &label`，这样可以在不复制的情况下读取。
  将其字符数作为 `int` 返回。

输入保持较小范围：`start` 为 1 到 100，factor 为 2 到 9，floor 为 0 到 200，label 为 0 到 20 个字符。

### 解答

```cpp
#include <string>

struct Solution {
    static void applyFactor(int &total, const int *factor) {
        // 传入了 factor 时，把调用者的 total 乘以它
        if (factor != nullptr) {
            total = total * *factor;
        }
    }

    static void raiseToFloor(int &total, int floorValue) {
        // total 低于 floorValue 时，把它提升到 floorValue
        if (total < floorValue) {
            total = floorValue;
        }
    }

    static int labelWeight(const std::string &label) {
        // 返回标签的字符数
        return label.size();
    }

    static int combinedTotal(int start, int factor, bool factorPresent, int floorValue, const std::string &text) {
        int total = start;
        const int *factorPointer = nullptr;
        if (factorPresent) {
            factorPointer = &factor;
        }
        applyFactor(total, factorPointer);
        raiseToFloor(total, floorValue);
        return total + labelWeight(text);
    }
};
```
