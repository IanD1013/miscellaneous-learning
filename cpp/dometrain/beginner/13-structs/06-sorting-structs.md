对结构体（struct）的 vector 进行排序会移动整个元素，而你传入的比较逻辑决定了它们最终的排列顺序：

```cpp
struct Item {
    std::string name;
    int quantity;
};

std::vector<Item> rows;

std::sort(rows.begin(), rows.end(), [](const Item &a, const Item &b) {
    return a.quantity < b.quantity;
});
```

`rows.begin()` 和 `rows.end()` 标记了范围。
第三个参数是一个 lambda 表达式，直接写在使用它的地方：方括号，接着是一个以常量引用方式接收该 vector 中两个元素的参数列表，然后是一个在 `a` 必须排在 `b` 之前时返回 true 的函数体。
读取 `a.quantity < b.quantity` 会将最小的数量排在最前面；将 `<` 改为 `>` 则会将最大的排在最前面。
排序时比较一个成员，然后移动整个元素，因此该行的所有其他成员都会跟随被比较的成员一起移动。
`Item` 自身不带有任何排序规则，所以规则必须从外部传入。

### 当两行平局时

相等的数量会让比较无从判断，这两个元素的排列顺序是未指定的。
平局时的决胜规则写在同一个 lambda 内部：

```cpp
std::sort(rows.begin(), rows.end(), [](const Item &a, const Item &b) {
    if (a.quantity != b.quantity) {
        return a.quantity < b.quantity;
    }
    return a.name < b.name;
});
```

当数量不同时，第一个判断就可以决定一切。
一旦它们相等，第二个成员将起决定作用，对两个 `std::string` 值使用 `<` 会按字符逐个比较，因此 "ana" 会排在 "bo" 之前。
两个成员都相等的两行在任意方向上比较都会返回 false，这保证了比较的一致性。
分别按每个成员排序两次会丢弃第一次的排序结果，因为 `std::sort` 并不保证保留相等元素的原有相对位置。

### 排名

初始代码构建了 `entries`，并在之后复制出名称。
在这两个步骤之间的排序逻辑以及守卫条件的主体是你需要添加的内容。

- `canRank` 接收这两个 vector 并返回一个 bool：当它们逐行对应时为 true，当行数不同时为 false。
  两个为空的 vector 是对齐对应的，因此它返回 true。
- `rankNames` 返回一个包含名称的 `std::vector<std::string>`。
  它会先调用 `canRank`，在进行任何索引操作之前，如果返回 false 则交回空 vector。
- 按积分对条目进行排序，积分最高的排在最前；积分相同时按名称从 a 到 z 排序。
- 使用一次 `std::sort` 调用和一个 lambda：文件中必须包含 `std::sort`，并且必须包含 `](`，即捕获列表的闭括号紧接着参数列表的开括号。
  禁止使用 `operator<`，因为在类型本身中编写比较逻辑属于后续课程的内容。
- 积分是整数且名称可能会重复，因此返回空结果意味着输入对被拒绝或者两个 vector 均为空。

### 解答

```cpp
#include <algorithm>
#include <cstddef>
#include <string>
#include <vector>

struct Score {
    std::string name;
    int points;
};

struct Solution {
    static bool canRank(const std::vector<std::string> &names, const std::vector<int> &points) {
        // 两个 vector 行数相同才能逐行对应
        return names.size() == points.size();
    }

    static std::vector<std::string> rankNames(const std::vector<std::string> &names, const std::vector<int> &points) {
        std::vector<std::string> ranked;
        if (!canRank(names, points)) {
            return ranked;
        }
        std::vector<Score> entries;
        for (std::size_t i = 0; i < names.size(); ++i) {
            entries.push_back(Score{names[i], points[i]});
        }
        // 用一次 std::sort 和 lambda 排序：积分高的在前，积分相同按名称排序
        std::sort(entries.begin(), entries.end(), [](const Score &a, const Score &b) {
            if (a.points != b.points) {
                return a.points > b.points;
            }
            return a.name < b.name;
        });
        for (const Score &entry : entries) {
            ranked.push_back(entry.name);
        }
        return ranked;
    }
};
```
