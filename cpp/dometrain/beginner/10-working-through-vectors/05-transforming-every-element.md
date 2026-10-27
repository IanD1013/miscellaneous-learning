转换操作（transformation）为每个输入元素生成一个输出元素，因此其循环不包含用于决定写入什么内容的条件判断：

```cpp
std::vector<int> v = {3, 0, -1};

std::vector<int> result;
for (int value : v) {
    result.push_back(value + 10);
}
```

`result` 的输出为 `{13, 10, 9}`。
输入了三个元素，输出了三个元素，且顺序与输入保持一致，因为每次遍历都以 `push_back` 结束。
每个输入对应一个输出，正是这一点保证了结果与输入的大小相同；对于没有任何元素的输入，循环体将执行零次，并生成一个空的结果，无需为此编写任何特殊处理情况。

通常有两种情况会导致大小不一致。
跳过看似无关紧要的元素（例如 0）会导致返回的结果比输入少一个元素。
如果先用输入的大小声明结果然后再追加元素，则会返回两倍数量的元素：那些声明的位置已经被零填充，而 `push_back` 会追加在它们之后。

将循环变量翻倍也不会影响它所来自的 vector。
基于范围的 for 循环会传递每个元素的副本，更何况 `numbers` 本身是一个 `const` 引用。

- `doubleEach` 接收 `const std::vector<int> &numbers` 并返回一个 `std::vector<int>`。
- 结果中的每个元素都是 `numbers` 对应位置元素的两倍，负数、零和重复值的处理方式完全相同。
- 结果包含与 `numbers` 相同数量的元素，若输入没有元素则结果也没有。
- 使用 `push_back` 构建结果，不要使用 `transform`（无论是否带有 `std::` 前缀）；本题考察的是一进一出的循环结构。

## 解答

```cpp
#include <vector>

struct Solution {
    static std::vector<int> doubleEach(const std::vector<int> &numbers) {
        std::vector<int> result;
        // 用 push_back 逐个追加，使 result 与 numbers 的元素数量相同
        for (int value : numbers) {
            result.push_back(value * 2);
        }
        return result;
    }
};
```
