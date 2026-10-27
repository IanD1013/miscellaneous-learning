将 5、1、9 和 3 推入 `std::priority_queue<int>`，`top()` 读取到的是 9，而不是最先进入的 5。
来自 `<queue>` 的队列会将优先级最高的元素保留在顶部，并且默认情况下，较大的 `int` 具有更高的优先级：

```cpp
std::priority_queue<int> heap;
heap.push(5);
heap.push(1);
heap.push(9);
heap.push(3);
int first = heap.top();   // 9
heap.pop();               // 移除 9
int second = heap.top();  // 5
```

与 `std::stack` 类似，`pop()` 不返回任何内容，而 `top()` 需要先进行 `empty()` 检查。
由于没有迭代器，因此 `top()` 是你唯一可以读取的元素。
在这些调用背后是一个排列成堆的 `std::vector`：最前面的元素的优先级至少与任何其他元素一样高，而其余元素只是部分有序。
每次 `push` 和 `pop` 都会移动少量元素来保持这一特性，比起只有在读取顶部时才对整个 vector 排序，这样做的开销要小得多。

### 选择顺序

比较方式是第三个模板参数。
模板参数按位置匹配，因此要指定第三个参数就意味着必须写出第二个参数，即容器类型，默认为 `std::vector<int>`：

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> heap;
```

现在同样的四次 push 会将 1 置于顶部。
如果你曾向 `std::sort` 传递过 `std::greater<int>()`，这看起来可能恰恰相反，因为在 `std::sort` 中它会将 9 排在最前面。
两者对比较的理解方向相反。
`std::sort` 认为 `comp(a, b)` 返回 true 意味着 `a` 排在 `b` 前面。
而队列则认为它意味着 `a` 的优先级低于 `b`，并将没有任何其他元素比其优先级更高的元素保留在顶部。
默认的比较方式 `std::less<int>` 返回 `a < b`，因此较小的值具有较低的优先级，最大的值位于顶部。
`std::greater<int>` 返回 `a > b`，因此较大的值具有较低的优先级，最小的值位于顶部。

尖括号内填入的是比较方式的类型，即不带 `()` 的 `std::greater<int>`。
队列会自行创建比较对象，而 `std::sort` 需要你传入一个对象。
取反每个值也可以让最小值先出队，除非某个值是最小的 `int`，对其取反会导致溢出；`std::greater<int>` 则不会改变值本身。

### 自定义比较规则

只要函数对象的 `operator()` 接受两个元素并返回 `bool`，就可以作为第三个参数。
对于包含等级和名称的 pair：

```cpp
struct LowerPriority {
    bool operator()(const std::pair<int, std::string>& a,
                    const std::pair<int, std::string>& b) const {
        // 当 a 的优先级低于 b 时返回 true
    }
};

std::priority_queue<std::pair<int, std::string>, std::vector<std::pair<int, std::string>>, LowerPriority> heap;
heap.push({3, "a"});
```

推入 `{1, "b"}`、`{3, "a"}` 和 `{3, "c"}`，仅凭比较方式即可决定名称弹出的顺序：

- 按照 `std::sort` 的方式编写 `operator()`，即在 `a` 应该先弹出时返回 true：`["b", "c", "a"]`。
  本应最后弹出的 pair 结果位于顶部，因此每个名称弹出的顺序都与你预期的相反。
- 不传入第三个参数：队列会退回使用 `std::pair` 的 `<`，该运算符先比较等级再比较名称，得到 `["c", "a", "b"]`。
  等级的顺序是正确的，但在相同等级中，排序靠后的名称反而先弹出了。
- 按照队列的方式编写 `operator()`，即在 `a` 的优先级低于 `b` 时返回 true：`["a", "c", "b"]`，这正是 `byUrgency` 必须返回的顺序。

堆不保留到达顺序。
如果 `operator()` 仅比较等级，则具有相同等级的两个 pair 优先级相同，无论你以何种顺序推入它们，`top()` 都有可能先读取其中的任何一个。
只有当 `operator()` 在等级相同时继续比较名称，并依然对优先级较低的 pair 返回 true 时，相同等级的元素才会以固定的顺序弹出。

### 编写内容

在 `priorities.cpp` 中实现 `Solution` 的三个函数：

- `largestK(values, k)` 返回 `k` 个最大的值，最大的排在最前；`smallestK(values, k)` 返回 `k` 个最小的值，最小的排在最前。
  重复的值分别计算，当 `k` 大于值的总数时，按该顺序返回所有值，例如 `largestK({2, 7, 2}, 5)` 返回 `[7, 2, 2]`。
  当 `k` 小于 1 时，返回一个空 vector。
- `byUrgency(names, levels)` 将每个名称与相同索引处的等级配对，并按等级从高到低返回名称，相同等级的按字母顺序排列。
  在 `struct Solution` 上方将其比较规则编写为函数对象（例如 `LowerPriority`）。
  当 `names` 和 `levels` 长度不同时，返回一个空 vector。

使用 `top()` 和 `pop()` 从 `std::priority_queue` 中取出每个值，不得使用 `std::sort`、`std::stable_sort`、`std::partial_sort` 或 `std::nth_element`。

### 解答

```cpp
#include <functional>
#include <queue>
#include <string>
#include <utility>
#include <vector>

struct LowerPriority {
    // a 的优先级低于 b 时返回 true：等级低者优先级低，同等级时名称靠后者优先级低
    bool operator()(const std::pair<int, std::string>& a,
                    const std::pair<int, std::string>& b) const {
        if (a.first != b.first) {
            return a.first < b.first;
        }
        return a.second > b.second;
    }
};

struct Solution {
    static std::vector<int> largestK(const std::vector<int>& values, int k) {
        std::priority_queue<int> heap(values.begin(), values.end());
        return takeTop(heap, k);
    }

    static std::vector<int> smallestK(const std::vector<int>& values, int k) {
        std::priority_queue<int, std::vector<int>, std::greater<int>> heap(values.begin(), values.end());
        return takeTop(heap, k);
    }

    static std::vector<std::string> byUrgency(const std::vector<std::string>& names, const std::vector<int>& levels) {
        if (names.size() != levels.size()) {
            return {};
        }
        std::priority_queue<std::pair<int, std::string>, std::vector<std::pair<int, std::string>>, LowerPriority> heap;
        for (std::size_t i = 0; i < names.size(); ++i) {
            heap.push({levels[i], names[i]});
        }
        std::vector<std::string> result;
        while (!heap.empty()) {
            result.push_back(heap.top().second);
            heap.pop();
        }
        return result;
    }

private:
    // 从堆顶依次取出最多 k 个值
    template <typename Heap>
    static std::vector<int> takeTop(Heap& heap, int k) {
        std::vector<int> result;
        while (static_cast<int>(result.size()) < k && !heap.empty()) {
            result.push_back(heap.top());
            heap.pop();
        }
        return result;
    }
};
```
