截断发生在 `/` 内部，而不是在其下游的某个地方：`7 / 2` 的结果是 3，将该 3 复制到 `double` 变量中只会存储 3.0。
给运算符传入一个不同算术类型的操作数，结果就会改变。
在混合表达式中，`int` 会首先转换为 `double`，然后运算符会产生一个 `double`：

```cpp
7 / 2      // 3，两个操作数都是 int
7 / 2.0    // 3.5，有一个操作数是 double
```

这种选择是针对每个运算符、根据该运算符实际看到的两个操作数来决定的。
`double average = 7 / 2;` 仍然执行 `int` 除法，因为 `/` 的两边都是 `int`，而向 `double` 的转换是在小数部分已经丢失之后才发生的。
即使将变量或函数的返回类型声明为 `double` 也无法挽救这一点。

当两个值都存在 `int` 变量中时，由于无法直接输入小数点，因此需要你自己转换其中一个：

```cpp
int wins = 7;
static_cast<double>(wins)   // double 类型的 7.0；wins 仍然是 int 类型的 7
```

`static_cast<double>` 会返回括号中值的 `double` 副本，并保持原始变量不变。
将该副本放在 `/` 的任意一侧，整个除法就会变成 double 除法：一个操作数就足够了，因为另一个操作数会被自动转换以匹配它。
转换必须发生在除法之前，因为 `static_cast<double>(7 / 2)` 会先进行除法运算，然后才将 3 扩展为 3.0。

请补全 `averageOf(int total, int count)`，它接收一个大于或等于 0 的 `total` 和一个大于或等于 1 的 `count`，使其返回 `total` 除以 `count` 的结果（作为保留小数部分的 `double`）。
请使用 `static_cast<double>` 编写转换。
本练习不会出现 count 为 0 的情况。
评测机打印返回的 `double` 时不带末尾的零，因此精确的 3.0 会显示为 3，而八分之一会显示为 0.125。

## 解答

```cpp
struct Solution {
    static double averageOf(int total, int count) {
        // 先转换为 double 再相除，这样小数部分才能保留
        return static_cast<double>(total) / count;
    }
};
```
