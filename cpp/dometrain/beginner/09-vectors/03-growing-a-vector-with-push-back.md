声明 `std::vector<int> squares;` 就此结束，会得到一个尚不包含任何元素的 vector，每当元素需要在程序运行时计算得出时，这正是你所需要的：

```cpp
std::vector<int> squares;   // size() 为 0
squares.push_back(1);
squares.push_back(4);       // squares 现在依次保存 1 和 4
```

没有大括号列表，括号中也没有数字：声明给出了元素类型和变量名后就结束了。
`size()` 为 0，并且 vector 已经构建完毕且完全可用，而不是半成品。
使用圆括号会将其变成其他东西，因为 `std::vector<int> squares(4);` 会请求 4 个元素并将它们填充为 0，导致之后添加的任何内容都会排在这 4 个元素之后。

`push_back` 接收要添加的值并将其作为一个元素放到末尾，使 `size()` 增加 1。
vector 中原有的内容保持在原位，无需预先腾出空间，调用中也不包含任何位置参数：`squares.push_back(4)` 指定了要添加什么，而无需指定放在哪里。

`multiplesOf` 接收两个 `int` 参数：`step` 和 `count`，并返回一个包含 `step * 1`、`step * 2` 直至 `step * count` 的 `std::vector<int>`，顺序与乘数递增的顺序一致。
声明不带大括号列表和圆括号数字的 `std::vector<int> result`，让计数器从 1 运行到 `count`（包含 `count`），在每次循环中 push `step * i`，并在计数器结束后返回 `result`。
每个元素都必须通过 `push_back` 调用加入。

### 自带答案的参数

`count` 为 0 时会在第一次检查时使循环条件为 false，因此不会 push 任何内容，返回的结果也不包含任何元素。
负数 `count` 的效果完全相同，这就是为什么两者都不需要为此专门编写守卫条件（guard）。
`step` 为 0 时每次循环都会 push 0，因此 count 为 3 时返回三个 0。
负数 step 会产生负倍数：-4 且 count 为 3 时返回 -4、-8、-12。

### 解答

```cpp
#include <vector>

struct Solution {
    static std::vector<int> multiplesOf(int step, int count) {
        // 从一个没有元素的 vector 开始，每次添加一个倍数
        std::vector<int> result;
        for (int i = 1; i <= count; ++i) {
            result.push_back(step * i);
        }
        return result;
    }
};
```
