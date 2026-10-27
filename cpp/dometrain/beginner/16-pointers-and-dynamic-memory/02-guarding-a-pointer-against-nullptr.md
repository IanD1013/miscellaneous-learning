一个持有 `nullptr` 的指针不指向任何内容，而解引用是绝对不能对其执行的操作。
在桌面编译器上，这种读取通常会发出明显警报（崩溃）。
但在这里它是静默的：探测显示它会返回 0 并且运行正常结束，因此唯一的症状就是一个看似确信的错误答案。

因此，比较操作必须放在读取操作之前：

```cpp
const int *found = nullptr;

if (found == nullptr) {
    return -1;
}
int value = *found;
```

这里的 `const` 修饰的是所指向的目标而非指针本身：该地址处的 int 可以通过 `found` 读取，但绝不能通过它写入。
`firstAtLeast` 返回的正是这种类型，因此接收其返回值的行应写为 `const int *found = firstAtLeast(values, threshold);`。
如果写成 `int *found`，该行就声明了辅助函数从未赋予的写入权限，编译器将会拒绝编译。

`nullptr` 是你需要显式写出的值，而不是语言提供的默认值。
从未被赋予该值的指针包含一个不确定的值，读取时可能为零或任何其他值，任何比较操作都无法挽救它。
在声明每个指针的行上，就给它赋一个有效值。
随后的检查就是你已经用过的保护子句（guard clause）：使用 `==` 或 `!=` 进行比较，返回文档中注明的失败值，并让函数的其余部分假定对象存在。
在 `int value = *found;` 之后再进行检查毫无意义，因为读取操作已经执行过了。

未找到元素时返回 0 无法与未受保护的读取所产生的 0 区分开来，因此本练习要求返回 -1，并且输入数据中不包含 -1。

### 要求

- `firstValueAtLeast` 接收 `const std::vector<int> &values` 和一个 `int threshold`，并返回一个 `int`。
- 提供的 `firstAtLeast` 返回指向达到阈值的第一个元素的 `const int *`，如果没有元素达到阈值则返回 `nullptr`。
  请保持原样并调用它；系统会检查代码中是否包含代码片段 `firstAtLeast(values`。
- 在通过指针读取任何内容之前，将指针与 `nullptr` 进行比较，并在此时返回 -1。
  请写为 `if (found == nullptr)`，因为系统会检查代码中是否包含代码片段 `nullptr)`。
- 否则返回通过指针读取的值，即元素本身而不是阈值。
- 每个元素都在 1 到 500 之间，因此 1 和 500 是有效答案。
  空 vector 以及高于所有元素的阈值，都会走返回 -1 的路径，而不是被直接拒绝。

### 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    // 已提供。每个元素都在 1 到 500 之间，因此没有元素是 0，也没有元素是 -1。
    // 返回第一个达到 threshold 的元素的地址，没有元素达到时返回 nullptr。保持此函数原样。
    static const int *firstAtLeast(const std::vector<int> &values, int threshold) {
        for (std::size_t i = 0; i < values.size(); i += 1) {
            if (values[i] >= threshold) {
                return &values[i];
            }
        }
        return nullptr;
    }

    static int firstValueAtLeast(const std::vector<int> &values, int threshold) {
        // 先取得地址，指针为空时返回 -1，否则再通过指针读取元素
        const int *found = firstAtLeast(values, threshold);
        if (found == nullptr) {
            return -1;
        }
        return *found;
    }
};
```
