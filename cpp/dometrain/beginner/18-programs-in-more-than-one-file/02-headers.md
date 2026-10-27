一旦多个文件需要同一组声明，在文件之间来回复制很容易导致两份副本在不知不觉中产生不一致。
头文件就是包含声明的单个文件，每个需要这些声明的文件都可以包含（include）它：

```cpp
// sizes.hpp
#include <string>

int lengthOf(const std::string &text);
```

```cpp
// sizes.cpp
#include "sizes.hpp"

int lengthOf(const std::string &text) {
    return static_cast<int>(text.size());
}
```

`sizes.hpp` 声明了存在哪些内容。
`sizes.cpp` 实现了它，并包含 `lengthOf` 的唯一定义。
头文件本身包含了 `<string>`，因为它的声明中提到了 `std::string`，因此包含该头文件的文件在顶部不需要再额外添加其他内容。

include 后面的标点符号决定了从哪里开始搜索。
双引号（如 `#include "sizes.hpp"`）会优先在项目自身的文件中查找，这也是找到你自己的头文件的方式。
尖括号则会从编译器配置的路径开始搜索，这是 `<string>` 所在的位置，而当前项目自身的文件并不在那里，因此无论该文件多么显眼地摆在那里，`#include <sizes.hpp>` 都会报错提示找不到文件。

### 需求

- `checks.hpp` 是固定不变的，并且已经包含了 `<vector>`。
  在 `main.cpp` 的顶部保留 `#include "checks.hpp"`，并在其下方编写这两个函数的定义。
  在这里，该 include 引入了 `<vector>` 以及这两个声明；如果在调用者位于单独文件的构建环境中，这也是该文件能够访问这些函数的唯一途径。
- 严格与头文件保持一致：`bool allPositive(const std::vector<int> &values)` 和 `int firstNegativeIndex(const std::vector<int> &values)`。
  如果改为按值传递 vector，则会声明第二个函数，而原先声明的函数将没有函数体。
  这两个函数都不要标记为 `static`，因为评分器是通过函数名直接调用它们，而不是通过某种类型。
- 当每个值都大于 0 时，`allPositive` 返回 `true`。
  0 或负数都无法满足该条件，因此 `{4, 0, 9}` 和 `{4, -1, 9}` 都会返回 `false`；而空 vector 会返回 `true`，因为没有任何值违反该规则。
- `firstNegativeIndex` 返回从 0 开始计数的第一个小于 0 的值的位置：对于 `{4, -1, 9, -3}` 返回 1，对于 `{-2, 5}` 返回 0。
  如果没有任何负数，则返回 -1。
- `<checks.hpp>` 是被禁止的。

这里的两个头文件（上面的 `sizes.hpp` 和项目中的 `checks.hpp`）顶部都还缺少一行代码。
一个被多个文件访问的头文件需要一种机制来表明其内容在单次构建中不能被重复引入，下一课将会补充这一内容。

### 解答

```cpp
#include "checks.hpp"

bool allPositive(const std::vector<int> &values) {
    // 判断是否每个值都大于零
    for (int value : values) {
        if (value <= 0) {
            return false;
        }
    }
    return true;
}

int firstNegativeIndex(const std::vector<int> &values) {
    // 返回第一个小于零的值的位置，没有则返回 -1
    for (std::size_t i = 0; i < values.size(); i++) {
        if (values[i] < 0) {
            return static_cast<int>(i);
        }
    }
    return -1;
}
```
