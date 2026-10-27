vector 中的每个元素都可以通过计数器来访问。
关键微妙之处在于中间的子句，即决定计数器何时超出范围的那个子句。

```cpp
#include <cstddef>
#include <iostream>
#include <vector>

std::vector<int> v = {3, 1, 4};
for (std::size_t i = 0; i < v.size(); ++i) {
    std::cout << v[i] << " ";
}
```

计数器从 0 开始，即第一个元素。
一旦达到元素总数它就会停止，因此最后一次循环执行时计数器比 `size()` 小 1，指向最后一个元素。
在这两者之间，循环体按顺序恰好访问每个元素一次，该循环将打印出 `3 1 4 `。

`std::size_t` 是 `size()` 返回的类型，是一个绝不为负的无符号计数值，因此这样声明计数器可以保持比较两边的数字类型一致。
该类型名称来自 `<cstddef>`，初始代码已为你将其与 `<vector>` 一同包含。
使用 `int` 类型的计数器也可以编译并运行；它会产生有符号与无符号比较的警告，而这里的警告绝不会导致运行失败。

如果用 `<=` 代替 `<`，循环就会多执行一次，从而读取 vector 中不存在的位置。
在 vector 包含元素的情况下，引擎不会因此停止，而是会返回一个数值，因此在代码读取 vector 外部内容时，总和可能看起来依然合情合理。
但在不包含任何元素的情况下，第一次循环就会读取空 vector 的位置 0，而第 9.2 课已经说明了会发生什么：程序会戛然而止，完全没有返回任何结果。
与 `size()` 进行 `<` 比较，是确保循环体使用的每个索引都确实属于该 vector 的唯一保证。

元素总和作为 `int` 从 `totalOf` 返回，而 `const std::vector<int> &values` 是唯一的输入参数。
请在循环上方声明累加总和变量。
如果在循环体内部声明，它在右花括号处就会超出作用域，导致 `return total;` 找不到该变量名而无法编译文件。
如果将本应写 `total += values[i]` 的地方误写成 `total = values[i]`，则最终只会保留最后一个元素的值。
你的循环条件应与 `values.size()` 进行比较，循环体中读取 `values[i]`。
不包含任何元素的 vector 无需编写额外处理代码，总和就会是 0，因为在第一次测试条件时结果就已经是 false 了。

## 解答

```cpp
#include <cstddef>
#include <vector>

struct Solution {
    static int totalOf(const std::vector<int> &values) {
        // 在循环之前声明累加总和，再把每个元素加进去
        int total = 0;
        for (std::size_t i = 0; i < values.size(); i += 1) {
            total += values[i];
        }
        return total;
    }
};
```
