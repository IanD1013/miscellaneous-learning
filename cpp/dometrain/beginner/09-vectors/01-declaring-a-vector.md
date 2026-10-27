vector 保存一系列共享相同类型的值，该类型写在声明的尖括号内：

```cpp
#include <vector>

std::vector<int> scores = {1, 2, 3};
```

`std::vector<int>` 指定了类型，而 `scores` 是正在声明的变量。
元素类型位于尖括号内，因此该 vector 的每个元素都是 `int`，声明一经确定便不可更改。
元素属于 vector 本身，vector 还会记录自身包含多少个元素。

`std::vector` 在 `<vector>` 头文件中声明，因此文件顶部需要在现有的 include 旁边添加 `#include <vector>`。
如果遗漏了该行，编译器遇到从未见过的类型就会停止编译，就像 `std::string` 必须依赖 `<string>` 一样。

`= {1, 2, 3}` 部分是一个大括号列表（braced list）。
它按顺序提供初始元素：先是 1，然后是 2，接着是 3。
内部没有任何内容的大括号不会提供任何元素，而不包含任何元素的 vector 是一个普通的 vector，并非损坏的 vector。

`scores.size()` 会查询 vector 当前包含多少个元素并直接返回该计数，因此 `scores` 返回 3，而空 vector 返回 0。

`elementCounts` 接收一个 `const std::vector<int> &values` 并返回一个包含两个数字的 `std::vector<int>`：首先是 `values` 的元素数量，然后是你自己声明的 vector 的元素数量。
使用包含三个数字的大括号列表声明该 vector 为 `std::vector<int> baseline`，任意三个数字均可，因为这里只关心元素数量。
传入四个数字返回 `[4, 3]`，单个数字返回 `[1, 3]`，空 vector 返回 `[0, 3]`。
向每个 vector 查询其自身的计数，因此答案中应同时出现 `values.size()` 和 `baseline.size()`，而不是直接在答案中硬编码输入 3。
计数并不是 `int` 类型，而大括号列表不允许窄化转换（narrowing），因此每一项都应写为 `static_cast<int>(values.size())`。
评分程序会逐个元素比对返回的 vector，输出到控制台的任何内容均不计分。

## 解答

```cpp
#include <vector>

struct Solution {
    static std::vector<int> elementCounts(const std::vector<int> &values) {
        // 声明一个包含三个元素的基准 vector，然后先返回传入的计数，再返回基准的计数
        std::vector<int> baseline = {1, 2, 3};
        return {static_cast<int>(values.size()), static_cast<int>(baseline.size())};
    }
};
```
