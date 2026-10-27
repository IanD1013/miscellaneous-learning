使用 `a < b` 比较两个字符串，你会得到按字母顺序排列的结果：`{"apple", "zip", "blueberry"}` 排序后变为 `{"apple", "blueberry", "zip"}`，其中最短的字符串排在最后。
比较操作接收这两个元素，但并没有强制要求比较元素本身。
它可以比较从这些元素中计算出的任何值：

```cpp
#include <algorithm>
#include <string>
#include <vector>

std::vector<std::string> v = {"apple", "zip", "blueberry"};
std::sort(v.begin(), v.end(), [](const std::string &a, const std::string &b) {
    return a.size() < b.size();
});
```

`v` 现在包含 `{"zip", "apple", "blueberry"}`。
`a.size()` 和 `b.size()` 是构建排序依据的计算值：它们在每次调用时重新计算且不存储在任何地方，而实际移动的是字符串本身。
这两个参数都通过 const 引用传递，这是函数在不需要拥有自身副本时读取字符串的常规方式。

构建第二个长度向量并对其进行排序，只会对数字进行排序而将字符串留在原处，这就是为什么计算逻辑应该放在比较操作内部，而不是放在其旁边。

空字符串不需要单独处理。
它的 `size()` 是 0，小于任何其他长度，因此它会像其他最短字符串一样排在最前面。

- `sortedByLength` 接收 `const std::vector<std::string> &words` 并返回一个包含相同字符串的 `std::vector<std::string>`，按最短的在前排序。
  对起始代码创建的副本进行排序并将其返回。
- `{"banana", "fig", "watermelon", "kiwi"}` 返回为 `{"fig", "kiwi", "banana", "watermelon"}`，而 `{"yes!", "", "three", "no"}` 则以空字符串开头：`{"", "no", "yes!", "three"}`。
- 每个评分用例中的字符串长度各不相同，因此这一条规则就决定了整个顺序。
- 由 `std::sort` 执行排序，并通过 lambda 提供比较规则，因此必须出现 `[]`；不需要 `main` 函数，因为外围程序已完整提供。

## 解答

```cpp
#include <algorithm>
#include <string>
#include <vector>

struct Solution {
    static std::vector<std::string> sortedByLength(const std::vector<std::string> &words) {
        // 按字符串长度从短到长排序这份副本
        std::vector<std::string> result = words;
        std::sort(result.begin(), result.end(), [](const std::string &a, const std::string &b) {
            return a.size() < b.size();
        });
        return result;
    }
};
```
