调用函数意味着写出函数名，后接圆括号，括号内为函数声明的每个参数提供一个表达式。

```cpp
static int doubled(int value) {
    return value * 2;
}

static int spread(int low, int high) {
    return doubled(high) - doubled(low);
}
```

`doubled(high)` 就是一次调用。
控制流离开 `spread`，`value` 开始持有 `high` 所持有的值，执行函数体，然后返回的值回到写下调用的位置。
对返回 `int` 的函数的调用可以用于任何可以使用 `int` 的地方，因此两个调用可以放在一个减法运算中。
`doubled` 定义在调用者的上方，因为编译器是从上到下读取文件的：对于像这两个写在任何大括号之外的函数，尚未遇到的名称会被视为错误，而不是向下搜索的提示。

实参是按位置匹配的。
括号中的第一个表达式初始化第一个参数，第二个表达式初始化第二个参数，调用两端的变量名称不参与配对。
两个相同类型的参数很容易悄悄出错，因为 `doubled(high) - doubled(low)` 和 `doubled(low) - doubled(high)` 编译结果相同，但符号相反。

### 该函数发起的两次调用

- `raiseTo(int base, int exponent)` 返回 `base` 乘以自身 `exponent` 次的结果（其中 `exponent` 大于或等于 0）。
  将乘积初始值设为 1，在运行 `exponent` 次的循环中每轮将其乘以 `base` 一次，并返回该乘积。
  指数为 0 时循环执行 0 次并保持结果为 1。
- 在 `powerDifference(int base, int exponent)` 内部调用函数 `raiseTo` 两次，第一次为 `raiseTo(base, exponent)`，第二次为 `raiseTo(exponent, base)`，并返回第一个结果减去第二个结果的差。
  如果将调用单独放在一行上，则会执行 `raiseTo` 并丢弃其生成的结果。
- 两个输入都在 0 到 7 之间。
  两者都不会小于 0，这是调用方的约定：不会要求 `raiseTo` 进行负数次的乘法。
  2 和 3 返回 -1，3 和 2 返回 1，5 和 5 返回 0，4 和 0 返回 1，0 和 3 返回 -1。
- 将 `raiseTo` 保留在初始代码放置它的 `struct Solution` 上方，并将 `main` 留给运行器（运行器已经提供了一个）。
  评分调用会测试这两个函数，`raiseTo` 既会独立接受测试，也会通过 `powerDifference` 接受测试，因此如果辅助函数一直返回 1 本身就会测试失败。

### 解答

```cpp
static int raiseTo(int base, int exponent) {
    // 从 1 开始，把 base 连乘 exponent 次并返回乘积
    int product = 1;
    for (int i = 0; i < exponent; ++i) {
        product *= base;
    }
    return product;
}

struct Solution {
    static int powerDifference(int base, int exponent) {
        // 调用 raiseTo 两次，返回两个结果之差
        int first = raiseTo(base, exponent);
        int second = raiseTo(exponent, base);
        return first - second;
    }
};
```
