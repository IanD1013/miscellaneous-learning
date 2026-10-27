将最大值的初始值设为 0，直到遇到所有元素均为负数的 vector 时就会出错。
`{-9, -4, -7}` 中没有任何元素能超过当前最优值 0，因此函数会返回 0，而这个数字根本不是其中的任何一个元素。
相反，应该从一个必定属于其中的值开始初始化：即第一个元素。

```cpp
std::vector<int> v = {6, 2, 11, 2};

int best = v[0];
for (int value : v) {
    if (value > best) {
        best = value;
    }
}
```

`best` 是目前见到的最大值。
它初始为 `v[0]`，这已经是 vector 中的一个元素了，之后任何更大的元素都会取代它的位置，在这里最终留下 11。
在第一次遍历时将第一个元素与自身进行比较不会产生额外开销，也不会改变任何结果，因为求最大值不是累加操作，遇到同一个元素两次并不会使其虚增。

但当 vector 为空时，这种初始化方式就会失效。
因为没有第一个元素可供读取，而在没有元素的情况下读取 `v[0]` 会导致程序异常终止，而不是返回一个数字。
因此，判空检查必须放在初始化之前，而不是之后。

空 vector 没有最大元素，而且没有哪个 `int` 值能代表这种“缺失”：0、-1 和 -1000 都是 vector 允许包含的合法值。
因此，这个默认值由调用者提供。
`largestValueOr` 接收第二个参数 `absent`，并在无可比较的内容时将其原样返回。
任何 `int` 都无法避免潜在的值冲突，所以只有已经了解自身数据覆盖范围的调用者才能识别 `absent` 值。
如果调用者不清楚范围，那么在第 7.4 课中构建的配对方法才是函数应该提供的替代方案：在调用者持有的变量旁附带一个 `bool`。
评分测试用例会传入两个不同的 absent 值。

### 要求

- `largestValueOr(const std::vector<int> &numbers, int absent)` 返回一个 `int`。
- 当存在元素时，返回最大值，包括所有元素均为负数，以及最大值位于首位、末尾或出现两次的情况。
- 如果 vector 的实际最大元素是 0，则返回 0，而不是 `absent`。
- 当没有元素时，原样返回调用者传入的 `absent`。
- 在初始化前会检查 `numbers.empty()`，因此检查逻辑中需要包含 `empty()`。
- 禁止使用标准库的最大值辅助工具：`std::max` 和 `max_element`（无论哪种拼写形式）均已被禁用，你需要自行实现比较逻辑。

### 解答

```cpp
#include <vector>

struct Solution {
    static int largestValueOr(const std::vector<int> &numbers, int absent) {
        // 返回最大元素，没有元素可比较时返回调用者的 absent 值
        if (numbers.empty()) {
            return absent;
        }
        int largest = numbers[0];
        for (int value : numbers) {
            if (value > largest) {
                largest = value;
            }
        }
        return largest;
    }
};
```
