有三个运算符可以将多个条件连接在一起。
`&&` 仅在两个操作数都为 `true` 时才返回 `true`；`||` 在其中任意一个操作数为 `true` 时就返回 `true`，因此至少有一个为 `true` 的操作数即可；而 `!` 则对其接收的单个操作数取反：

```cpp
int width = 4;
int height = 3;
bool bothPositive = width > 0 && height > 0;
bool eitherZero   = width == 0 || height == 0;
bool usable       = !eitherZero;
```

`&&` 和 `||` 的优先级低于比较运算符，因此 `width > 0 && height > 0` 会先进行两次比较，然后再进行 `&&` 运算，不需要括号。
`||` 的优先级更低，因此同时使用两者的表达式会先结合 `&&` 部分，如果要改变结合顺序就需要显式使用括号。
`!` 则恰恰相反：它的优先级高于任何比较运算符，因此 `!eitherZero` 是 `eitherZero` 的逻辑非，而 `!width == 9` 则会将 `width` 取反为 0 或 1，再拿它与 9 比较，当 `width` 为 4 时结果为 `false`，即使 4 并不等于 9。
如果要对比较操作取反，必须在比较表达式两边加上括号，这也是为什么分别给每个部分命名一个 `bool` 变量会很有价值的原因之一。

这两个连接运算符都具有短路特性。
`&&` 在计算完左操作数后，一旦其为 `false` 就会停止计算；而 `||` 一旦左操作数为 `true` 就会停止计算，因为此时结果已经确定。
短路能节省多少开销取决于操作数：右侧高开销的调用可以被完全跳过，但如果是在表达式之前就已经计算好的两个 `bool` 变量，开销则没有区别。

数学中的一种表达形式在编程中并不适用。
`low <= value <= high` 可以通过编译，但它会将第一次比较得到的 `true` 或 `false` 与 `high` 进行比较，对于范围 0 到 10 内 `value` 为 20 的情况，其计算结果居然会是 `true`。
每一端都需要单独进行比较。

完成 `isInRangeAndNotExcluded(int value, int low, int high, int excludedA, int excludedB)` 函数。
当 `value` 位于 `low` 和 `high` 之间（包含两个边界），且既不等于 `excludedA` 也不等于 `excludedB` 时，返回 `true`。
其他所有情况均返回 `false`，包括 `low` 大于 `high` 的空区间。
初始代码已经为你声明了 `inRange` 和 `excluded`。
请用通过 `&&` 连接的两个边界比较来填充第一个变量，用通过 `||` 连接的两个排除标记比较来填充第二个变量，然后返回用 `&&` 连接的两者的结果（其中排除条件需取反）。

## 解答

```cpp
struct Solution {
    static bool isInRangeAndNotExcluded(int value, int low, int high, int excludedA, int excludedB) {
        // 用两个边界构建 inRange，用两个排除标记构建 excluded
        bool inRange = value >= low && value <= high;
        bool excluded = value == excludedA || value == excludedB;
        return inRange && !excluded;
    }
};
```
