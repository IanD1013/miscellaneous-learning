`std::deque<int>` 可以在两端增长。
`std::vector` 没有 `push_front`：`v.insert(v.begin(), x)` 会将每个元素后移一位来腾出空间，因此从前端填充 vector 随着元素增加开销会越来越大。
deque 将其元素保存在固定大小的块中，并在某端填满时添加一个新块，因此在任一端添加元素都不会移动它已有的元素。
`push_front`、`pop_front`、`push_back` 和 `pop_back` 的耗时均为常数时间，并且 `items[i]` 仍然支持索引访问：

```cpp
std::deque<int> items{5, 6};
items.push_front(4);    // 4 5 6
items.push_back(7);     // 4 5 6 7
items.pop_front();      // 5 6 7
items.pop_back();       // 5 6
int second = items[1];  // 6
```

两种 pop 操作均不返回任何值，并且对空的 deque 执行 pop 会导致未定义行为，因此可能遇到空 deque 的 pop 操作应置于 `if (!items.empty())` 之后。

### 栈和队列

`std::stack` 和 `std::queue` 是容器适配器：它们分别包装了一个容器（除非另行指定，否则默认为 `std::deque`），并且仅允许遵循特定规则的操作。
栈是后进先出：`push` 在顶部添加元素，`top()` 读取最新元素，而 `pop()` 将其移除。
队列是先进先出：`push` 在末尾添加元素，`front()` 读取最旧的元素，而 `pop()` 将其移除。

```cpp
std::stack<int> opened;
opened.push(0);
opened.push(3);
int newest = opened.top();   // 3
opened.pop();                // top() 又变回 0

std::queue<std::pair<int, int>> waiting;
waiting.push({0, 3});
waiting.push({1, 5});
auto [index, remaining] = waiting.front();   // 0 和 3
waiting.pop();
```

`pop()` 不返回任何值，因此你需要先通过 `top()` 或 `front()` 读取该元素。
这里的结构化绑定会拷贝队首的 pair，从而在 `pop()` 之后 `index` 和 `remaining` 依然有效；若使用 `auto&` 则会将它们绑定到被 `pop()` 销毁的元素上。
`top()` 和 `front()` 都不会报告适配器是否为空，也不会提供默认值：在空的适配器上调用它们或者执行 pop 都会导致未定义行为。
在每次读取和每次 pop 之前，务必检查 `empty()`。

### 这三个函数

这三个函数均为 `adaptors.cpp` 中 `Solution` 类的静态成员，各自基于为其指定的容器构建。

- `firstUnmatched(text)` 使用保存左括号索引的 `std::stack<int>` 来检查括号 `()`、`[]` 和 `{}`，并跳过所有其他字符。
  遇到的第一个没有对应左括号、或者其栈顶左括号类型不同的右括号时，扫描结束，`firstUnmatched` 返回该右括号的索引。
  每个左括号都有闭合并不够：在 `"([)]"` 中，索引 2 处的 `)` 遇到栈顶的 `[`，因此返回 2。
  如果扫描到达末尾，返回仍然未闭合的最早左括号的索引；若全部闭合，则返回 -1。
  最早的左括号位于栈底，而 `top()` 仅显示最新的左括号。
- `roundRobin(work, slice)` 通过包含 (索引, 剩余单位数) 的 `std::queue<std::pair<int, int>>` 按轮次调度 `work` 中的各项。
  每轮调度队首的项，并最多处理其 `slice` 个单位的工作量；仍有剩余工作量的项会被放回队尾，而工作量为 0 的项在其第一轮即告完成。
  该函数按各项完成的先后顺序返回其索引，因此 `roundRobin({2, 5, 1}, 2)` 返回 `{0, 2, 1}`：在第一轮之后，索引 1 仍剩余 3 个单位的工作量，因此它排在索引 2 之后等待。
  在运行代码之前，先推导一下 `roundRobin({3, 1, 0, 1000}, 1)` 会返回什么。

  如果使用 `std::stack` 进行同样的轮次调度，结果将是 `{2, 1, 0}`。
  索引 2 最后被压入因而最先出来；索引 1 在每轮后被压回，再次位于栈顶，并在索引 0 获得调度之前完成了全部三轮。

  若 slice 小于或等于 0，则返回 `{-1}`：此时每轮都不会消耗任何工作量，因此大于 0 的项永远无法完成。
- `applyEnds(ops, values)` 从空的 `std::deque<int>` 开始，对每个 `i` 执行 `ops[i]` 和 `values[i]`。
  `"push_front"` 和 `"push_back"` 会在对应的一端添加 `values[i]`。
  `"pop_front"` 和 `"pop_back"` 会从对应的一端移除元素并忽略对应的值，若 deque 为空则什么都不做。
  该函数从前到后返回内容。
  任何其他操作名称均返回 `{-1}`，由于所有推入的值都大于或等于 0，这永远不可能是真实的内容。

### 解答

```cpp
#include <algorithm>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <utility>
#include <vector>

struct Solution {
    static int firstUnmatched(const std::string& text) {
        std::stack<int> opened;  // 左括号的索引
        for (int i = 0; i < static_cast<int>(text.size()); ++i) {
            char c = text[i];
            if (c == '(' || c == '[' || c == '{') {
                opened.push(i);
            } else if (c == ')' || c == ']' || c == '}') {
                char expected = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (opened.empty() || text[opened.top()] != expected) {
                    return i;
                }
                opened.pop();
            }
        }
        // 最早的未闭合左括号在栈底
        int earliest = -1;
        while (!opened.empty()) {
            earliest = opened.top();
            opened.pop();
        }
        return earliest;
    }

    static std::vector<int> roundRobin(const std::vector<int>& work, int slice) {
        if (slice <= 0) {
            return {-1};
        }
        std::queue<std::pair<int, int>> waiting;
        for (int i = 0; i < static_cast<int>(work.size()); ++i) {
            waiting.push({i, work[i]});
        }
        std::vector<int> finished;
        while (!waiting.empty()) {
            auto [index, remaining] = waiting.front();
            waiting.pop();
            remaining -= std::min(remaining, slice);
            if (remaining > 0) {
                waiting.push({index, remaining});
            } else {
                finished.push_back(index);
            }
        }
        return finished;
    }

    static std::vector<int> applyEnds(const std::vector<std::string>& ops, const std::vector<int>& values) {
        std::deque<int> items;
        for (std::size_t i = 0; i < ops.size(); ++i) {
            const std::string& op = ops[i];
            if (op == "push_front") {
                items.push_front(values[i]);
            } else if (op == "push_back") {
                items.push_back(values[i]);
            } else if (op == "pop_front") {
                if (!items.empty()) {
                    items.pop_front();
                }
            } else if (op == "pop_back") {
                if (!items.empty()) {
                    items.pop_back();
                }
            } else {
                return {-1};
            }
        }
        return std::vector<int>(items.begin(), items.end());
    }
};
```
