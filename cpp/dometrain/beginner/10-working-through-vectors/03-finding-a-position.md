如果一个搜索要回答的是“在哪里”而不是“是什么”，它就必须遍历位置。
基于范围的 for 循环只会传递每个元素，却无法说明它来自何处，因此该循环需要对索引进行计数，并且循环体内的 `return` 会在找到第一个匹配项时停止搜索：

```cpp
std::vector<int> v = {5, 9, 5};

for (std::size_t i = 0; i < v.size(); i += 1) {
    if (v[i] == 9) {
        return static_cast<int>(i);
    }
}
return -1;
```

`i` 是正在检查的位置，且仅当 `i < v.size()` 时才会读取 `v[i]`。
在 `if` 内部返回会立即退出函数，因此永远不会访问到后面相同的元素，返回的正是第一个匹配的索引。
`i` 的类型为 `std::size_t`，而函数返回的是 `int`，因此在返回时使用 `static_cast<int>(i)` 进行了转换。

执行到循环外部意味着没有任何元素匹配，而 -1 是为此规定的返回值。
这里使用 -1 不会引起混淆，其原因值得在每次重用该模式时再次确认：该函数返回的是位置，位置从 0 开始，因此任何有效的结果都不可能是负数。
如果一个函数返回的是匹配的元素，则无法做出同样的保证，因为 -1 本身可能就是其中一个元素；那种约定需要第 7.4 课中的 `bool` 结果和引用输出参数。
字符串上的 `find` 也做出了类似的保证，使用的是 `std::string::npos`。

空的 vector 不需要特殊的防范措施。
循环条件在第一次测试时就会判定为假，循环体永远不会执行，程序会按常规路径返回 -1。

`firstIndexOf` 接受 `const std::vector<int> &numbers` 和一个 `int target`，并返回等于 `target` 的第一个元素的 `int` 位置；如果没有元素等于它，则返回 -1。
在每次循环时都要对照 `numbers.size()` 检查索引，且不要使用 `std::find`：自行定位位置才是本练习的任务。

## 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    static int firstIndexOf(const std::vector<int> &numbers, int target) {
        // 返回第一个等于 target 的元素的位置，找不到则返回 -1
        for (std::size_t i = 0; i < numbers.size(); i += 1) {
            if (numbers[i] == target) {
                return static_cast<int>(i);
            }
        }
        return -1;
    }
};
```
