`std::find` 报告第一个匹配元素所在的位置，而 `std::count` 报告有多少个元素匹配：

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v = {3, 8, 3};
auto found = std::find(v.begin(), v.end(), 8);
bool present = found != v.end();
int howMany = static_cast<int>(std::count(v.begin(), v.end(), 3));
```

在这里 `present` 为 `true` 且 `howMany` 为 2。
两次调用遍历相同的左闭右开区间，并且都不关心元素的排列顺序。

`std::find` 返回的是一个位置，既不是值也不是索引。
它是等于目标值的第一个元素的位置，当没有元素等于目标值时，它返回 `end()`。
由于 `end()` 位于最后一个元素的后一位，它不指向任何元素，这使得它可以作为未找到任何内容的答案：`found != v.end()` 表示存在匹配项，`found == v.end()` 表示不存在匹配项。
因此，该位置只用于比较而绝不会被解引用读取。
`end()` 不指向任何元素，语言也没有定义读取它的行为，所以本课程中没有任何内容会这样做。
在字符串上将 `find` 与 `std::string::npos` 进行比较也是同样的机制，只不过是用一个保留数字代替了位置；而在第 10.3 课中手写的搜索也是同样的机制，只是层级更低一些。

`std::count` 会一直遍历到区间末尾，并返回一个数字：有多少个元素等于目标值。
在这里，零是一个有效的答案，表示没有匹配的元素，而不是出错的标志。
它以标准库自有的计数类型返回，而不是 `int`，因此在调用周围加上 `static_cast<int>` 是为了将该数字放入 `int` 类型的 vector 中。

空 vector 在进行任一调用前都不需要做保护检查，因为在空 vector 中 `begin()` 等于 `end()`：搜索会立即停止并表示未找到，而计数结果会返回 0。

- `presenceAndCount` 接收 `const std::vector<int> &values` 和一个 `int target`，并返回一个恰好包含两个元素的 `std::vector<int>`。
- 当目标值在 `values` 中时，第 0 个元素为 1；不在时为 0。
  通过将 `std::find` 返回的结果与 `values.end()` 进行比较来决定。
- 第 1 个元素是目标值出现的次数，即 `std::count` 返回的数字。
- 当输入为 `{3, 1, 3, 6, 3}` 且目标值为 3 时返回 `{1, 3}`；当输入为 `{2, 4, 6}` 且目标值为 0 时返回 `{0, 0}`；无论目标值是什么，空 vector 均返回 `{0, 0}`。
- 你的解答中必须同时出现 `std::find` 和 `std::count`。

## 解答

```cpp
#include <algorithm>
#include <vector>

struct Solution {
    static std::vector<int> presenceAndCount(const std::vector<int> &values, int target) {
        // 第 0 个元素表示是否找到目标值，第 1 个元素是它出现的次数
        std::vector<int> report;
        if (std::find(values.begin(), values.end(), target) != values.end()) {
            report.push_back(1);
        } else {
            report.push_back(0);
        }
        report.push_back(static_cast<int>(std::count(values.begin(), values.end(), target)));
        return report;
    }
};
```
