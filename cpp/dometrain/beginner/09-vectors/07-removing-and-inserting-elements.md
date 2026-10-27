vector 中的位置（position）与索引（index）是不同的概念，而 `erase` 和 `insert` 所需要的正是位置。
`v.begin()` 表示第一个元素的位置，`v.end()` 表示最后一个元素之后的一个位置（该位置不对应任何元素），而 `v.begin() + i` 则表示元素 `i` 的位置。
这样的值本身有一个专属名称，叫做迭代器（iterator），在这里它仅用于指定应当在哪里进行修改。

```cpp
#include <cstddef>
#include <vector>

std::vector<int> v = {10, 20, 30, 40};
std::size_t i = 1;

v.erase(v.begin() + i);
v.insert(v.begin(), 99);
```

`erase` 会移除给定位置的元素，并将该位置之后的所有元素向左移动一位以填补空隙，因此 `v` 变为 `{10, 30, 40}` 且 `size()` 减一。
该位置必须是 vector 中实际存在的位置，这与用于保护下标访问的 `size()` 比较规则是一致的。
`insert` 会将其第二个参数放置在给定的位置上，并将从该位置开始的所有元素向右移动一位，因此 `v` 变为 `{99, 10, 30, 40}` 且 `size()` 加一。
在 `v.begin()` 处插入，新值会排在最前面；在 `v.end()` 处插入，新值会排在最后面，这正是 `push_back` 所做的工作。

删除和插入操作会使调用前获取的所有位置失效，因为保存的位置所指向的元素已经发生了移动。
在每次修改之后，应当基于 `begin()` 重新构建位置，而不是跨修改保留旧位置。
索引也面临同样的风险：在 `i` 处执行删除后，原来位于空隙之后的元素现在直接来到了 `i` 处，因此如果在该轮遍历中递增索引，就会跳过一个从未检查过的元素。
在执行了删除操作的一轮中，索引应保持不变；只有在未删除任何元素的一轮中，才递增索引。
在运行过程中，没有任何机制会主动提示位置已失效，因此遵守该规则完全取决于你。

`collapseOccurrences` 接收 `const std::vector<int> &values` 和一个 `int target`，并返回一个 `std::vector<int>`。
由于参数是 `const`，初始代码会将其复制到 `result` 中，你所做的所有修改都针对该副本。
代码中必须出现 `.erase(`，且禁止使用 `push_back`。
删除所有等于 `target` 的元素；如果至少删除了一个元素，则在 `result.begin()` 处插入一个单独的 `target`，使其排在最前面，其余保留的元素按原来的顺序排在其后。
如果 vector 从未包含过 `target`，则原样返回；如果是空 vector，则返回一个空 vector。

## 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    static std::vector<int> collapseOccurrences(const std::vector<int> &values, int target) {
        std::vector<int> result = values;
        // 从 result 中删除所有 target，若删除过则在最前面放回一个
        bool removed = false;
        std::size_t i = 0;
        while (i < result.size()) {
            if (result[i] == target) {
                result.erase(result.begin() + i);
                removed = true;
            } else {
                i += 1;
            }
        }
        if (removed) {
            result.insert(result.begin(), target);
        }
        return result;
    }
};
```
