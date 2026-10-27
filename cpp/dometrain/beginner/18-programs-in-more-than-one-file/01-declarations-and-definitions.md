声明向编译器提供函数的返回类型、函数名以及参数类型，并在原本是函数体的位置放置一个分号：

```cpp
int helper(int n);
```

该行没有定义任何内容。
它表明 `helper` 存在，调用时传入一个 `int` 并返回一个 `int`，且函数体位于其他位置。
文件是从上到下读取的，编译器会拒绝它未见过的任何名称，因此在代码上方放置声明可以在看不到函数体的情况下使调用成功编译。
参数名 `n` 是可选的，仅供阅读代码的人参考。
声明通过返回类型和参数类型与函数体相匹配，无论该函数体采用何种布局，而代替函数体的分号是两者之间的唯一区别。

名称可以根据需要声明任意多次，也可以在任意多个文件中声明，只要整个程序中的函数体恰好对应一个定义即可。
常规构建会单独编译每个 `.cpp` 文件，因此一个文件永远看不到另一个文件的文本，随后链接器会将每次调用与定义它的唯一定义体进行匹配。
这就是为什么声明就足够了。
而本运行环境则是按顺序将项目的 `.cpp` 文件拼接在一起，因此这里的顺序很重要（在实际构建中则不会），并且已有函数体的第二份副本会导致该名称具有两个定义，从而报错为重复定义（redefinition）。

`helpers.cpp` 无法编辑，并且会被拼接在你的文件之后。
它提供了 `tripleOf`（返回所传入 `int` 的三倍）以及 `isNegative`（对于小于零的 `int` 返回 `true`）。
这两个名称都不会自动出现在你的文件中。

请将这两个声明放在 `struct Solution` 上方，即 `int tripleOf(int value);` 和 `bool isNegative(int value);`。
在运行前会检查开头的 `int tripleOf` 和 `bool isNegative` 声明，同时也会检查形式为 `isNegative(value)` 和 `tripleOf(value)` 的两次调用，因此请将循环变量命名为 `value`。
然后完成 `sumOfTriples` 函数，该函数接收 `const std::vector<int> &values` 并返回一个 `int`：遍历该 vector，跳过 `isNegative` 报告为负的每个值，并将其余值的 `tripleOf(value)` 累加到总和中。
`{2, 5, 1}` 的总和为 24。
空 vector 的总和为 0，全为负数的 vector 总和也为 0；而 0 不是负数，因此它会传给 `tripleOf` 且不会增加总和。

## 解答

```cpp
#include <vector>

// 声明定义在 helpers.cpp 中的两个函数
int tripleOf(int value);
bool isNegative(int value);

struct Solution {
    static int sumOfTriples(const std::vector<int> &values) {
        // 跳过负数，把其余每个值的三倍累加起来
        int total = 0;
        for (int value : values) {
            if (isNegative(value)) {
                continue;
            }
            total += tripleOf(value);
        }
        return total;
    }
};
```
