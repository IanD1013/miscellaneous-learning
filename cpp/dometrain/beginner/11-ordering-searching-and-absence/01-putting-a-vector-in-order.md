对 vector 进行排序只需要一次调用，其第三个参数决定了排序的方向：

```cpp
#include <algorithm>
#include <functional>
#include <vector>

std::vector<int> v = {4, 1, 9};
std::sort(v.begin(), v.end(), std::greater<int>());
```

之后 `v` 的内容为 `{9, 4, 1}`。
`std::sort` 会就地重新排列元素且不返回任何内容，因此不需要接收新的 vector：在调用中指定的那个 vector 本身就已经被排序了。

前两个参数指明了要处理哪些元素。
`begin()` 是第一个元素的位置，而 `end()` 是最后一个元素之后的位置，因此它们共同标记了一个左闭右开区间，涵盖从第一个元素开始、直到但不包括 `end()` 所指位置的所有元素。
`end()` 本身并不指代任何元素。
如果在此处写 `end() - 1`，则最后一个元素将被排除在排序之外，静静地保持原来的位置。
在空 vector 上，`begin()` 已经等于 `end()`，该区间不包含任何元素，调用无需执行任何操作。

第三个参数是一个用于判断两个元素关系的对象：第一个元素是否应该排在第二个元素之前？当第一个元素较小时，`std::less<int>()` 会返回 true，从而实现从小到大的排序；当第一个元素较大时，`std::greater<int>()` 会返回 true，从而实现从大到小的排序。
这两个名称来自 `#include <functional>`，而 `std::sort` 来自 `#include <algorithm>`；起始代码中已包含这两行。
末尾的圆括号用于构造该对象；如果漏掉它们，你传递的将是一个类型名称而不是比较对象，文件将无法通过编译。

在通常的 C++ 中可以省略该参数，但当前引擎在链接数字 vector 时无法直接省略它：构建会因 `undefined symbol '__lttf2'` 中止，这是关于底层库的提示，而不是你的代码有问题。
请每次都显式传入一个比较对象。

- `sortedValues` 接受 `const std::vector<int> &values` 和一个 `bool smallestFirst`，并返回一个 `std::vector<int>`。
- const 参数无法直接就地重排，这就是为什么起始代码将其拷贝到 `result` 中：对 `result` 进行排序，并返回 `result`。
- `true` 要求从小到大排序，`false` 要求从大到小排序，因此对于 `{4, -2, 9, 1}`，一种情况返回 `{-2, 1, 4, 9}`，另一种情况返回 `{9, 4, 1, -2}`。
- 重复值会被保留，单个元素直接返回自身，空 vector 返回空，因为不包含任何元素的区间无需重排。
- 你的答案中必须出现 `std::sort`；`[]` 和 `main` 均被禁用。

## 解答

```cpp
#include <algorithm>
#include <functional>
#include <vector>

struct Solution {
    static std::vector<int> sortedValues(const std::vector<int> &values, bool smallestFirst) {
        // 先复制一份，再按标志选择的比较对象排序
        std::vector<int> result = values;
        if (smallestFirst) {
            std::sort(result.begin(), result.end(), std::less<int>());
        } else {
            std::sort(result.begin(), result.end(), std::greater<int>());
        }
        return result;
    }
};
```
