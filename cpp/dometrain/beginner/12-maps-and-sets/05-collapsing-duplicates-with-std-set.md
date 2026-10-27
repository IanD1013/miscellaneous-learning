向 `std::set<int>` 中插入两次 4，它仍然只包含一个 4。
成员归属关系是集合唯一解答的问题：它只存储值，没有需要填写的第二部分：

```cpp
#include <set>

std::set<int> seen;
seen.insert(4);
seen.insert(9);
seen.insert(4);   // 已经存在，因此没有任何变化
```

`std::set<int>` 在尖括号中指定元素类型，并将每个不同的值保留一次。
`#include <set>` 引入了该类型，它与 `#include <map>` 各自成行，因此同时使用这两种类型的文件需要包含这两个头文件。
在这三次调用之后，`seen.size()` 为 2。

`insert(value)` 会添加集合中尚未包含的值；若已包含，则什么都不做。
重复插入不是错误，也不需要用条件判断进行保护，这使得在循环内去重只需一行代码。
集合不会记录某个值出现了多少次：在三次插入后，`seen.count(4)` 返回的结果与一次插入后完全一样，都是 1，这与 map 的 `count` 返回 0 或 1 相同。
它没有索引位置，因此 `seen[0]` 无法通过编译。

### 插入前先查询

`newValuesInArrivalOrder(const std::vector<int> &already, const std::vector<int> &values)` 返回一个 `std::vector<int>`：包含 `values` 中尚未出现过的元素，每个元素仅出现一次，并保持它们到达的顺序。
先用 `already` 填充一个 `std::set<int>`，然后遍历 `values`，将集合中尚未包含的每个值添加到结果中，并在继续遍历前将其插入集合中。
务必在插入之前进行 `count(value) == 0` 检查，绝不能在插入之后：一旦执行了插入，每个值就都存在于集合中了。
边遍历边插入可以确保 `values` 中重复出现的值只保留一个元素：第一个副本是全新的，第二个副本则会匹配到第一个副本留下的记录。

空的 `already` 搭配为 `{8, -2, 8, -2, 5}` 的 `values` 会返回 `[8, -2, 5]`。
集合会按升序存储这三个值（-2、5 然后是 8），而答案需要保留到达顺序，因此答案是在遍历过程中构建的，而不是从集合中读取出来的。

容器必须声明为 `std::set<`，且每个值必须通过 `.insert(` 存入。
如何查询集合中是否已包含某个值由你决定，只要在插入之前查询即可。
不会有任何输入被拒绝，也没有失败值：元素为空的结果也是有效的结果。
空的 `values` 会产生空结果，没有任何新元素的 `values` 也会产生空结果。

### 解答

```cpp
#include <set>
#include <vector>

struct Solution {
    static std::vector<int> newValuesInArrivalOrder(const std::vector<int> &already, const std::vector<int> &values) {
        std::vector<int> fresh;
        // 先把已见过的值放进 set，再按到达顺序收集新值，收集后立即插入
        std::set<int> seen;
        for (int value : already) {
            seen.insert(value);
        }
        for (int value : values) {
            if (seen.count(value) == 0) {
                fresh.push_back(value);
                seen.insert(value);
            }
        }
        return fresh;
    }
};
```
