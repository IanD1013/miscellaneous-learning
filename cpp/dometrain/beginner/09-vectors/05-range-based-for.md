括号内的冒号在一行中替换了计数器、条件和自增：

```cpp
#include <iostream>
#include <vector>

std::vector<double> v = {1.5, 2.25, 0.75};
for (double value : v) {
    std::cout << value << " ";
}
```

`double` 是元素类型，`value` 是循环体读取的名称，冒号将该名称与正在遍历的 vector 分隔开。
循环按顺序访问每个元素，每次遍历将其中一个元素复制到 `value` 中，因此这会打印 `1.5 2.25 0.75 `。
无需声明计数器、编写比较条件，也无需在括号中放置索引，循环既不会在最后一个元素之前停止，也不会越界。

由于 `value` 保存的是副本，在循环体中对其赋值只会更改副本，而保持 vector 完全不变。
在循环旁声明一个 `int` 并手动递增它，又重新引入了这种形式本意要消除的簿记操作。
当位置本身是答案的一部分时，索引循环仍然是可以指明位置的形式。

在名称之前编写的类型是一项决策。
`for (const auto &value : v)` 使 `value` 成为元素的别名而不是其副本，而 `const` 表示此循环仅读取其访问的内容。
一旦元素足够大以至于复制会产生开销，这种节省就很有价值。
`double` 足够小，复制它没有任何开销，因此这里直接使用普通形式即可。

`sumOfValues` 接收 `const std::vector<double> &values`，并将其元素的总和作为 `double` 返回。
在 `for (double value : values)` 上方声明该总和变量，并将每个访问的元素累加到其中。
当 `values` 为空时，循环体永远不会运行，并且总和将作为声明时的 0 返回。
`values[` 和 `.size()` 均被禁用，这明确排除了索引形式，并且你的循环头部需包含 `: values`（严格保持此空格格式），以确保遍历 vector 使用的是冒号形式本身。

## 解答

```cpp
#include <vector>

struct Solution {
    static double sumOfValues(const std::vector<double> &values) {
        // 用基于范围的 for 访问每个元素，并累加到总和中
        double total = 0;
        for (double value : values) {
            total += value;
        }
        return total;
    }
};
```
