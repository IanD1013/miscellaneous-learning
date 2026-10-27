当现成的比较对象无法满足你所需要的规则时，你可以自己将其编写为一个 lambda 表达式，即一个在需要它的地方定义的函数：

```cpp
#include <algorithm>
#include <vector>

auto comesBefore = [](int a, int b) {
    return a < b;
};
```

方括号是捕获列表；将其留空表示该函数不使用周围代码中的任何内容。
`(int a, int b)` 是它的参数列表：即需要进行比较的两个值。
大括号内是函数体，用于返回结果。
`auto` 为整个表达式赋予了一个名称，并且由于该行定义了一个变量，因此它以分号结尾。
该名称有两种使用方式：`comesBefore(3, 4)` 直接调用它，而 `std::sort(result.begin(), result.end(), comesBefore)` 则将相同的规则传递给排序算法。

这里的规则是奇数在前，偶数在后，且每组内部按从小到大排序。
当 `value % 2 != 0` 时，该值为奇数。
如果测试 `value % 2 == 1`，则会遗漏所有负奇数，因为余数会保留左操作数的符号：`-3 % 2` 的结果是 `-1`，绝不是 1。

### 比较操作的约定

`std::sort` 要求严格弱序（strict comparison）。
它仅在第一个值应该排在第二个值之前时返回 `true`，否则返回 `false`：即当第二个值应排在前面，或者两个值相等时。
如果写成 `a <= b`，你就声明了一个值应该排在与之相等的值（包括它自身）之前，这不是一个任何算法能够据此工作的有效顺序。
如果向排序算法提供该规则，它返回的排列将没有任何保证，即使结果看起来可能完全有序，排序后的结果也不能作为规则是否正确的依据。
`<` 和 `<=` 仅在一对相等的值上存在分歧，这就是为什么第二个评分函数会直接向比较本身提出该问题。

将 lambda 存储一次，放在 `struct Solution` 上方初始代码注释所在的位置，并在两个函数中都使用它。

- `oddsBeforeEvens` 接受 `const std::vector<int> &values` 并返回一个 `std::vector<int>`：即按照规则重新排序后的相同值。
  `{4, 7, 2, 9, 6, 1}` 的结果为 `{1, 7, 9, 2, 4, 6}`，`{-3, 8, 5, -6, 2}` 的结果为 `{-3, 5, -6, 2, 8}`。
  0 是偶数。
  对初始代码中的副本进行排序。
- `ordersBefore` 接受两个 `int` 值，并返回你的比较对该对值所给出的 `bool` 结果。
  `ordersBefore(3, 2)` 为 `true`，`ordersBefore(2, 3)` 为 `false`，`ordersBefore(4, 4)` 也为 `false`，而 `ordersBefore(1, 3)` 为 `true`（因为两者都是奇数且 1 较小）。
- 重新排序使用 `std::sort` 进行，并且捕获列表 `[]` 必须出现在你的比较中。
  无需添加 `main`：每个测试用例都会自行调用这些函数之一。

### 解答

```cpp
#include <algorithm>
#include <vector>

// 比较规则只存一次：奇数排在偶数前面，同组内从小到大
auto oddsFirst = [](int a, int b) {
    bool aOdd = a % 2 != 0;
    bool bOdd = b % 2 != 0;
    if (aOdd != bOdd) {
        return aOdd;
    }
    return a < b;
};

struct Solution {
    static bool ordersBefore(int first, int second) {
        // 返回比较规则对这一对值的判断
        return oddsFirst(first, second);
    }

    static std::vector<int> oddsBeforeEvens(const std::vector<int> &values) {
        std::vector<int> result = values;
        std::sort(result.begin(), result.end(), oddsFirst);
        return result;
    }
};
```
