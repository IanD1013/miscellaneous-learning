vector 名称后面的方括号用于选取单个元素，且索引位置从 0 开始：

```cpp
std::vector<int> v = {10, 20, 30};

int first = v[0];
int last = v[v.size() - 1];
```

`v[0]` 是第一个元素，即 10。
因为计数从 0 开始，所以最后一个元素的位置比总数少 1：这里的 `size()` 返回 3，因此 `v[v.size() - 1]` 读取位置 2 并获取到 30。
方括号根本不会进行任何检查。
它们只会读取传入的位置，这就需要由周围的代码来确保该位置确实存在。

如果弄错了这一点，在这个引擎上会出现两种截然不同的表现。
对包含元素的 vector 进行越界读取会返回一个数字（通常是 0），并且没有任何报错提示。
而对一个空 vector 读取 `v[0]` 则是另一种情况：测试用例会直接因退出代码 134 中断，没有任何解释，而对同一个空 vector 读取更大的位置仍然会返回 0。
使用 `.at()` 也无济于事，因为越界的 `.at()` 会以同样突兀的方式终止测试用例，让你的函数根本无法处理。

因此，必须先进行验证，然后再使用方括号：

```cpp
if (!v.empty()) {
    int last = v[v.size() - 1];
}
```

对于不含任何元素的 vector，`empty()` 会返回 `true`，只要含有元素就会返回 `false`。
跳过这一检查还会导致减法出错，因为计数永远不会是负数：在空 vector 上执行 `size() - 1` 得到的不是 -1，而是一个远远超出 vector 实际大小的位置。

### 要求

- `firstAndLast` 接收一个 `const std::vector<int> &values` 并返回一个 `std::vector<int>`，评测系统会对返回值进行逐元素比较。
- 当存在元素时，恰好返回其中的两个元素：先是 `values[0]`，然后是 `values[values.size() - 1]`。
- 对于只包含一个元素的 vector，返回包含该元素两次的结果，因为两端都是同一个元素。
- 给定一个空 vector 时，返回一个空 vector：`return {};`。
- 判空检查应放在两次读取操作之前，而不是与它们并列。
- `.front()` 和 `.back()` 已被禁用，因此最后一个位置需要你根据元素数量计算得出。

### 解答

```cpp
#include <vector>

struct Solution {
    static std::vector<int> firstAndLast(const std::vector<int> &values) {
        // 返回第一个和最后一个元素，没有元素时返回空 vector
        if (values.empty()) {
            return {};
        }
        return {values[0], values[values.size() - 1]};
    }
};
```
