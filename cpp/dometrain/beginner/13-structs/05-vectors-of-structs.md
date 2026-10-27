`std::vector<Item>` 以结构体作为其元素类型，因此一行数据作为一个元素传递。

```cpp
struct Row {
    std::string city;
    int visits;
};

std::vector<Row> rows;
rows.push_back(Row{"oslo", 3});
rows.push_back(Row{"lima", 8});

int total = 0;
for (const Row &row : rows) {
    total = total + row.visits;
}
```

`push_back` 追加一个元素，而 `Row{"oslo", 3}` 在存入之前通过大括号列表构建该元素。
元素 0 现在是一个完整的 Row，它的 city 和 visits 组合在一起，而不是城市在一个 vector 中、计数在另一个 vector 中且仅在无人修改任何一个 vector 时才能对齐。

将基于范围的 for 循环变量声明为 `const Row &row` 可以直接引用已存在于 vector 中的元素。
写成 `Row row` 则会在每次迭代时复制每个元素（包括 string），并且写入该副本的任何内容都不会影响原数据。

`totalForName` 接收 `const std::vector<std::string> &names`、`const std::vector<int> &quantities` 和 `const std::string &wanted`。
它返回一个 int，由以下五条规则决定其返回值：

- 长度相等才能构成一行数据，因此大小不同则返回 -1，并且在对任何一个 vector 建立索引之前就做出裁决。
- 输入中任何位置的计数小于 0 也返回 -1。
- 构建一个 `std::vector<Item>` 并使用 `push_back` 进行填充，每行一个元素。
  该元素类型和调用都是必需的。
- 累加名称等于 `wanted` 的每个元素的数量，在遍历它们时将每个元素命名为 `const Item &`。
  两个行包含相同名称时，两处的计数都要计入。
- 未与任何行匹配的名称返回 0，一对不包含任何内容的 vector 同样返回 0，因为空的总和是 0 而不是拒绝处理。

名称可能重复且可能为空字符串，并且每个被接受的计数都大于或等于 0。
这就是为什么在此可以使用 -1 作为拒绝标志：任何进入累加步骤的总和都不会为负数。

## 解答

```cpp
#include <cstddef>
#include <string>
#include <vector>

struct Item {
    std::string name;
    int quantity;
};

struct Solution {
    static int totalForName(const std::vector<std::string> &names, const std::vector<int> &quantities, const std::string &wanted) {
        // 长度不同返回 -1，用 push_back 把两个 vector 配对成 std::vector<Item>，再累加名称匹配的行
        if (names.size() != quantities.size()) {
            return -1;
        }
        std::vector<Item> items;
        for (std::size_t i = 0; i < names.size(); ++i) {
            if (quantities[i] < 0) {
                return -1;
            }
            items.push_back(Item{names[i], quantities[i]});
        }
        int total = 0;
        for (const Item &item : items) {
            if (item.name == wanted) {
                total += item.quantity;
            }
        }
        return total;
    }
};
```
